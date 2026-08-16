/*
 * ESP32-CAM OV2640 — WEB STREAMER + SUPABASE AUTO-CAPTURE
 * =========================================================
 * Single file. No board_config.h, no app_httpd.cpp needed.
 * Pinout + XCLK already set to the values your board verified.
 *
 * ---------------- ARDUINO IDE SETTINGS ----------------
 *   Board            : AI Thinker ESP32-CAM
 *   Partition Scheme : Huge APP (3MB No OTA/1MB SPIFFS)
 *   PSRAM            : Enabled
 *   Flash Frequency  : 80 MHz
 *   Upload Speed     : 115200
 *   Serial Monitor   : 115200 baud
 * ------------------------------------------------------
 *
 * Pages served (once connected to WiFi):
 *   http://<ip>/          control page with live stream
 *   http://<ip>/stream    raw MJPEG (open directly in VLC if you like)
 *   http://<ip>/capture   single JPEG still
 *   http://<ip>/led?v=0   flash LED off  (v=0..255)
 *   http://<ip>/size?v=8  resolution, see table on the page
 *
 * Background task (independent of the pages above):
 *   Every 30 minutes, aligned to wall-clock :00/:30 via NTP (same schedule
 *   as the esp32PlantMonitoring_multiwifi_v3 sensor board), this board
 *   grabs one best-quality still and uploads it to Supabase Storage as
 *   app-files/latest.jpg (overwritten each cycle — no photo history).
 */

#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <time.h>
#include "esp_camera.h"
#include "esp_http_server.h"
#include "esp_timer.h"

// ===========================
//  WiFi — same networks as the sensor board, tried in order
// ===========================

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

const int WIFI_COUNT = sizeof(wifiNetworks) / sizeof(wifiNetworks[0]);

// ===========================
//  Supabase Storage — same project as the sensor board
// ===========================

#define SUPABASE_BUCKET "app-files"
#define SUPABASE_OBJECT_PATH "latest.jpg"

// ===========================
//  Tuning
// ===========================
#define XCLK_HZ        10000000   // 10 MHz verified stable on your board; try 20000000 later
#define START_SIZE     FRAMESIZE_VGA   // startup / live-view resolution
#define JPEG_QUALITY   12              // 0 best .. 63 worst (live view)

#define CAPTURE_SIZE     FRAMESIZE_UXGA   // best-quality capture for Supabase uploads
#define CAPTURE_QUALITY  10                // 0 best .. 63 worst (upload)

// ===========================
//  NTP Time Sync — mirrors esp32PlantMonitoring_multiwifi_v3 so both
//  boards upload within moments of each other without talking directly.
// ===========================

const long GMT_OFFSET_SEC      = 8 * 3600;   // Philippines, UTC+8
const int  DAYLIGHT_OFFSET_SEC = 0;

const unsigned long UPLOAD_SLOT_SECONDS = 1800UL;   // 30 minutes
const unsigned long FALLBACK_INTERVAL_MS = UPLOAD_SLOT_SECONDS * 1000UL;

// Sanity threshold for "has NTP actually synced" (~Nov 2023).
const time_t NTP_SANITY_THRESHOLD = 1700000000;

long lastUploadSlot = -1;
unsigned long lastFallbackUpload = 0;

// ===========================
//  AI-Thinker pinout (auto-detected on your board)
// ===========================
#define PWDN_GPIO_NUM   32
#define RESET_GPIO_NUM  -1
#define XCLK_GPIO_NUM    0
#define SIOD_GPIO_NUM   26
#define SIOC_GPIO_NUM   27
#define Y9_GPIO_NUM     35
#define Y8_GPIO_NUM     34
#define Y7_GPIO_NUM     39
#define Y6_GPIO_NUM     36
#define Y5_GPIO_NUM     21
#define Y4_GPIO_NUM     19
#define Y3_GPIO_NUM     18
#define Y2_GPIO_NUM      5
#define VSYNC_GPIO_NUM  25
#define HREF_GPIO_NUM   23
#define PCLK_GPIO_NUM   22
#define LED_GPIO_NUM     4    // onboard white flash LED

