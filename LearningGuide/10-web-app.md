# Chapter 10 — The Web App

[← Previous](09-cloud-database.md) · [Contents](README.md) · [Next: The AI Layer →](11-ai-layer.md)

---

## Normally, websites are hard

To build a normal website you need three languages: HTML for structure, CSS for appearance, JavaScript for behavior. Then a server. Then a way to connect the server to the browser. It is weeks of learning before you can show a number on a page.

**Streamlit** removes all of that. You write Python, and Streamlit turns it into a website.

```python
import streamlit as st

st.title("Hello!")
st.write("The temperature is 29.4 degrees.")
```

Run it, and you have a real web page in a browser. No HTML, no CSS, no JavaScript.

That is why this project uses it. The point of the project is the sensing, the cloud, and the AI — not fighting with web layout. Streamlit lets a beginner get a genuinely good-looking dashboard without learning three extra languages.

---

## The thing about Streamlit that confuses everyone

Streamlit has one unusual behavior, and you must understand it or nothing else will make sense.

**Every time anything changes, Streamlit re-runs your entire Python file from the top.**

Click a button? Whole file runs again. Type in a box? Whole file runs again. Auto-refresh timer fires? Whole file runs again.

Coming from normal programming, this feels insane. But it is actually simple to reason about: the page you see is always just *the result of running the script right now*. There is no hidden state to track, no "update this part of the page" logic. Run the script, get the page.

Two consequences you need to remember:

**1. Anything slow gets slow fast.** If your script calls a paid AI on every run, and it re-runs every five minutes forever, that adds up. This is exactly why the AI call is cached — Chapter 11.

**2. Normal variables do not survive.** Set `count = 0` at the top and it resets to 0 on every rerun. To remember something across reruns you use `st.session_state`, which is a box that survives.

You can see this in the camera code:

```python
if photo_id != st.session_state.get("uploaded_photo_id"):
    if upload_plant_image(photo.getvalue()):
        st.session_state["uploaded_photo_id"] = photo_id
```

Why? Because `st.camera_input` keeps handing back the *same* photo on every rerun until the user takes a new one. Without that check, the app would re-upload the identical photo every five minutes forever.

That is a real bug that was found by running the thing and watching the uploads pile up. Now the code remembers which photo it already uploaded and skips it.

---

## Virtual environments

Before running the app you need to understand one Python thing.

Python projects use **libraries** — code other people wrote. This project uses `streamlit`, `pandas`, `supabase`, `plotly`, and more.

Problem: different projects need different versions of the same library. Project A needs pandas 1.5, Project B needs pandas 3.0. Install them globally and they fight.

**A virtual environment is a private box of libraries for one project.** Each project gets its own, they never conflict.

Creating one:

```
python -m venv venv
```

Activating it (Windows PowerShell):

```
venv\Scripts\activate
```

Your prompt changes to show `(venv)`. That means you are inside the box.

Installing this project's libraries:

```
pip install -r requirements.txt
```

`requirements.txt` is a list of every library and its exact version. One command installs all of them, at the right versions.

> **The most common Python error in the world** is `ModuleNotFoundError: No module named 'streamlit'`. It means: you did not activate the virtual environment, or you did not install the requirements. Activate first, then install, then run. That is the order, every time.

---

## Running the app

```
streamlit run main.py
```

Your browser opens automatically. The app is live.

Stop it with **Ctrl + C**. (It runs forever until you do — remember Chapter 02.)

While it is running, edit any file and save. Streamlit notices and offers to rerun. Instant feedback. This tight loop — change, save, look — is the best part of web development, and it is why building the dashboard feels fun compared to flashing firmware.

---

## How main.py is organized

Open it. The whole file is:

```python
# 1. Configure the page
st.set_page_config(page_title="🌱 Smart Plant Monitor", ...)

# 2. Auto-refresh every 5 minutes
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="refresh")

# 3. Get the data
latest = get_latest_record()
history = get_last_n_records(1440)

# 4. Calculate things
online = device_online(latest["time_stamp"])
health = calculate_health(...)
plant_alerts = get_plant_alerts(...)

# 5. Draw the page, top to bottom
show_header(online, health, latest["time_stamp"])
show_plant(plant_alerts)
show_plant_information()
show_health(health)
show_insight(latest, plant_alerts, history)
show_sensor_grid(latest)
show_trends(history)
# ... today's summary ...
show_history(history)
```

**Configure. Refresh. Get data. Calculate. Draw.**

The order of those `show_` calls *is* the order things appear on the page. Want the AI insight above the health bar? Move the line. That is the whole layout system.

> **Why `show_insight` sits exactly there** — after health, before the sensor grid — is a deliberate product decision recorded in this project's `CLAUDE.md`: the AI insight must appear *before* the current environmental conditions. The reasoning is that you want the interpretation first, and the raw numbers as supporting evidence. Most dashboards do the opposite and lead with numbers.

