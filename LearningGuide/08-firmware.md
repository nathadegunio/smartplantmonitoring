# Chapter 08 — The Firmware

[← Previous](07-electronics-and-sensors.md) · [Contents](README.md) · [Next: The Cloud Database →](09-cloud-database.md)

---

## What firmware is

**Firmware** is a program that lives permanently inside a device and runs the moment it gets power.

Your laptop loads programs from a hard drive when you double-click them. The ESP32 has no hard drive and nothing to click. It has one program burned into its memory, and it starts running the instant electricity arrives and does not stop until electricity leaves.

That is the whole difference. Firmware is a program that *is* the device.

The file is `esp32PlantMonitoring_multiwifi_v3.ino`. It is about 1,200 lines, and the great majority of that is comments and screen-drawing code. The actual logic is small.

---

## setup() and loop()

Every Arduino-style program has exactly two required functions:

```c
void setup() {
    // runs ONCE, when power arrives
}

void loop() {
    // runs over and over, forever, until power is removed
}
```

That is the shape of every embedded program you will ever write.

**In this project:**

`setup()` — start the serial connection so you can watch it, wake up the OLED screen, wake up each sensor, connect to WiFi, and sync the clock from the internet.

`loop()` — read the sensors, check them against the ideal ranges, update the screen, beep if needed, and every five minutes send everything to the cloud.

---

## The functions, and what each one is for

The whole firmware is these ten functions. Read the names — you can almost see the program from the list alone:

| Function | Its job |
|---|---|
| `connectWiFi()` | Try each saved WiFi network until one works |
| `dueForUpload()` | Decide whether it is time to send data |
| `readSensors()` | Ask every sensor for its current value |
| `evaluateAlerts()` | Compare readings to the ideal ranges |
| `beep()` | Sound the buzzer N times |
| `drawSensorPage()` | Draw the numbers on the OLED |
| `drawAlertPage()` | Draw the warnings on the OLED |
| `uploadToSupabase()` | Send the readings to the cloud |
| `setup()` | Start everything up |
| `loop()` | Do it all, forever |

Naming things well is genuinely half of programming. Notice you can guess what every one of those does without opening it.

---

## Four interesting decisions in this firmware

The basic stuff is not worth walking through line by line. These four decisions are — because each one solves a real problem, and each one is the kind of thing you would only discover by actually running a device outdoors for a week.

### 1. Multiple WiFi networks

```c
WiFiCredential wifiNetworks[] = {
  {"YOUR_WIFI_SSID_1", "YOUR_WIFI_PASSWORD_1"},
  {"YOUR_WIFI_SSID_2", "YOUR_WIFI_PASSWORD_2"},
};
```

The device stores a **list** of networks and tries each in turn. That is what "multiwifi" in the filename means.

Why? Because a device that works in the school garden and dies when you bring it home for testing is infuriating. Store both networks, it works in both places.

And critically: if **no** network connects, the device **does not stop**. It keeps reading sensors, keeps showing them on the OLED, keeps beeping about problems — it just cannot upload. It tries WiFi again next cycle.

This is called **graceful degradation**: when part of a system fails, the rest keeps doing what it still can. Compare that to a design where losing WiFi means the whole device freezes. Same hardware, vastly different reliability.

### 2. Aligning uploads to clean clock times

Naive approach: upload every five minutes counting from boot. Simple, and it produces timestamps like 2:03, 2:08, 2:13 — ugly, and different every time you restart the device.

What this firmware does instead:

```c
const long GMT_OFFSET_SEC = 8 * 3600;   // Philippines, UTC+8
const unsigned long UPLOAD_SLOT_SECONDS = SENSOR_INTERVAL / 1000UL;
```

It gets the real time from the internet (a service called **NTP** — Network Time Protocol), then uploads aligned to wall-clock boundaries: 2:00, 2:05, 2:10, 2:15.

Why bother? Clean, predictable data. Charts line up. You can look at the database and immediately see if a reading is missing.

And there is a fallback — if NTP never syncs (no internet at boot), it falls back to plain five-minute counting. **Better ugly data than no data.**

### 3. The one-minute settle delay

```c
const unsigned long BOOT_DELAY_MS = 60000UL;   // 1 minute
```

When the device first powers on, it waits a full minute before its first reading.

Why? Because in that first minute WiFi is still negotiating, the clock has not synced, and the DHT22 sensor has not thermally settled. Readings taken immediately after boot are unreliable.

This is the kind of thing you only learn by watching a device in the real world and noticing that the first reading after every restart is garbage. Then you add a delay, and the problem goes away.

Real engineering is full of these. They look arbitrary in the code, and every one of them is a scar from a real problem.

### 4. Raw data only

The firmware knows the ideal ranges — it uses them for the buzzer and the OLED:

```c
const float TEMP_LOW_LIMIT      = 24.0;
const float TEMP_HIGH_LIMIT     = 32.0;
const float HUMIDITY_LOW_LIMIT  = 50.0;
const float HUMIDITY_HIGH_LIMIT = 70.0;
const int   SOIL_DRY_LIMIT      = 40;
const int   SOIL_WET_LIMIT      = 70;
const float LIGHT_LOW_LIMIT     = 10000;
const float LIGHT_HIGH_LIMIT    = 50000;
```