#define PART_BOUNDARY "123456789000000000000987654321"
static const char *STREAM_CONTENT_TYPE = "multipart/x-mixed-replace;boundary=" PART_BOUNDARY;
static const char *STREAM_BOUNDARY     = "\r\n--" PART_BOUNDARY "\r\n";
static const char *STREAM_PART         = "Content-Type: image/jpeg\r\nContent-Length: %u\r\n\r\n";

httpd_handle_t camera_httpd = NULL;
httpd_handle_t stream_httpd = NULL;

// ---------------------------------------------------------------
//  Control page
// ---------------------------------------------------------------
static const char PAGE_INDEX[] PROGMEM = R"HTML(
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1">
<title>ESP32-CAM</title><style>
body{font-family:system-ui,sans-serif;background:#111;color:#eee;margin:0;padding:12px;text-align:center}
img{max-width:100%;border-radius:8px;background:#000;margin-top:10px}
button,select{font-size:15px;padding:8px 14px;margin:4px;border-radius:6px;border:1px solid #555;
background:#222;color:#eee}
button:active{background:#444}
.row{margin:8px 0}
label{font-size:14px;margin-right:6px}
</style></head><body>
<h3>ESP32-CAM OV2640</h3>
<div class="row">
<button onclick="go()">Start</button>
<button onclick="stop()">Stop</button>
<button onclick="shot()">Still</button>
</div>
<div class="row">
<label>Resolution</label>
<select id="sz" onchange="setSize()">
<option value="4">QVGA 320x240</option>
<option value="6">VGA 640x480</option>
<option value="8" selected>SVGA 800x600</option>
<option value="9">XGA 1024x768</option>
<option value="11">HD 1280x1024</option>
<option value="13">UXGA 1600x1200</option>
</select>
</div>
<div class="row">
<label>Flash</label>
<input type="range" min="0" max="255" value="0" onchange="led(this.value)">
</div>
<img id="v" src="">
<script>
const v=document.getElementById('v');
function go(){v.src=location.origin+'/stream?'+Date.now();}
function stop(){v.src='';fetch('/stop').catch(()=>{});}
function shot(){v.src=location.origin+'/capture?'+Date.now();}
function setSize(){fetch('/size?v='+document.getElementById('sz').value);}
function led(x){fetch('/led?v='+x);}
window.onload=go;
</script></body></html>
)HTML";

static esp_err_t index_handler(httpd_req_t *req) {
  httpd_resp_set_type(req, "text/html");
  return httpd_resp_send(req, PAGE_INDEX, strlen(PAGE_INDEX));
}

// ---------------------------------------------------------------
//  Single still
// ---------------------------------------------------------------
static esp_err_t capture_handler(httpd_req_t *req) {
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    httpd_resp_send_500(req);
    return ESP_FAIL;
  }
  httpd_resp_set_type(req, "image/jpeg");
  httpd_resp_set_hdr(req, "Content-Disposition", "inline; filename=capture.jpg");
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  esp_err_t res = httpd_resp_send(req, (const char *)fb->buf, fb->len);
  esp_camera_fb_return(fb);
  return res;
}

// ---------------------------------------------------------------
//  MJPEG stream
// ---------------------------------------------------------------
static esp_err_t stream_handler(httpd_req_t *req) {
  camera_fb_t *fb = NULL;
  esp_err_t res   = ESP_OK;
  char part_buf[64];
  uint32_t frames = 0;
  int64_t  t0     = esp_timer_get_time();

  res = httpd_resp_set_type(req, STREAM_CONTENT_TYPE);
  if (res != ESP_OK) return res;
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  httpd_resp_set_hdr(req, "X-Framerate", "60");

  Serial.println("Stream client connected");

  while (true) {
    fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Frame grab failed");
      res = ESP_FAIL;
      break;
    }

    res = httpd_resp_send_chunk(req, STREAM_BOUNDARY, strlen(STREAM_BOUNDARY));
    if (res == ESP_OK) {
      size_t hlen = snprintf(part_buf, sizeof(part_buf), STREAM_PART, fb->len);
      res = httpd_resp_send_chunk(req, part_buf, hlen);
    }
    if (res == ESP_OK) {
      res = httpd_resp_send_chunk(req, (const char *)fb->buf, fb->len);
    }

    esp_camera_fb_return(fb);
    fb = NULL;

    if (res != ESP_OK) break;   // client disconnected

    if (++frames % 30 == 0) {
      int64_t dt = esp_timer_get_time() - t0;
      Serial.printf("Stream: %u frames, %.1f fps, heap %u\n",
                    frames, 30.0f * 1000000.0f / (float)dt, ESP.getFreeHeap());
      t0 = esp_timer_get_time();
    }
  }

  Serial.println("Stream client disconnected");
  return res;
}

// ---------------------------------------------------------------
//  Resolution + LED
// ---------------------------------------------------------------
static int query_int(httpd_req_t *req, const char *key, int def) {
  char buf[64], val[16];
  if (httpd_req_get_url_query_str(req, buf, sizeof(buf)) != ESP_OK) return def;
  if (httpd_query_key_value(buf, key, val, sizeof(val)) != ESP_OK) return def;
  return atoi(val);
}

static esp_err_t size_handler(httpd_req_t *req) {
  int v = query_int(req, "v", 8);
  sensor_t *s = esp_camera_sensor_get();
  if (s) {
    s->set_framesize(s, (framesize_t)v);
    Serial.printf("Framesize set to %d\n", v);
  }
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  return httpd_resp_send(req, "ok", 2);
}

static esp_err_t led_handler(httpd_req_t *req) {
  int v = constrain(query_int(req, "v", 0), 0, 255);
#if ESP_ARDUINO_VERSION_MAJOR >= 3
  ledcAttach(LED_GPIO_NUM, 5000, 8);
  ledcWrite(LED_GPIO_NUM, v);
#else
  ledcSetup(2, 5000, 8);
  ledcAttachPin(LED_GPIO_NUM, 2);
  ledcWrite(2, v);
#endif
  httpd_resp_set_hdr(req, "Access-Control-Allow-Origin", "*");
  return httpd_resp_send(req, "ok", 2);
}

// ---------------------------------------------------------------
//  Server startup — stream lives on its own port/task
// ---------------------------------------------------------------
void startCameraServer() {
  httpd_config_t config = HTTPD_DEFAULT_CONFIG();
  config.server_port    = 80;
  config.ctrl_port      = 32768;
  config.max_uri_handlers = 8;
  config.stack_size     = 8192;

  httpd_uri_t index_uri   = { "/",        HTTP_GET, index_handler,   NULL };
  httpd_uri_t capture_uri = { "/capture", HTTP_GET, capture_handler, NULL };
  httpd_uri_t size_uri    = { "/size",    HTTP_GET, size_handler,    NULL };
  httpd_uri_t led_uri     = { "/led",     HTTP_GET, led_handler,     NULL };
  httpd_uri_t stream_uri  = { "/stream",  HTTP_GET, stream_handler,  NULL };

  if (httpd_start(&camera_httpd, &config) == ESP_OK) {
    httpd_register_uri_handler(camera_httpd, &index_uri);
    httpd_register_uri_handler(camera_httpd, &capture_uri);
    httpd_register_uri_handler(camera_httpd, &size_uri);
    httpd_register_uri_handler(camera_httpd, &led_uri);
    Serial.println("Control server started on port 80");
  }

  // separate server so a blocking stream cannot freeze the control page
  config.server_port = 81;
  config.ctrl_port   = 32769;
  if (httpd_start(&stream_httpd, &config) == ESP_OK) {
    httpd_register_uri_handler(stream_httpd, &stream_uri);
    Serial.println("Stream server started on port 81");
  }
}

// ---------------------------------------------------------------
//  connectWiFi()
//
//  Tries each known network in turn. If none connect, the board keeps
//  running (camera server stays up, capture task keeps retrying on its
//  own schedule) instead of halting — a temporarily unreachable router
//  shouldn't brick the capture loop.
// ---------------------------------------------------------------
void connectWiFi() {
  if (WiFi.status() == WL_CONNECTED) return;

  WiFi.mode(WIFI_STA);
  WiFi.setAutoReconnect(true);
  WiFi.persistent(true);

  Serial.println("Searching for known WiFi...");

  for (int i = 0; i < WIFI_COUNT; i++) {
    Serial.print("Trying: ");
    Serial.println(wifiNetworks[i].ssid);

    WiFi.begin(wifiNetworks[i].ssid, wifiNetworks[i].password);

    unsigned long start = millis();
    while (WiFi.status() != WL_CONNECTED && millis() - start < 10000) {
      delay(500);
      Serial.print(".");
    }
    Serial.println();

    if (WiFi.status() == WL_CONNECTED) {
      Serial.print("Connected to: ");
      Serial.println(wifiNetworks[i].ssid);
      Serial.print("IP: ");
      Serial.println(WiFi.localIP());

      // Sync wall-clock time so uploads land on the same :00/:30
      // boundaries as the sensor board.
      configTime(GMT_OFFSET_SEC, DAYLIGHT_OFFSET_SEC, "pool.ntp.org", "time.google.com");

      return;
    }

    WiFi.disconnect(true, true);
    delay(500);
  }

  Serial.println("No known WiFi available. Running in offline mode.");
}

// ---------------------------------------------------------------
//  dueForUpload() — same NTP-aligned 30-minute scheduler as the
//  sensor board, so both boards upload within moments of each other.
// ---------------------------------------------------------------
bool dueForUpload() {
  time_t now = time(nullptr);

  if (now > NTP_SANITY_THRESHOLD) {
    long slot = now / UPLOAD_SLOT_SECONDS;

    if (slot != lastUploadSlot) {
      lastUploadSlot = slot;
      lastFallbackUpload = millis();
      return true;
    }

    return false;
  }

  if (millis() - lastFallbackUpload >= FALLBACK_INTERVAL_MS) {
    lastFallbackUpload = millis();
    return true;
  }

  return false;
}

// ---------------------------------------------------------------
//  captureAndUpload()
//
//  Grabs one best-quality still and PUTs it to Supabase Storage,
//  overwriting app-files/latest.jpg each time. Temporarily switches
//  the sensor to CAPTURE_SIZE/CAPTURE_QUALITY and restores whatever
//  the live view was using, so a client watching /stream doesn't
//  notice a resolution change.
// ---------------------------------------------------------------
void captureAndUpload() {
  connectWiFi();

  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Capture upload skipped (offline)");
    return;
  }

  sensor_t *s = esp_camera_sensor_get();
  framesize_t previousSize = s ? s->status.framesize : CAPTURE_SIZE;
  int previousQuality = s ? s->status.quality : CAPTURE_QUALITY;

  if (s) {
    s->set_framesize(s, CAPTURE_SIZE);
    s->set_quality(s, CAPTURE_QUALITY);
  }

  camera_fb_t *fb = esp_camera_fb_get();

  if (s) {
    s->set_framesize(s, previousSize);
    s->set_quality(s, previousQuality);
  }

  if (!fb) {
    Serial.println("Capture upload failed: frame grab returned null");
    return;
  }

  HTTPClient http;

  String url = String(SUPABASE_URL) + "/storage/v1/object/" SUPABASE_BUCKET "/" SUPABASE_OBJECT_PATH;
  http.begin(url);

  http.addHeader("apikey", SUPABASE_KEY);
  http.addHeader("Authorization", "Bearer " SUPABASE_KEY);
  http.addHeader("Content-Type", "image/jpeg");
  http.addHeader("x-upsert", "true");

  int httpResponseCode = http.PUT(fb->buf, fb->len);

  Serial.println();
  Serial.println("========== Supabase Image Upload ==========");
  Serial.printf("Frame size    : %u bytes\n", fb->len);
  Serial.print("HTTP Response : ");
  Serial.println(httpResponseCode);
  Serial.println(http.getString());
  Serial.println("============================================");

  http.end();
  esp_camera_fb_return(fb);
}