### The auto-refresh

```python
st_autorefresh(interval=REFRESH_SECONDS * 1000, key="refresh")
```

`REFRESH_SECONDS` is 300 — five minutes. It matches the sensor upload rate, and that matching is on purpose. Refreshing every 10 seconds would just fetch the same data 30 times and waste everyone's resources. Refreshing every hour would show stale numbers.

**Match your refresh rate to how fast your data actually changes.** Simple idea, frequently ignored.

---

## The three folders

### services/ — things that know how to do something

No visuals here. Pure logic.

**`database.py`** — talks to Supabase. Every function that fetches sensor data lives here and nowhere else.

**`storage.py`** — uploads and downloads the photo.

**`ai_insights.py`** — talks to Gemini. Chapter 11.

**`health.py`** — the rules. This is the plant knowledge of the whole system:

```python
def get_temperature_status(v):
    if v < 24:
        return "Cold", "#2196F3", 10
    if v <= 32:
        return "Ideal", "#2E7D32", 25
    return "Hot", "#D32F2F", 10
```

Each function returns three things: a label, a color, and a score out of 25. Four sensors × 25 = 100 total health.

```python
def calculate_health(temp, hum, soil, light):
    return (
        get_temperature_status(temp)[2]
        + get_humidity_status(hum)[2]
        + get_soil_status(soil)[2]
        + get_light_status(light)[2]
    )
```

Simple, transparent, and easy to explain to a judge. It is not machine learning. It is four rules added together, and that honesty is a strength — you can defend every point of that score.

`health.py` also holds `plant_advice()`, which produces rule-based text advice. That is the **fallback** used when the AI is unavailable. Remember it — it becomes important in the next chapter.

**`analytics.py`** — the smallest and one of the most useful files:

```python
def sensor_statistics(df, column):
    return {
        "current": round(df[column].iloc[-1], 1),
        "min": round(df[column].min(), 1),
        "max": round(df[column].max(), 1),
        "avg": round(df[column].mean(), 1),
    }
```

Min, max, average, current for any column. Used by the "Today's Summary" cards — and *reused* to build the historical trend that gets sent to the AI. One small function, two purposes. That reuse is deliberate; the summary you see and the trend the AI sees are guaranteed to be the same numbers.

### components/ — things that draw

Each file draws one section. They take data as input and produce visuals.

`insight.py` is the biggest and most interesting — it handles the camera, the upload, the AI call, and the fallback. Chapter 11.

### utils/ — small helpers

**`constants.py`** — settings in one place, so there are no mystery numbers scattered through the code.

**`helpers.py`** — time conversion and formatting. `to_manila()`, `format_timestamp()`, and `time_ago()`, which turns a timestamp into "3 minutes ago." Small human touch, big difference in how a dashboard feels.

**`secrets.py`** — reads API keys. Chapter 13 explains why this file exists at all, and it is a genuinely interesting story.

---

## Two details worth stealing

### Offline detection

```python
def device_online(timestamp):
    return (now - latest) <= timedelta(minutes=15)
```

If the newest reading is more than 15 minutes old, the device is considered offline.

Why 15 and not 5? Because readings arrive every 5 minutes, and one missed upload — a WiFi hiccup — should not make the dashboard scream "OFFLINE." Fifteen minutes means three consecutive failures. That is a real problem, not a blip.

**But note the coupling:** if you ever change the upload interval, you must change this too. Change uploads to every 20 minutes and forget this line, and your dashboard will report the device offline permanently, even though it is working perfectly.

Coupled numbers in different files are a classic source of confusing bugs. This one is at least documented in a comment — which is the minimum you owe the next person.

### Alerts as a list

```python
def get_plant_alerts(temp, humidity, soil, light, online):
    if not online:
        return ["offline"]

    alerts = []
    if temp < 24: alerts.append("cold")
    elif temp > 32: alerts.append("hot")
    # ... and so on ...

    if len(alerts) == 0:
        alerts.append("happy")

    return alerts
```

Two nice touches here.

**Offline short-circuits everything.** If the device is offline, the readings are stale, so reporting "soil is dry" would be dishonest — you do not actually know that. Return offline and nothing else. A system that refuses to claim things it cannot know is a trustworthy system.

**Multiple alerts at once.** It is a list, so the plant can be both hot and dry simultaneously, and both get shown. An earlier version of this project only showed one — the real plant, of course, promptly had two problems at once.

---

## What to do with this chapter

Open the project in VS Code and read these three files, in this order:

1. `main.py` — see the shape
2. `services/health.py` — see the rules
3. `components/sensor_grid.py` — see how one section gets drawn

Then ask Claude Code:

> Read `components/trends.py` and explain how the charts are built. I am a beginner.

You now have the vocabulary to understand the answer. That is the whole point of the last ten chapters.

---

[← Previous](09-cloud-database.md) · [Contents](README.md) · [Next: The AI Layer →](11-ai-layer.md)
