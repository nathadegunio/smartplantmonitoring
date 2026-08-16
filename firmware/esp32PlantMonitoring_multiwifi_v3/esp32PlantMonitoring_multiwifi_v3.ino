/*
===============================================================================
 SmartPlantMonitor.ino
-------------------------------------------------------------------------------
 Author      : Diether Masangcay
 Platform    : ESP32
 Sensors     : DHT22
               BH1750
               Capacitive Soil Moisture Sensor
 Display     : SH1106 OLED (128x64)
 Database    : Supabase
 Communication : WiFi

 Description
 ------------------------------------------------------------------------------
 SmartPlantMonitor is an IoT-based environmental monitoring system designed
 specifically for chilli plants.

 Every 30 minutes (NTP-aligned with the ESP32-CAM board) the ESP32 performs
 the following tasks:

    1. Reads environmental sensors
         • Temperature
         • Humidity
         • Soil Moisture
         • Light Intensity

    2. Evaluates whether the environment is suitable for chilli plant growth.

    3. Displays real-time sensor readings on the OLED.

    4. Displays the current health status of the plant.

    5. Sounds the buzzer whenever one or more environmental conditions are
       outside the recommended range.

    6. Uploads raw sensor readings to Supabase.

 IMPORTANT
 ------------------------------------------------------------------------------
 The ESP32 only performs sensor monitoring and simple status evaluation.

 Detailed recommendations, historical analytics, dashboards and charts are
 handled by the SmartPlant Web Application.

===============================================================================
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <Wire.h>
#include <BH1750.h>
#include <DHT.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SH110X.h>
#include <time.h>



//=============================================================================
// WiFi Configuration
//=============================================================================

// Multiple WiFi credentials
struct WiFiCredential {
  const char* ssid;
  const char* password;
};

//=============================================================================
// secrets.h
//
// Defines wifiNetworks[], SUPABASE_URL, and SUPABASE_KEY.
// Kept out of source control — copy secrets.h.example to secrets.h and
// fill in your own values before building.
//=============================================================================

#include "secrets.h"

const int WIFI_COUNT = sizeof(wifiNetworks)/sizeof(wifiNetworks[0]);



//=============================================================================
// ESP32 Pin Configuration
//=============================================================================

#define SDA_PIN      21
#define SCL_PIN      22

#define DHTPIN       5
#define DHTTYPE      DHT22

#define SOIL_PIN     34
#define BUZZER_PIN   18



//=============================================================================
// OLED Configuration
//=============================================================================

#define SCREEN_WIDTH   128
#define SCREEN_HEIGHT   64



//=============================================================================
// Hardware Objects
//=============================================================================

Adafruit_SH1106G display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);
BH1750 lightMeter;
DHT dht(DHTPIN, DHTTYPE);



//=============================================================================
// Soil Moisture Calibration
//
// Adjust these values according to your own soil sensor.
//
// DRY_VALUE -> Sensor reading in completely dry soil.
// WET_VALUE -> Sensor reading in fully wet soil.
//
// The raw analog reading is converted into a percentage (0-100%).
//=============================================================================

const int DRY_VALUE = 3200;
const int WET_VALUE = 1200;



//=============================================================================
// Chilli Plant Environmental Thresholds
//
// These thresholds are based on common chilli plant growing recommendations.
//
// Temperature
//    Cold      : < 24°C
//    Ideal     : 24°C - 32°C
//    Hot       : > 32°C
//
// Humidity
//    Low       : < 50%
//    Ideal     : 50% - 70%
//    High      : > 70%
//
// Soil Moisture
//    Dry       : < 40%
//    Moist     : 40% - 70%
//    Wet       : > 70%
//
// Light Intensity
//    Low       : < 10,000 lux
//    Ideal     : 10,000 - 50,000 lux
//    Very Bright : > 50,000 lux
//=============================================================================

const float TEMP_LOW_LIMIT      = 24.0;
const float TEMP_HIGH_LIMIT     = 32.0;

const float HUMIDITY_LOW_LIMIT  = 50.0;
const float HUMIDITY_HIGH_LIMIT = 70.0;

const int SOIL_DRY_LIMIT        = 40;
const int SOIL_WET_LIMIT        = 70;

const float LIGHT_LOW_LIMIT     = 10000;
const float LIGHT_HIGH_LIMIT    = 50000;



//=============================================================================
// System Timing
//
// SENSOR_INTERVAL
//     Sensor reading and Supabase upload interval, in milliseconds.
//     Used only as the offline fallback interval — see UPLOAD_SLOT_SECONDS
//     below for the normal NTP-aligned schedule.
//
// PAGE_INTERVAL
//     OLED page switching interval.
//
//=============================================================================

const unsigned long SENSOR_INTERVAL = 1800000UL;   // 30 minutes
const unsigned long PAGE_INTERVAL   = 5000UL;

//=============================================================================
// NTP Time Sync
//
// The ESP32-CAM board runs the same 30-minute upload schedule
// independently. Both boards align their uploads to wall-clock time
// (e.g. :00 and :30 past the hour) via NTP instead of counting from
// their own boot time, so the two boards' uploads land at the same time
// without talking to each other directly.
//=============================================================================

const long GMT_OFFSET_SEC      = 8 * 3600;   // Philippines, UTC+8
const int  DAYLIGHT_OFFSET_SEC = 0;

const unsigned long UPLOAD_SLOT_SECONDS = SENSOR_INTERVAL / 1000UL;

// Sanity threshold for "has NTP actually synced" (~Nov 2023).
// Before sync, time(nullptr) reports a small number near epoch 0.
const time_t NTP_SANITY_THRESHOLD = 1700000000;



//=============================================================================
// Sensor Values
//=============================================================================

float lux = 0;
float temp = 0;
float humidity = 0;

int moisture = 0;



//=============================================================================
// Chilli Plant Status
//
// Each sensor is classified into one of three conditions.
//
// Temperature
//      Cold
//      Ideal
//      Hot
//
// Humidity
//      Low
//      Ideal
//      High
//
// Soil
//      Dry
//      Moist
//      Wet
//
// Light
//      Low
//      Ideal
//      Very Bright
//=============================================================================

String tempStatus;
String humStatus;
String soilStatus;
String lightStatus;



//=============================================================================
// Recommendation Messages
//
// These short messages are shown on the OLED.
//
// More detailed recommendations will be generated by the web application.
//=============================================================================

String tempReco;
String humReco;
String soilReco;
String lightReco;



//=============================================================================
// Alert Flags
//
// TRUE means the sensor value is outside the ideal growing range.
//
// These flags are also used to determine the number of buzzer beeps.
//=============================================================================

bool soilAlert = false;
bool tempAlert = false;
bool humAlert = false;
bool lightAlert = false;



//=============================================================================
// Alert Counter
//
// Counts how many environmental factors are currently outside
// the recommended range.
//
// Example
//
//    0 = Plant is healthy
//    1 = One issue
//    2 = Two issues
//    3 = Three issues
//    4 = Four issues
//=============================================================================

int alertCount = 0;



//=============================================================================
// OLED Page Control
//=============================================================================

bool showSensorPage = true;

long lastUploadSlot = -1;
unsigned long lastFallbackUpload = 0;
unsigned long lastPage = 0;


//=============================================================================
// connectWiFi()
//
// Attempts to connect to WiFi.
//
// If the connection cannot be established within 10 seconds,
// the ESP32 continues operating in OFFLINE mode.
//
// Offline Mode
// -------------
// ✓ Sensor reading
// ✓ OLED display
// ✓ Buzzer alerts
//
// Disabled while offline
// ----------------------
// ✗ Uploading to Supabase
//
// The ESP32 will automatically retry connecting whenever
// uploadToSupabase() is called.
//=============================================================================

void connectWiFi()
{
    if (WiFi.status() == WL_CONNECTED) return;

    WiFi.mode(WIFI_STA);
    WiFi.setAutoReconnect(true);
    WiFi.persistent(true);

    Serial.println("Searching for known WiFi...");

    for(int i=0;i<WIFI_COUNT;i++)
    {
        Serial.print("Trying: ");
        Serial.println(wifiNetworks[i].ssid);

        WiFi.begin(wifiNetworks[i].ssid, wifiNetworks[i].password);

        unsigned long start=millis();

        while(WiFi.status()!=WL_CONNECTED && millis()-start<10000)
        {
            delay(500);
            Serial.print(".");
        }

        Serial.println();

        if(WiFi.status()==WL_CONNECTED)
        {
            Serial.print("Connected to: ");
            Serial.println(wifiNetworks[i].ssid);
            Serial.print("IP: ");
            Serial.println(WiFi.localIP());

            // Sync wall-clock time so uploads land on the same
            // :00 / :30 boundaries as the ESP32-CAM board.
            configTime(GMT_OFFSET_SEC, DAYLIGHT_OFFSET_SEC, "pool.ntp.org", "time.google.com");

            return;
        }

        WiFi.disconnect(true,true);
        delay(500);
    }

    Serial.println("No known WiFi available. Running in offline mode.");
}



//=============================================================================
// dueForUpload()
//
// Returns true once per 30-minute window.
//
// When NTP time is synced, this aligns to wall-clock :00 / :30 boundaries
// so this board and the ESP32-CAM board upload within moments of each
// other. Falls back to a plain millis() countdown when NTP hasn't synced
// yet (e.g. still offline), so uploads keep happening on schedule
// regardless of network state.
//=============================================================================

bool dueForUpload()
{
    time_t now = time(nullptr);

    if (now > NTP_SANITY_THRESHOLD)
    {
        long slot = now / UPLOAD_SLOT_SECONDS;

        if (slot != lastUploadSlot)
        {
            lastUploadSlot = slot;
            lastFallbackUpload = millis();
            return true;
        }

        return false;
    }

    if (millis() - lastFallbackUpload >= SENSOR_INTERVAL)
    {
        lastFallbackUpload = millis();
        return true;
    }

    return false;
}




//=============================================================================
// beep()
//
// Sounds the buzzer a specified number of times.
//
// Number of beeps corresponds to the number of environmental conditions
// that are outside the recommended chilli plant growing range.
//
// Example
//
//     0 alerts -> No sound
//     1 alert  -> One beep
//     2 alerts -> Two beeps
//     3 alerts -> Three beeps
//     4 alerts -> Four beeps
//
// This provides a quick audible indication without requiring the user
// to look at the OLED display.
//=============================================================================

void beep(byte numberOfBeeps)
{
    for (byte i = 0; i < numberOfBeeps; i++)
    {
        digitalWrite(BUZZER_PIN, HIGH);
        delay(180);

        digitalWrite(BUZZER_PIN, LOW);

        if (i < numberOfBeeps - 1)
            delay(180);
    }
}



//=============================================================================
// readSensors()
//
// Reads all connected environmental sensors.
//
// Sensors
// --------
// • BH1750  -> Light Intensity (Lux)
// • DHT22   -> Temperature (°C)
// • DHT22   -> Relative Humidity (%)
// • Soil Sensor -> Soil Moisture (%)
//
// Soil Moisture Conversion
// ------------------------
// The ESP32 reads a raw analog value (0-4095).
//
// This value is mapped into a percentage:
//
//      0%   = Completely Dry
//      100% = Fully Wet
//
// The DRY_VALUE and WET_VALUE constants should be calibrated according
// to the specific soil moisture sensor being used.
//=============================================================================

void readSensors()
{
    //-------------------------------
    // Read Light Sensor
    //-------------------------------

    lux = lightMeter.readLightLevel();


    //-------------------------------
    // Read Temperature & Humidity
    //-------------------------------

    humidity = dht.readHumidity();
    temp = dht.readTemperature();


    //-------------------------------
    // Read Soil Moisture
    //-------------------------------

    int rawSoil = analogRead(SOIL_PIN);

    moisture = constrain(
        map(rawSoil, DRY_VALUE, WET_VALUE, 0, 100),
        0,
        100
    );


    //-------------------------------
    // Debug Output
    //-------------------------------

    Serial.println();
    Serial.println("========== Sensor Reading ==========");

    Serial.print("Temperature : ");
    Serial.print(temp);
    Serial.println(" °C");

    Serial.print("Humidity    : ");
    Serial.print(humidity);
    Serial.println(" %");

    Serial.print("Light       : ");
    Serial.print(lux);
    Serial.println(" lux");

    Serial.print("Soil        : ");
    Serial.print(moisture);
    Serial.println(" %");

    Serial.println("====================================");

    
}



//=============================================================================
// evaluateAlerts()
//
// Purpose
// -----------------------------------------------------------------------------
// Evaluates whether the current environmental conditions are suitable for
// growing chilli plants.
//
// This function DOES NOT change or modify any sensor readings.
//
// Instead, it classifies each sensor reading into a human-readable status,
// stores a short recommendation for OLED display, and determines whether
// the condition should trigger an alert.
//
// The total number of non-ideal conditions is stored in alertCount.
// This value is later used to determine how many times the buzzer sounds.
//
// Classification Summary
// -----------------------------------------------------------------------------
//
// Temperature (°C)
//      < 24      -> Cold
//      24-32     -> Ideal
//      > 32      -> Hot
//
// Humidity (%)
//      < 50      -> Low
//      50-70     -> Ideal
//      > 70      -> High
//
// Soil Moisture (%)
//      < 40      -> Dry
//      40-70     -> Moist
//      > 70      -> Wet
//
// Light Intensity (Lux)
//      < 10,000      -> Low Light
//      10k - 50k     -> Ideal
//      > 50k         -> Very Bright
//
// NOTE
// -----------------------------------------------------------------------------
// The ESP32 only performs simple environmental classification.
//
// More detailed recommendations, notifications, historical analytics,
// dashboards, and reports are generated by the SmartPlant Web Application.
//
//=============================================================================

void evaluateAlerts()
{
    // Reset alert counter before evaluating all sensors.
    alertCount = 0;

    //=========================================================================
    // TEMPERATURE
    //=========================================================================
    //
    // Chilli plants grow best between 24°C and 32°C.
    //
    // Below 24°C
    //     Plant growth slows and cold stress may occur.
    //
    // Above 32°C
    //     Heat stress may increase water loss and reduce productivity.
    //
    //=========================================================================

    if (temp < TEMP_LOW_LIMIT)
    {
        tempStatus = "Cold";
        tempReco = "Move warmer";

        tempAlert = true;
        alertCount++;
    }
    else if (temp <= TEMP_HIGH_LIMIT)
    {
        tempStatus = "Ideal";
        tempReco = "Healthy";

        tempAlert = false;
    }
    else
    {
        tempStatus = "Hot";
        tempReco = "Provide shade";

        tempAlert = true;
        alertCount++;
    }


    //=========================================================================
    // HUMIDITY
    //=========================================================================
    //
    // Recommended humidity:
    //      50% - 70%
    //
    // Low humidity can increase water loss.
    // High humidity can encourage fungal diseases.
    //
    //=========================================================================

    if (humidity < HUMIDITY_LOW_LIMIT)
    {
        humStatus = "Low";
        humReco = "Increase humidity";

        humAlert = true;
        alertCount++;
    }
    else if (humidity <= HUMIDITY_HIGH_LIMIT)
    {
        humStatus = "Ideal";
        humReco = "Healthy";

        humAlert = false;
    }
    else
    {
        humStatus = "High";
        humReco = "Improve airflow";

        humAlert = true;
        alertCount++;
    }


    //=========================================================================
    // SOIL MOISTURE
    //=========================================================================
    //
    // Dry (<40%)
    //      Water the plant soon.
    //
    // Moist (40-70%)
    //      Ideal soil moisture.
    //
    // Wet (>70%)
    //      Delay watering to reduce root rot risk.
    //
    //=========================================================================

    if (moisture < SOIL_DRY_LIMIT)
    {
        soilStatus = "Dry";
        soilReco = "Water soon";

        soilAlert = true;
        alertCount++;
    }
    else if (moisture <= SOIL_WET_LIMIT)
    {
        soilStatus = "Moist";
        soilReco = "Healthy";

        soilAlert = false;
    }
    else
    {
        soilStatus = "Wet";
        soilReco = "Delay watering";

        soilAlert = true;
        alertCount++;
    }


    //=========================================================================
    // LIGHT INTENSITY
    //=========================================================================
    //
    // Low Light
    //      Photosynthesis may be insufficient.
    //
    // Ideal
    //      Suitable for healthy growth.
    //
    // Very Bright
    //      Plant may experience heat stress during peak sunlight.
    //
    //=========================================================================

    if (lux < LIGHT_LOW_LIMIT)
    {
        lightStatus = "Low";
        lightReco = "More sunlight";

        lightAlert = true;
        alertCount++;
    }
    else if (lux <= LIGHT_HIGH_LIMIT)
    {
        lightStatus = "Ideal";
        lightReco = "Healthy";

        lightAlert = false;
    }
    else
    {
        lightStatus = "Bright";
        lightReco = "Provide shade";

        lightAlert = true;
        alertCount++;
    }


    //=========================================================================
    // Debug Output
    //=========================================================================
    //
    // Print the environmental classification to the Serial Monitor.
    // This is useful during development and troubleshooting.
    //
    //=========================================================================

    Serial.println();
    Serial.println("========= Plant Evaluation =========");

    Serial.print("Temperature : ");
    Serial.println(tempStatus);

    Serial.print("Humidity    : ");
    Serial.println(humStatus);

    Serial.print("Soil        : ");
    Serial.println(soilStatus);

    Serial.print("Light       : ");
    Serial.println(lightStatus);

    Serial.print("Alerts      : ");
    Serial.println(alertCount);

    Serial.println("====================================");
}


//=============================================================================
// uploadToSupabase()
//
// Purpose
// -----------------------------------------------------------------------------
// Uploads the latest sensor readings to the Supabase database using the
// REST API.
//
// The ESP32 only uploads RAW SENSOR VALUES.
//
// No recommendation or plant health analysis is uploaded because those
// processes are handled by the SmartPlant Web Application.
//
// Uploaded Fields
// -----------------------------------------------------------------------------
// temperature_c
// humidity
// light_intensity
// soil_moisture
//
// Database Table
// -----------------------------------------------------------------------------
// esp32_log
//
// Request Type
// -----------------------------------------------------------------------------
// HTTP POST
//
// Authentication
// -----------------------------------------------------------------------------
// • apikey
// • Bearer Token
//
// NOTE
// -----------------------------------------------------------------------------
// If the DHT22 fails to return valid readings, the upload is skipped to
// prevent storing invalid (NaN) values in the database.
//
//=============================================================================

void uploadToSupabase()
{
    //---------------------------------------------------------------------
    // Validate DHT22 readings before uploading.
    //---------------------------------------------------------------------

    if (isnan(temp) || isnan(humidity))
    {
        Serial.println();
        Serial.println("Upload Cancelled");
        Serial.println("Reason : Invalid DHT22 reading.");
        return;
    }


    //---------------------------------------------------------------------
    // Ensure WiFi connection is available.
    //---------------------------------------------------------------------

    connectWiFi();

  if(WiFi.status()!=WL_CONNECTED){
    Serial.println("Upload skipped (offline)");
    return;
  }

    if (WiFi.status() != WL_CONNECTED)
{
    Serial.println("Upload skipped (No WiFi)");
    return;
}


    //---------------------------------------------------------------------
    // Create JSON document containing the latest sensor readings.
    //---------------------------------------------------------------------

    StaticJsonDocument<256> jsonDocument;

    jsonDocument["temperature_c"] = temp;
    jsonDocument["humidity"] = humidity;
    jsonDocument["light_intensity"] = lux;
    jsonDocument["soil_moisture"] = moisture;


    //---------------------------------------------------------------------
    // Convert JSON document into a String for HTTP transmission.
    //---------------------------------------------------------------------

    String requestBody;
    serializeJson(jsonDocument, requestBody);


    //---------------------------------------------------------------------
    // Configure HTTP Client.
    //---------------------------------------------------------------------

    HTTPClient http;

    http.begin(String(SUPABASE_URL) + "/rest/v1/esp32_log");

    http.addHeader("Content-Type", "application/json");
    http.addHeader("apikey", SUPABASE_KEY);
    http.addHeader("Authorization", "Bearer " + String(SUPABASE_KEY));

    // Return the inserted row after a successful POST.
    http.addHeader("Prefer", "return=representation");


    //---------------------------------------------------------------------
    // Send HTTP POST request.
    //---------------------------------------------------------------------

    int httpResponseCode = http.POST(requestBody);


    //---------------------------------------------------------------------
    // Display upload result in the Serial Monitor.
    //---------------------------------------------------------------------

    Serial.println();
    Serial.println("========== Supabase Upload ==========");

    Serial.print("HTTP Response : ");
    Serial.println(httpResponseCode);

    Serial.println();
    Serial.println("Uploaded JSON");

    Serial.println(requestBody);

    Serial.println();
    Serial.println("Server Response");

    Serial.println(http.getString());

    Serial.println("=====================================");


    //---------------------------------------------------------------------
    // Close HTTP connection.
    //---------------------------------------------------------------------

    http.end();
}


//=============================================================================
// drawSensorPage()
//
// Purpose
// -----------------------------------------------------------------------------
// Displays the latest sensor readings collected from the environmental
// sensors.
//
// Displayed Information
// -----------------------------------------------------------------------------
// • Temperature
// • Humidity
// • Soil Moisture
// • Light Intensity
//
// This screen is intended to provide users with real-time environmental
// measurements.
//
// The OLED automatically switches to the Plant Status page every
// PAGE_INTERVAL (5 seconds).
//=============================================================================

void drawSensorPage()
{
    display.clearDisplay();

    display.setTextSize(1);
    display.setCursor(0,0);

    display.println("=== Sensor Reading ===");

    display.printf("Temp : %.1f C\n", temp);

    display.printf("Hum  : %.0f %%\n", humidity);

    display.printf("Soil : %d %%\n", moisture);

    display.printf("Light: %.0f lx\n", lux);

    display.display();
}



//=============================================================================
// drawAlertPage()
//
// Purpose
// -----------------------------------------------------------------------------
// Displays the environmental status for chilli plants.
//
// Instead of displaying raw sensor values, this page displays whether
// each environmental factor is currently:
//
// • Ideal
// • Cold / Hot
// • Low / High
// • Dry / Wet
//
// If every environmental condition is within the recommended growing
// range, the plant is considered healthy.
//
// This page automatically alternates with the Sensor Reading page every
// 5 seconds.
//=============================================================================

void drawAlertPage()
{
    display.clearDisplay();

    display.setTextSize(1);
    display.setCursor(0,0);

    display.println("=== Plant Status ===");

    display.print("Temp : ");
    display.println(tempStatus);

    display.print("Hum  : ");
    display.println(humStatus);

    display.print("Soil : ");
    display.println(soilStatus);

    display.print("Light: ");
    display.println(lightStatus);

    display.display();
}

//=============================================================================
// setup()
//
// Purpose
// -----------------------------------------------------------------------------
// Performs all one-time hardware and software initialization when the ESP32
// powers on or resets.
//
// Initialization Sequence
// -----------------------------------------------------------------------------
// 1. Start Serial Monitor
// 2. Configure buzzer output pin
// 3. Initialize I2C communication
// 4. Configure ADC resolution
// 5. Initialize sensors
//      • DHT22
//      • BH1750
// 6. Initialize OLED display
// 7. Connect to WiFi
// 8. Read initial sensor values
// 9. Evaluate chilli plant environmental conditions
//
// After setup() finishes, the loop() function executes continuously.
//=============================================================================

void setup()
{
    //------------------------------------------------------------
    // Initialize Serial Monitor
    //------------------------------------------------------------

    Serial.begin(115200);

    Serial.println();
    Serial.println("========================================");
    Serial.println("      Smart Plant Monitor Starting");
    Serial.println("========================================");


    //------------------------------------------------------------
    // Configure buzzer
    //------------------------------------------------------------

    pinMode(BUZZER_PIN, OUTPUT);
    digitalWrite(BUZZER_PIN, LOW);


    //------------------------------------------------------------
    // Initialize I2C communication
    //------------------------------------------------------------

    Wire.begin(SDA_PIN, SCL_PIN);


    //------------------------------------------------------------
    // Configure Analog-to-Digital Converter
    //------------------------------------------------------------

    analogReadResolution(12);


    //------------------------------------------------------------
    // Initialize Sensors
    //------------------------------------------------------------

    dht.begin();

    lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE);


    //------------------------------------------------------------
    // Initialize OLED Display
    //------------------------------------------------------------

    display.begin(0x3C, true);
    display.setTextColor(SH110X_WHITE);
    display.clearDisplay();
    display.display();


    //------------------------------------------------------------
    // Connect to WiFi
    //------------------------------------------------------------

    connectWiFi();


    //------------------------------------------------------------
    // Read initial sensor values
    //------------------------------------------------------------

    readSensors();


    //------------------------------------------------------------
    // Evaluate chilli plant conditions
    //------------------------------------------------------------

    evaluateAlerts();


    Serial.println();
    Serial.println("System Initialization Complete");
    Serial.println();
}



//=============================================================================
// loop()
//
// Purpose
// -----------------------------------------------------------------------------
// Main execution loop.
//
// The ESP32 continuously performs two independent timed tasks:
//
// -----------------------------------------------------------------------------
// Task 1 (Every 30 Minutes, NTP-aligned)
//
// • Read all sensors
// • Evaluate chilli plant conditions
// • Sound buzzer if required
// • Upload raw sensor data to Supabase
//
// -----------------------------------------------------------------------------
// Task 2 (Every 5 Seconds)
//
// Alternate between:
//
//     Screen 1
//         Sensor Readings
//
//     Screen 2
//         Plant Status
//
// This provides users with both raw environmental data and an easy-to-read
// assessment of the current growing conditions.
//
//=============================================================================

void loop()
{
    unsigned long currentMillis = millis();


    //=====================================================================
    // Sensor Update Task
    //
    // Executes once every 30-minute window (NTP-aligned — see
    // dueForUpload() above).
    //=====================================================================

    if (dueForUpload())
    {

        //----------------------------------------------------------
        // Read all environmental sensors
        //----------------------------------------------------------

        readSensors();


        //----------------------------------------------------------
        // Evaluate current chilli plant conditions
        //----------------------------------------------------------

        evaluateAlerts();


        //----------------------------------------------------------
        // Audible alert
        //
        // Number of beeps equals the number of environmental
        // conditions outside the recommended range.
        //----------------------------------------------------------

        if (alertCount > 0)
        {
            beep(alertCount);
        }


        //----------------------------------------------------------
        // Upload sensor readings to Supabase
        //----------------------------------------------------------

        uploadToSupabase();
    }


    //=====================================================================
    // OLED Screen Switching Task
    //
    // Automatically alternates between:
    //
    // Screen 1 : Sensor Reading
    // Screen 2 : Plant Status
    //
    // every PAGE_INTERVAL (5 seconds).
    //=====================================================================

    if (currentMillis - lastPage >= PAGE_INTERVAL)
    {
        lastPage = currentMillis;

        showSensorPage = !showSensorPage;
    }


    //=====================================================================
    // Draw the currently selected OLED page.
    //=====================================================================

    if (showSensorPage)
    {
        drawSensorPage();
    }
    else
    {
        drawAlertPage();
    }
}

