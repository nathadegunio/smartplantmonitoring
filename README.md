# 🌱 Smart Plant Monitoring System

A real-time IoT-based plant monitoring system for **Sili (Chili Pepper)** that combines an **ESP32**, environmental sensors, **Supabase**, and a **Streamlit** dashboard to help monitor plant health and provide intelligent care recommendations.

---

## 📷 Dashboard Preview

> *Add screenshots of your dashboard here after deployment.*

Example:

```
assets/dashboard.png
```

---

# 📖 Overview

The Smart Plant Monitoring System continuously monitors the environmental conditions of a chili pepper plant and displays the data through a modern, mobile-friendly Streamlit web application.

Sensor readings are collected by an ESP32 every minute and uploaded to Supabase. The dashboard retrieves the latest data, evaluates plant health, displays historical trends, and provides care recommendations based on the current conditions.

---

# ✨ Features

- 🌡 Real-time Temperature Monitoring
- 💧 Humidity Monitoring
- 🌱 Soil Moisture Monitoring
- ☀ Light Intensity Monitoring
- ❤️ Plant Health Score
- 📈 Historical Sensor Trends
- 📊 Daily Statistics
- 📋 Recent Sensor Readings
- 📥 CSV Export
- 🤖 Intelligent Plant Care Recommendations
- 📱 Mobile-Friendly Dashboard
- ☁ Cloud Database using Supabase
- 🚀 Free Deployment using Streamlit Community Cloud

---

# 🛠 Hardware Components

| Component | Description |
|------------|-------------|
| ESP32 | Main Microcontroller |
| DHT22 | Temperature & Humidity Sensor |
| BH1750 | Digital Light Sensor |
| Capacitive Soil Moisture Sensor | Soil Moisture Measurement |
| OLED Display (Optional) | Local Sensor Display |

---

# 💻 Software Stack

- Python
- Streamlit
- Supabase
- Pandas
- Plotly
- GitHub
- Streamlit Community Cloud

---

# 🏗 System Architecture

```
                     🌱 Chili Pepper Plant
                              │
                              │
                  Environmental Conditions
                              │
        ┌─────────────────────────────────────┐
        │                                     │
        │        ESP32 Microcontroller         │
        │                                     │
        ├─────────────────────────────────────┤
        │ DHT22        → Temperature          │
        │ DHT22        → Humidity             │
        │ BH1750       → Light Intensity      │
        │ Soil Sensor  → Soil Moisture        │
        └─────────────────────────────────────┘
                              │
                         WiFi Internet
                              │
                              ▼
                       Supabase Database
                              │
                              ▼
                  Streamlit Web Application
                              │
                              ▼
                  Mobile / Desktop Browser
```

---

# 📁 Project Structure

```
PlantMonitoring/

assets/
│
├── chilli_happy.png
├── chilli_sad.png
└── chilli_sleep.png

components/
│
├── advice.py
├── card.py
├── charts.py
├── header.py
├── health.py
├── history.py
├── plant.py
├── plant_info.py
├── sensor_grid.py
├── stat_card.py
└── trends.py

services/
│
├── analytics.py
├── database.py
└── health.py

utils/
│
├── constants.py
└── helpers.py

.env
.gitignore
main.py
requirements.txt
README.md
```

---

# 🗄 Database

## Table

```
esp32_log
```

| Column | Description |
|----------|-------------|
| id | Primary Key |
| time_stamp | Timestamp |
| temperature_c | Temperature (°C) |
| humidity | Relative Humidity (%) |
| soil_moisture | Soil Moisture (%) |
| light_intensity | Light Intensity (Lux) |

---

# ❤️ Plant Health Calculation

The overall health score is calculated from four environmental parameters.

| Parameter | Weight |
|------------|---------|
| Temperature | 25% |
| Humidity | 25% |
| Soil Moisture | 25% |
| Light | 25% |

Maximum Health Score

```
100%
```

---

# 🌶 Chili Pepper Growing Conditions

## 🌡 Temperature

| Range | Status |
|---------|---------|
| Below 24°C | Cold |
| 24°C–32°C | Ideal |
| Above 32°C | Hot |

Recommendation:

- Move to a warmer location if too cold.
- Provide shade and additional watering if too hot.

---

## 💧 Humidity

| Range | Status |
|---------|---------|
| Below 50% | Low |
| 50–70% | Ideal |
| Above 70% | High |

Recommendation:

- Increase humidity if too low.
- Improve air circulation if too high.

---

## 🌱 Soil Moisture

| Range | Status |
|---------|---------|
| Below 40% | Dry |
| 40–70% | Ideal |
| Above 70% | Wet |

Recommendation:

- Water the plant if dry.
- Avoid watering if already wet.

---

## ☀ Light Intensity

| Range | Status |
|---------|---------|
| Below 10,000 Lux | Low |
| 10,000–50,000 Lux | Ideal |
| Above 50,000 Lux | Very Bright |

Recommendation:

- Move to a brighter location if too dark.
- Provide partial shade during extreme sunlight.

---

# 🌱 Plant State Logic

The dashboard displays different plant images depending on the sensor readings.

Priority:

1. Device Offline
2. Soil Too Dry
3. Temperature Too Hot
4. Light Too Low
5. Healthy Plant

---

# 📊 Dashboard Features

The dashboard includes:

- Device Status
- Plant Health Score
- Plant Image
- Plant Information
- Current Sensor Readings
- Historical Sensor Charts
- Daily Statistics
- Recent Sensor Readings
- CSV Download
- Plant Care Recommendations

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/PlantMonitoring.git

cd PlantMonitoring
```

---

## Create Virtual Environment

Windows

```bash
python -m venv plantmonitoring
```

Activate

```bash
plantmonitoring\Scripts\activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create

```
.env
```

Example

```env
SUPABASE_URL=YOUR_SUPABASE_URL
SUPABASE_KEY=YOUR_SUPABASE_KEY
```

---

## Run Application

```bash
streamlit run main.py
```

---

# ☁ Deploy to Streamlit Community Cloud

1. Push the project to GitHub.
2. Open Streamlit Community Cloud.
3. Connect your GitHub account.
4. Select the repository.
5. Set:

```
Main file:

main.py
```

6. Add the Secrets:

```
SUPABASE_URL

SUPABASE_KEY
```

7. Deploy.

---

# 📈 Future Improvements

- 🌦 Weather API Integration
- 🚿 Automatic Irrigation
- 🔔 Push Notifications
- 📱 Progressive Web App
- 📷 Plant Camera
- 🤖 AI Disease Detection
- 👥 Multi-Plant Support
- 📊 Advanced Analytics
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