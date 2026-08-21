# Chapter 06 — The Big Picture

[← Previous](05-github-and-git.md) · [Contents](README.md) · [Next: Electronics and Sensors →](07-electronics-and-sensors.md)

---

**Read this chapter twice.** Once now, once after you finish Chapter 11. It is the map that every other chapter is a close-up of.

---

## The whole system in one diagram

```
                        THE PLANT
                     (a chili pepper)
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
   ┌────▼─────┐      ┌──────▼──────┐     ┌──────▼──────┐
   │  DHT22   │      │   BH1750    │     │    Soil     │
   │  temp +  │      │    light    │     │  moisture   │
   │ humidity │      │   sensor    │     │   probe     │
   └────┬─────┘      └──────┬──────┘     └──────┬──────┘
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │  wires
                    ┌───────▼────────┐
                    │     ESP32      │  ← a tiny computer
                    │   (the board)  │     with WiFi built in
                    └───────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
        ┌─────▼─────┐ ┌─────▼─────┐      │
        │   OLED    │ │  Buzzer   │      │  every 5 minutes,
        │  screen   │ │  (beeps)  │      │  over WiFi
        └───────────┘ └───────────┘      │
         shows numbers  warns if bad     │
         on the spot                     │
                                         ▼
                            ╔════════════════════════╗
                            ║       SUPABASE         ║
                            ║   (the cloud)          ║
                            ║                        ║
                            ║  ┌──────────────────┐  ║
                            ║  │ table: esp32_log │  ║
                            ║  │ every reading    │  ║
                            ║  │ ever taken       │  ║
                            ║  └──────────────────┘  ║
                            ║  ┌──────────────────┐  ║
                            ║  │ bucket:app-files │  ║
                            ║  │ latest.jpg       │  ║
                            ║  │ (newest photo)   │  ║
                            ║  └──────────────────┘  ║
                            ╚═══════┬────────▲═══════╝
                                    │        │
                            reads   │        │  writes the photo
                            data    │        │
                                    ▼        │
                       ┌─────────────────────┴──────┐
                       │      THE WEB APP           │
                       │   (Streamlit, Python)      │
                       │                            │
                       │  • charts and history      │
                       │  • health score            │
                       │  • alerts                  │
                       │  • camera → takes photo    │
                       └────────────┬───────────────┘
                                    │
                        sends photo + numbers
                        + recent trend
                                    │
                                    ▼
                       ┌────────────────────────────┐
                       │     GOOGLE GEMINI          │
                       │   (the AI / LLM)           │
                       │                            │
                       │  "You are an expert chili  │
                       │   pepper agronomist..."    │
                       └────────────┬───────────────┘
                                    │
                          a written assessment
                          in plain language
                                    │
                                    ▼
                       ┌────────────────────────────┐
                       │     NATHANIEL'S PHONE      │
                       │                            │
                       │  "The leaves look healthy  │
                       │   but soil moisture has    │
                       │   dropped steadily over    │
                       │   the last 3 hours.        │
                       │   Water before noon."      │
                       └────────────────────────────┘
```

---

## The four layers

Every part of this system belongs to one of four layers. If you remember nothing else from this chapter, remember these four words and what each does.

### Layer 1 — SENSE (the hardware)

**Job:** turn physical reality into numbers.

The plant is warm, the air is humid, the soil is damp, the sun is bright. None of that is data yet. The sensors convert each of those physical facts into a number a computer can hold.

**Lives in:** `esp32PlantMonitoring_multiwifi_v3/` — the firmware, running on the chip in your garden.

**Covered in:** Chapters 07 and 08.

### Layer 2 — STORE (the cloud)

**Job:** remember everything, forever, from anywhere.

A number the ESP32 is holding in its memory disappears the moment power is lost. To be useful it must go somewhere permanent, and somewhere reachable from a phone across town.

**Lives in:** Supabase — a database table for the readings, a storage bucket for the photo.

**Covered in:** Chapter 09.

### Layer 3 — SHOW (the web app)

**Job:** turn numbers into something a human can understand at a glance.

`27.4` means nothing on its own. A green card saying "Temperature — Ideal" and a line chart showing it has been steady all day means something.

**Lives in:** `main.py`, `components/`, `services/`.

**Covered in:** Chapter 10.

### Layer 4 — DECIDE (the AI)

**Job:** turn understanding into a recommendation.

This is the layer that makes SmartGrow different from every other IoT plant monitor, and it is the reason the project is an innovation rather than an exercise.

**Lives in:** `services/ai_insights.py`.

**Covered in:** Chapter 11.

---

## Follow one reading through the whole system

This is the most useful thing in this chapter. Trace it slowly.

**It is 2:00 PM. The ESP32 wakes up.**

**1.** The firmware asks the DHT22: what is the temperature? The sensor answers `31.2`. It asks about humidity: `58.0`. It asks the BH1750 about light: `42000` lux. It reads the soil probe, gets a raw electrical value of `2100`, and converts that to `52` percent using a calibration formula.

**2.** The firmware checks those against the ideal ranges it knows for chili peppers. Temperature 24–32, humidity 50–70, soil 40–70, light 10,000–50,000. All four are inside. No buzzer.

**3.** It prints them to the little OLED screen so anyone standing next to the plant can see them.

**4.** It packages the four numbers into a small text format called JSON:

