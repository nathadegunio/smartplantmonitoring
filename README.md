# 🌱 Smart Plant Monitoring System

A real-time IoT-based plant monitoring system for **Sili (Chili Pepper)** that combines an **ESP32**, environmental sensors, an **ESP32-CAM**, **Supabase** (database + storage), **Gemini AI**, and a **Streamlit** dashboard to help monitor plant health and provide intelligent care recommendations.

---

# 📖 Overview

The Smart Plant Monitoring System continuously monitors the environmental conditions of a chili pepper plant and displays the data through a modern, mobile-friendly Streamlit web application.

Every 30 minutes, in sync:
- The **ESP32 sensor board** reads temperature, humidity, soil moisture, and light, and uploads them to Supabase.
- The **ESP32-CAM** captures a best-quality still of the plant and uploads it to Supabase Storage.

The dashboard retrieves the latest reading and photo, evaluates plant health, asks **Gemini** (acting as a chilli-pepper cultivation expert) to summarize the plant's current condition from the photo + sensor data, displays historical trends, and provides care recommendations.

---

# ✨ Features

- 🌡 Real-time Temperature Monitoring
- 💧 Humidity Monitoring
- 🌱 Soil Moisture Monitoring
- ☀ Light Intensity Monitoring
- 📷 Live Plant Camera (ESP32-CAM, latest photo every 30 min)
- 🤖 AI Plant Insight — Gemini-generated condition summary from the latest photo + sensor snapshot
- ❤️ Plant Health Score
- 📈 Historical Sensor Trends
- 📊 Daily Statistics
- 📋 Recent Sensor Readings
- 📥 CSV Export
- 🇵🇭 Timestamps shown in Philippine Time (converted from UTC)
- 📱 Mobile-Friendly Dashboard
- ☁ Cloud Database + Storage using Supabase
- 🚀 Free Deployment using Streamlit Community Cloud

---

# 🛠 Hardware Components

| Component | Description |
|------------|-------------|
| ESP32 | Sensor board microcontroller |
| ESP32-CAM (AI-Thinker) | Camera board microcontroller |
| DHT22 | Temperature & Humidity Sensor |
| BH1750 | Digital Light Sensor |
| Capacitive Soil Moisture Sensor | Soil Moisture Measurement |
| OLED Display (SH1106) | Local Sensor Display |

Firmware sketches live in this repo under `firmware/`:
- `firmware/esp32PlantMonitoring_multiwifi_v3/esp32PlantMonitoring_multiwifi_v3.ino` — sensor board
- `firmware/aaESP32CAM_WebStream/aaESP32CAM_WebStream.ino` — camera board (also serves a local live-view web UI on port 80/81 for testing)

Each sketch folder reads its WiFi credentials and Supabase URL/key from a
`secrets.h` file, which is gitignored (same reasoning as `.env` for the web
app — this repo is public). Before opening a sketch in Arduino IDE, copy its
`secrets.h.example` to `secrets.h` in the same folder and fill in your own
values.

---

# 💻 Software Stack

- Python / Streamlit
- Supabase (Postgres database + Storage)
- Google Gemini API (`gemini-3.1-flash-lite`, via the Interactions API)
- Pandas / Plotly
- GitHub / Streamlit Community Cloud

---

# 🏗 System Architecture

```
                         🌱 Chili Pepper Plant
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
          ESP32 (sensors)                 ESP32-CAM (photo)
     DHT22 / BH1750 / Soil Sensor          best-quality JPEG
                  │                               │
                  │  every 30 min, NTP-aligned     │
                  ▼                               ▼
         Supabase: esp32_log table     Supabase Storage: app-files/latest.jpg
                  │                               │
                  └───────────────┬───────────────┘
                                  ▼
                       Streamlit Web Application
                                  │
                        Gemini AI (photo + sensors
                         → plant condition summary)
                                  │
                                  ▼
                       Mobile / Desktop Browser
```

---

# 📁 Project Structure

```
plantmonitoring/

assets/
firmware/
│
├── esp32PlantMonitoring_multiwifi_v3/
│   └── esp32PlantMonitoring_multiwifi_v3.ino    Sensor board
└── aaESP32CAM_WebStream/
    └── aaESP32CAM_WebStream.ino                  Camera board

components/
│
├── card.py
├── charts.py
├── header.py
├── health.py
├── history.py
├── insight.py        AI Plant Insight card (photo + Gemini summary)
├── plant.py
├── plant_info.py
├── sensor_grid.py
├── stat_card.py
└── trends.py

services/
│
├── ai_insights.py     Gemini "Chilli Plant AI Advisor"
├── analytics.py
├── database.py
├── health.py
└── storage.py          Latest camera photo from Supabase Storage

utils/
│
├── constants.py
├── helpers.py
└── secrets.py           Reads Streamlit secrets, falls back to .env

.env
.gitignore
main.py
requirements.txt
README.md
```

---

# 🗄 Database

## Table: `esp32_log`