But it uploads **only the four raw numbers**. No health score, no advice, no status.

The comment at the top of the file states this deliberately:

> *The ESP32 only performs sensor monitoring and simple status evaluation. Detailed recommendations, historical analytics, dashboards and charts are handled by the SmartPlant Web Application.*

Chapter 06 covered why: things that change often should live where they are easy to change. Editing a number in the web app is instant. Editing a number on the chip means recompiling and physically re-flashing the device in the garden.

> **Worth noticing:** those same eight numbers appear again in `services/health.py` in the web app, and again in the AI prompt in `services/ai_insights.py`. The same knowledge, written in three places. That is a real weakness in this design — change one and forget the others, and the device beeps while the dashboard says everything is fine. Spotting things like this is a genuinely valuable skill. If you rebuild this, think about whether you can define those ranges once.

---

## The upload, step by step

`uploadToSupabase()` does this:

1. **Check the readings are valid.** If the DHT22 returned nonsense, skip the whole upload. Never send bad data.
2. **Build a JSON packet** — a small block of text in the format APIs expect:
   ```json
   {
     "temperature_c": 31.2,
     "humidity": 58.0,
     "light_intensity": 42000,
     "soil_moisture": 52
   }
   ```
   The `ArduinoJson` library builds this.
3. **Open an HTTPS connection** to your Supabase URL.
4. **Attach the API key** as a header, proving the device is allowed to write.
5. **POST the packet.** POST is the HTTP word for "here is some new data, store it."
6. **Check the response code.** 200 or 201 means success. Anything else gets printed to Serial so you can see what went wrong.

That sequence — build data, authenticate, send, check response — is what *every* program talking to *any* API does. Learn it once, recognize it everywhere.

---

## secrets.h

At the top of the firmware:

```c
#include "secrets.h"
```

That pulls in a separate file holding the WiFi passwords and the Supabase key. Those values are not in the `.ino` file.

Why split them out? Because the `.ino` is on public GitHub and `secrets.h` is not. Chapter 13 covers this fully.

What is committed instead is `secrets.h.example` — the same file with the real values replaced by placeholders:

```c
WiFiCredential wifiNetworks[] = {
  {"YOUR_WIFI_SSID_1", "YOUR_WIFI_PASSWORD_1"},
};

#define SUPABASE_URL "https://YOUR_PROJECT_REF.supabase.co"
#define SUPABASE_KEY "YOUR_SUPABASE_PUBLISHABLE_KEY"
```

So anyone can see the *shape* of what is needed without seeing the actual values. Copy it to `secrets.h`, fill in your own, and it compiles.

**The sketch will not compile without a `secrets.h`.** That is the first error you will hit, and now you know the fix.

---

## Flashing it onto the board

"Flashing" means copying the compiled program onto the chip.

1. **Plug the ESP32 into your laptop** with a USB **data** cable.
2. **Arduino IDE → Tools → Board** → pick your ESP32 model (often "ESP32 Dev Module").
3. **Tools → Port** → pick the COM port that appeared when you plugged it in. If none appeared, you need a driver — Chapter 03, section 6.
4. **Open the `.ino` file.**
5. **Make sure `secrets.h` exists** in the same folder with your real values.
6. **Click Verify** (the ✓). This compiles without uploading. Fix any errors here first.
7. **Click Upload** (the →). This compiles and copies to the board.
8. **Open Tools → Serial Monitor**, set speed to **115200**, and watch it boot.

> **If upload fails with "Failed to connect":** some boards need you to hold the **BOOT** button while the upload starts, then release. Annoying, well-known, harmless.

---

## Reading the Serial Monitor

This is how you know the device is alive and healthy. You will see it report which WiFi it connected to, what each sensor read, whether the upload succeeded, and the reason if it did not.

**When something is wrong, this is where you look first.** Not the dashboard, not the database. Here. The firmware tells you what it is doing at every step; you just have to be watching.

---

## If you were rebuilding this

You would not type 1,200 lines. You would have a conversation something like:

> I have an ESP32 with a DHT22 on pin 5, a BH1750 light sensor and an SH1106 OLED on I2C pins 21 and 22, a capacitive soil moisture sensor on pin 34, and a buzzer on pin 18.
>
> Write firmware that reads all four sensors every 5 minutes and shows them on the OLED. Beep once per problem when any reading is outside these ranges: temperature 24–32 C, humidity 50–70 percent, soil moisture 40–70 percent, light 10,000–50,000 lux.
>
> Put the WiFi credentials and API key in a separate `secrets.h` file, and support a list of multiple WiFi networks to try in order. If none connect, keep running offline and retry next cycle.
>
> Explain each section as you write it — I am a beginner.

Then you would run it, watch the Serial Monitor, find the soil readings were wrong, and come back with:

> The soil moisture reads 100 percent even when the probe is in dry air. Raw analog value in dry air is about 3300 and in water is about 1150. Fix the calibration.

**That is how this file actually came to exist.** Not typed from memory — described, run, corrected, repeated.

---

[← Previous](07-electronics-and-sensors.md) · [Contents](README.md) · [Next: The Cloud Database →](09-cloud-database.md)