```json
{
  "temperature_c": 31.2,
  "humidity": 58.0,
  "light_intensity": 42000,
  "soil_moisture": 52
}
```

**5.** It sends that over WiFi to Supabase's API. Supabase adds a timestamp and files it as a **new row** in the `esp32_log` table. Nothing is overwritten — the 1:55 PM reading is still there, and so is every reading from every day since the project started.

**6.** Meanwhile, Nathaniel opens the dashboard on his phone.

**7.** The web app asks Supabase for the newest row, and for the last 1,440 rows (that is five days of history at one reading every five minutes).

**8.** It calculates a health score, decides which alerts are active, draws the charts, and fills in the cards.

**9.** Nathaniel points his phone camera at the plant and taps capture. That photo goes up to the Supabase storage bucket as `latest.jpg`, replacing whatever was there before.

**10.** The app bundles together: the photo, the current reading, the recent min/max/average of each sensor, both timestamps, and a long instruction block that says *"you are an expert chili pepper agronomist, here is how to interpret this."* All of that goes to Google Gemini.

**11.** Gemini reads it — the picture and the numbers together — and writes back three to five sentences of plain language.

**12.** That text appears on the phone.

---

## Two things about that flow that are easy to miss

### The photo and the sensors are completely independent

The sensors report every five minutes automatically, forever, whether anyone is watching or not.

The photo is taken by a person, whenever they feel like it. It could be from thirty seconds ago or from last Tuesday.

These two never coordinate. They do not know about each other.

That is why the system carries **two separate timestamps** all the way through, and why the AI is explicitly told: *use the photo only to describe what the plant looked like, and use the sensors to judge conditions — and if the two timestamps are more than fifteen minutes apart, mention that the photo might be stale.*

That is a small design decision, and it is the difference between an honest system and one that confidently tells you your plant looks fine based on a week-old picture.

### Analysis lives in the app, not on the chip

The ESP32 uploads **raw numbers only**. No health score, no advice.

Why? Because the chip is tiny and slow, and because rules change. If you decide chili peppers actually prefer 25–33 degrees instead of 24–32, changing that in the web app takes ten seconds. Changing it on the chip means recompiling firmware, walking out to the garden, unplugging it, connecting a laptop, and re-flashing.

**Keep the smart parts where they are easy to change.** That is a real engineering principle and you just learned it from a plant.

---

## Why split the web app into so many files?

Open the project and you see a lot of small files:

```
main.py                      ← the conductor
components/
    header.py                ← draws the top bar
    plant.py                 ← draws the plant status
    health.py                ← draws the health bar
    insight.py               ← draws the AI section + camera
    sensor_grid.py           ← draws the four sensor cards
    trends.py                ← draws the charts
    history.py               ← draws the data table
services/
    database.py              ← talks to Supabase
    storage.py               ← handles the photo
    ai_insights.py           ← talks to Gemini
    health.py                ← the ideal-range rules
    analytics.py             ← min / max / average
utils/
    secrets.py               ← reads API keys safely
    helpers.py               ← time conversion, formatting
    constants.py             ← settings in one place
```

This could all be one giant file. It would even work. But:

**You can find things.** Something wrong with the charts? `components/trends.py`. You do not read 2,000 lines hunting.

**You can change one thing safely.** Editing how charts look cannot possibly break how the database works, because they are not in the same room.

**You can describe things precisely to Claude.** *"In `components/trends.py`, change the line color"* is unambiguous.

Notice the pattern in the folder names:

- **`services/`** — things that *know how to do something* (talk to a database, call an AI, calculate a score). No visuals.
- **`components/`** — things that *draw something on screen*. They ask services for data; they do not fetch it themselves.
- **`utils/`** — small helpers used everywhere.
- **`main.py`** — the conductor. It calls services to get data, then calls components in order to draw the page.

That separation — **logic apart from appearance** — is one of the most reliably useful ideas in all of software. You will see it in every serious project you ever encounter.

---

## Read main.py right now

Seriously, open `main.py`. It is under 200 lines and most of them are comments.

You will find that you can basically *read* it, even without knowing Python:

```python
latest = get_latest_record()
history = get_last_n_records(1440)

online = device_online(latest["time_stamp"])
health = calculate_health(...)
plant_alerts = get_plant_alerts(...)

show_header(online, health, latest["time_stamp"])
show_plant(plant_alerts)
show_plant_information()
show_health(health)
show_insight(latest, plant_alerts, history)
show_sensor_grid(latest)
show_trends(history)
```

Get the latest reading. Get the history. Work out if the device is online, how healthy the plant is, what alerts are active. Then draw each section of the page in order.

**That is the entire app.** Everything else is detail hidden inside those function names.

This is what good architecture buys you: the top level of the program reads like a description of what it does. If you can achieve that in your own projects, you are doing well.

---

## The test

You understand this chapter when you can answer these without looking:

1. What are the four layers, and what does each one do?
2. Where do the sensor readings physically live after the ESP32 sends them?
3. Why does the ESP32 not calculate the health score itself?
4. Why does the system track two different timestamps?
5. What is the difference between `services/` and `components/`?

If you can explain all five to another person, you understand this system better than most people who will see it at the science fair.

---

[← Previous](05-github-and-git.md) · [Contents](README.md) · [Next: Electronics and Sensors →](07-electronics-and-sensors.md)