```sql
DROP TABLE IF EXISTS public.esp32_log CASCADE;

CREATE TABLE public.esp32_log (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    time_stamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    temperature_c REAL,
    humidity REAL,
    light_intensity REAL,
    soil_moisture REAL
);

ALTER TABLE public.esp32_log ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Policy_esp32_log_insert"
ON public.esp32_log FOR INSERT TO anon WITH CHECK (true);

CREATE POLICY "Policy_esp32_log_select"
ON public.esp32_log FOR SELECT TO anon USING (true);
```

| Column | Description |
|----------|-------------|
| id | Primary Key |
| time_stamp | Timestamp (UTC, shown as PH time in the dashboard) |
| temperature_c | Temperature (°C) |
| humidity | Relative Humidity (%) |
| soil_moisture | Soil Moisture (%) |
| light_intensity | Light Intensity (Lux) |

## Storage bucket: `app-files`

The ESP32-CAM overwrites a single object, `latest.jpg`, every 30 minutes — there is no photo history, only the latest capture.

1. In the Supabase dashboard, set the `app-files` bucket to **Public** (so the dashboard can load `latest.jpg` from a plain public URL without signed URLs).
2. Run this in the Supabase SQL editor so the ESP32-CAM's publishable key is allowed to upload/overwrite:

```sql
CREATE POLICY "Policy_app_files_insert"
ON storage.objects FOR INSERT TO anon
WITH CHECK (bucket_id = 'app-files');

CREATE POLICY "Policy_app_files_update"
ON storage.objects FOR UPDATE TO anon
USING (bucket_id = 'app-files');
```

(The UPDATE policy is required because the ESP32-CAM uploads with `x-upsert: true`, overwriting the existing object instead of inserting a new one each cycle.)

---

# 🤖 AI Plant Insight (Gemini)

`services/ai_insights.py` sends the latest photo + latest sensor readings to Gemini (`gemini-3.1-flash-lite`, via the REST **Interactions API**: `POST https://generativelanguage.googleapis.com/v1beta/interactions`), with a fixed "chilli-pepper cultivation expert" instruction prompt. The model returns a short, plain-language condition summary and one actionable tip, shown at the top of the dashboard, before the current environmental conditions.

- Cached for 30 minutes (keyed on the latest reading's timestamp), so Gemini is called once per upload cycle regardless of how many people load the dashboard — this matters for staying within the free tier.
- If Gemini is unavailable (no key, quota exceeded, network error) or no photo has been uploaded yet, the card falls back to the existing rule-based advice in `services/health.py` so the dashboard never breaks.

---

# ❤️ Plant Health Calculation

The overall health score is calculated from four environmental parameters.

| Parameter | Weight |
|------------|---------|
| Temperature | 25% |
| Humidity | 25% |
| Soil Moisture | 25% |
| Light | 25% |

Maximum Health Score: **100%**

---

# 🌶 Chili Pepper Growing Conditions

## 🌡 Temperature

| Range | Status |
|---------|---------|
| Below 24°C | Cold |
| 24°C–32°C | Ideal |
| Above 32°C | Hot |

## 💧 Humidity

| Range | Status |
|---------|---------|
| Below 50% | Low |
| 50–70% | Ideal |
| Above 70% | High |

## 🌱 Soil Moisture

| Range | Status |
|---------|---------|
| Below 40% | Dry |
| 40–70% | Ideal |
| Above 70% | Wet |

## ☀ Light Intensity

| Range | Status |
|---------|---------|
| Below 10,000 Lux | Low |
| 10,000–50,000 Lux | Ideal |
| Above 50,000 Lux | Very Bright |

---

# 📡 Device Online Status

The dashboard considers the device **offline** if no reading has arrived in the last 40 minutes (30-minute upload interval + buffer for a missed cycle).

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/nathadegunio/smartplantmonitoring.git
cd smartplantmonitoring
```

## Create Virtual Environment

Windows

```bash
python -m venv plantmonitoring
plantmonitoring\Scripts\activate
```

## Install Requirements

```bash
pip install -r requirements.txt
```

## Configure Environment Variables

Create `.env`:

```env
SUPABASE_URL=YOUR_SUPABASE_URL
SUPABASE_KEY=YOUR_SUPABASE_KEY
TABLE_NAME=esp32_log
SUPABASE_BUCKET=app-files
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

## Run Application

```bash
streamlit run main.py
```

---

# ☁ Deploy to Streamlit Community Cloud

1. Push the project to GitHub.
2. Open Streamlit Community Cloud → connect your GitHub account → select the repository.
3. Main file: `main.py`
4. Add the Secrets:

```
SUPABASE_URL
SUPABASE_KEY
TABLE_NAME
SUPABASE_BUCKET
GEMINI_API_KEY
```

5. Deploy.

---

# 📈 Future Improvements

- 🚿 Automatic Irrigation
- 🔔 Push Notifications
- 📱 Progressive Web App
- 🤖 AI Disease Detection
- 👥 Multi-Plant Support
- 📅 Growth Timeline

---

# 👨‍💻 Author

**Diether Masangcay**

Bachelor of Science in Information Technology

IoT | Data Analytics | Python | Machine Learning

---

# 📄 License

This project is licensed under the MIT License.

---

⭐ If you found this project helpful, consider giving it a star on GitHub.