// ---------------------------------------------------------------
void setup() {
  Serial.begin(115200);
  delay(2000);
  Serial.println("\n\n===== ESP32-CAM WEB STREAMER =====");

  bool hasPsram = psramFound();
  Serial.printf("PSRAM : %s\n", hasPsram ? "found" : "NOT found");

  camera_config_t config = {};
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer   = LEDC_TIMER_0;
  config.pin_d0       = Y2_GPIO_NUM;
  config.pin_d1       = Y3_GPIO_NUM;
  config.pin_d2       = Y4_GPIO_NUM;
  config.pin_d3       = Y5_GPIO_NUM;
  config.pin_d4       = Y6_GPIO_NUM;
  config.pin_d5       = Y7_GPIO_NUM;
  config.pin_d6       = Y8_GPIO_NUM;
  config.pin_d7       = Y9_GPIO_NUM;
  config.pin_xclk     = XCLK_GPIO_NUM;
  config.pin_pclk     = PCLK_GPIO_NUM;
  config.pin_vsync    = VSYNC_GPIO_NUM;
  config.pin_href     = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn     = PWDN_GPIO_NUM;
  config.pin_reset    = RESET_GPIO_NUM;
  config.xclk_freq_hz = XCLK_HZ;
  config.pixel_format = PIXFORMAT_JPEG;
  config.jpeg_quality = JPEG_QUALITY;

  if (hasPsram) {
    config.frame_size  = FRAMESIZE_SVGA;      // buffer size ceiling
    config.fb_count    = 2;
    config.grab_mode   = CAMERA_GRAB_LATEST;
    config.fb_location = CAMERA_FB_IN_PSRAM;
  } else {
    config.frame_size  = FRAMESIZE_QVGA;
    config.fb_count    = 1;
    config.grab_mode   = CAMERA_GRAB_WHEN_EMPTY;
    config.fb_location = CAMERA_FB_IN_DRAM;
  }

  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK) {
    Serial.printf("Camera init FAILED: 0x%02X\n", err);
    while (true) delay(1000);
  }
  Serial.println("Camera init OK");

  sensor_t *s = esp_camera_sensor_get();
  if (s) {
    Serial.printf("Sensor PID: 0x%04X\n", s->id.PID);
    s->set_framesize(s, START_SIZE);
    s->set_brightness(s, 1);
    s->set_saturation(s, 0);
    // s->set_vflip(s, 1);     // uncomment if image is upside down
    // s->set_hmirror(s, 1);   // uncomment if image is mirrored
  }

  // make sure the flash LED starts off
  pinMode(LED_GPIO_NUM, OUTPUT);
  digitalWrite(LED_GPIO_NUM, LOW);

  connectWiFi();

  // Camera server starts regardless of WiFi status — it becomes
  // reachable automatically once WiFi (re)connects, same as the
  // capture-and-upload task below.
  startCameraServer();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.print("  Open http://");
    Serial.print(WiFi.localIP());
    Serial.println("  in your browser");
    Serial.println();
  }
}

void loop() {
  static uint32_t last = 0;
  if (millis() - last > 30000) {
    last = millis();
    Serial.printf("alive — heap %u, wifi %s\n",
                  ESP.getFreeHeap(),
                  WiFi.status() == WL_CONNECTED ? "ok" : "DROPPED");
  }

  if (dueForUpload()) {
    captureAndUpload();
  }

  delay(100);
}
