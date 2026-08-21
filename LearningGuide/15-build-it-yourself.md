# Chapter 15 — Build It Yourself

[← Previous](14-deploy.md) · [Contents](README.md) · [Next: When Things Break →](16-when-it-breaks.md)

---

This is the chapter where you stop reading and start building.

Below is the complete path, in order, with the actual prompts to use. Follow it and you will end up with a working system built by you.

**Do not rush it.** Each stage should work before you move to the next. A stage that "mostly works" will haunt you three stages later.

---

## Before you begin: build in the right order

There is a temptation to start with the exciting part — the AI. Do not.

Build in the order the data flows:

```
   STAGE 1        STAGE 2        STAGE 3        STAGE 4        STAGE 5
   ┌───────┐      ┌───────┐      ┌───────┐      ┌───────┐      ┌───────┐
   │Sensors│ ───► │ Cloud │ ───► │  Web  │ ───► │Camera │ ───► │  AI   │
   │ read  │      │ store │      │ shows │      │ photo │      │thinks │
   └───────┘      └───────┘      └───────┘      └───────┘      └───────┘
```

Why this order? **Because each stage gives you something you can see and test.** If you build the AI first you have nothing to feed it, no way to know if it works, and no way to tell whether a failure is in your prompt or your plumbing.

Each stage below ends with a **checkpoint** — a specific thing that must be true before continuing.

---

## Stage 0 — Setup

- [ ] Everything in Chapter 03 installed and verified
- [ ] GitHub, Supabase, Google AI Studio accounts created
- [ ] Hardware in hand: ESP32, DHT22, BH1750, soil sensor, OLED, buzzer, breadboard, jumper wires
- [ ] A project folder created and opened in VS Code

Create your `CLAUDE.md` first, before any code:

> Create a `CLAUDE.md` for a new project. It is a chili pepper monitoring system with an ESP32 sensor board, a Supabase cloud database, a Streamlit web dashboard, and a Gemini AI insight feature. I am a high school student and a beginner — include an instruction that you should explain what you are doing as you go, and never put API keys directly in code.

**Checkpoint:** every command in Chapter 03's final check prints a version number.

---

## Stage 1 — Sensors read

**Goal:** the ESP32 reads all four sensors and prints them to the Serial Monitor. No WiFi, no cloud, nothing else.

Wire everything per Chapter 07. Check every connection twice.

Prompt:

> Write Arduino code for an ESP32 that reads four sensors and prints all values to Serial at 115200 baud every 5 seconds. Nothing else — no WiFi, no display yet.
>
> - DHT22 on GPIO 5 — temperature in Celsius and humidity percent
> - BH1750 light sensor on I2C, SDA GPIO 21, SCL GPIO 22 — lux
> - Capacitive soil moisture sensor on GPIO 34 (analog) — print the raw 0-4095 value for now, I need it to calibrate
>
> Explain each section as you write it. I am a beginner.

Flash it. Open Serial Monitor at 115200.

### Now calibrate the soil sensor

This is the step people skip and then wonder why their readings are nonsense.

1. Hold the probe in **dry air**. Write down the raw number.
2. Put it in **a glass of water** (not past the marked line on the board). Write down that number.

Then:

> My soil sensor reads about 3300 in dry air and about 1150 in water. Add a function that converts the raw reading into a moisture percentage from 0 to 100, where dry air is 0% and water is 100%. Print both the raw value and the percentage.

Use *your* numbers, not those.

**Checkpoint:** all four values print, and they *react correctly*. Breathe on the DHT22 — humidity rises. Cover the BH1750 — lux drops. Move the soil probe from air to water — percentage rises. If any sensor does not respond to the real world, fix it now.

---

## Stage 2 — Cloud storage

**Goal:** readings arrive in Supabase every 5 minutes.

Set up Supabase per Chapter 09: project, `esp32_log` table, RLS policies for INSERT and SELECT, and copy your URL and anon key.

Prompt:

> Add WiFi and Supabase upload to my ESP32 sketch.
>
> - Put the WiFi credentials and Supabase URL/key in a separate `secrets.h` file, and also create a `secrets.h.example` with placeholder values. `secrets.h` must be gitignored.
> - Support a list of multiple WiFi networks, tried in order. If none connect, keep reading sensors and retry next cycle — do not stop or block.
> - Upload all four readings as JSON to the Supabase table `esp32_log`, every 5 minutes.
> - Do not upload a timestamp — the database sets it with a default of `now()`.
> - If the DHT22 returns invalid readings, skip that upload entirely rather than sending bad data.
> - Print to Serial what was sent and what the HTTP response code was.

**Checkpoint:** open Supabase Table Editor. New rows appear every five minutes with sensible values. Unplug the ESP32, plug it back in, confirm it recovers on its own.

---

## Stage 3 — The dashboard

**Goal:** a web page showing the data.

```
python -m venv venv
venv\Scripts\activate
pip install streamlit supabase pandas python-dotenv plotly streamlit-autorefresh
```

Create `.env` with your Supabase values. Add `.env` to `.gitignore` **first**.

Build it in pieces, not all at once.

**3a — Read the data:**

> Create `services/database.py` that connects to Supabase and has two functions: `get_latest_record()` returning the newest row as a dictionary, and `get_last_n_records(limit)` returning recent rows as a pandas DataFrame sorted oldest-first.
>
> Read the URL and key from `.env` — never hardcode them. Supabase stores timestamps in UTC; convert them to Asia/Manila before returning, in one place so the rest of the app never has to think about time zones.

**3b — Show it:**

> Create `main.py` — a Streamlit app that gets the latest record and displays the four sensor values as four metric cards in a 2x2 grid, with the reading time above them.

Run `streamlit run main.py`. **You should now see your plant's data in a browser.** That is a real moment — stop and appreciate it.

**3c — The health rules:**

> Create `services/health.py` with the plant logic. Ideal ranges for chili pepper: temperature 24-32 C, humidity 50-70%, soil moisture 40-70%, light 10,000-50,000 lux.
>
> For each sensor, a function returning a status label, a color, and a score out of 25. Then `calculate_health()` summing them to a score out of 100. Then `get_plant_alerts()` returning a list of active problems — a list, because the plant can have several at once.
>
> Also add `device_online(timestamp)` returning False if the newest reading is more than 15 minutes old, since readings arrive every 5 minutes and one missed upload should not count as offline.

**3d — Charts:**

> Add a `components/trends.py` with a line chart for each sensor over the recent history, in a 2x2 grid, with a shaded band showing the ideal range. Reuse the ranges from `services/health.py` rather than hardcoding them again.

**3e — Auto-refresh:**

> Add auto-refresh every 5 minutes to match the sensor upload rate. Put the interval in a `utils/constants.py` so it is defined in one place.

**Checkpoint:** the dashboard shows live data, a health score, alerts, and charts — and updates on its own.

**Commit and push now.** You have a real working project.

---

## Stage 4 — The camera

**Goal:** capture a photo from the browser and store it.

In Supabase: create the `app-files` bucket, add RLS policies for SELECT, INSERT, and UPDATE.

> Create `services/storage.py` with `upload_plant_image(image_bytes)` that uploads to the Supabase bucket `app-files` as `latest.jpg` with upsert enabled — there is only ever one photo, always overwritten — and `get_latest_plant_image()` that returns the image bytes plus the object's `updated_at` timestamp from `list()`. Both should return None on failure rather than raising, so the dashboard never crashes.
>
> Then create `components/insight.py` that shows `st.camera_input()`, uploads a captured photo, and displays the latest stored photo with its capture time.

Then the bug you will definitely hit:

> The photo re-uploads on every autorefresh because `st.camera_input` keeps returning the same file across reruns. Fix it by tracking the file id in `st.session_state` and only uploading when it changes.

Try it without the fix first, watch the uploads pile up, then apply it. You will remember the lesson far better.

**Checkpoint:** take a photo on your phone through the dashboard. It appears, with a timestamp, and does not re-upload on refresh.

---

## Stage 5 — The AI

**Goal:** the thing that makes this an innovation.

Get your Gemini API key from Google AI Studio, add it to `.env`.

**5a — The call:**

> Create `services/ai_insights.py` that calls the Gemini Interactions API at `https://generativelanguage.googleapis.com/v1beta/interactions` using model `gemini-3.1-flash-lite`, with the API key in an `x-goog-api-key` header and a 20 second timeout.
>
> The function takes the sensor reading, the active alerts, the sensor timestamp, the photo timestamp, the photo bytes, and the historical min/max/avg stats. It sends the photo as a base64 image part plus a text part, and returns the model's text — or None on any failure, so the caller can fall back.

**5b — The prompt.** This is the important part. Write it deliberately:

> Write the expert prompt for that function. It should:
>
> - Set the role as an expert agronomist specializing in chili pepper (Capsicum annuum) in a tropical outdoor Philippine climate
> - State the four ideal ranges explicitly
> - Say clearly that the PHOTO is only for describing visual appearance and must NOT be used to judge current conditions, because it may be old
> - Say that the CURRENT reading and HISTORICAL trend are what determine the environmental assessment
> - Explain that the photo is taken manually whenever the owner chooses while sensors report automatically every 5 minutes, so the two timestamps may differ
> - Require: 3 to 5 short sentences, plain language, no markdown or bullets
> - Require it to start with what the photo shows, then assess conditions using sensors plus trend, and end with one concrete actionable tip
> - Require it to note if the two timestamps are more than about 15 minutes apart

**5c — The fallback:**

> In `components/insight.py`, call the AI. If it returns None for any reason, fall back to the rule-based `plant_advice()` from `services/health.py` and show a small caption saying the summary is rule-based because AI is unavailable. The dashboard must never break because of an AI failure.

**5d — The caching:**

> Cache the AI call with `@st.cache_data`, keyed on the sensor timestamp and the photo timestamp, so a fresh call only happens when one of them actually changes — not on every 5-minute autorefresh. This matters for staying inside the free tier.

**Checkpoint:** the dashboard shows a written assessment that mentions both what the photo shows and what the sensors say. Test the fallback by temporarily removing your API key — the app should degrade, not crash.

---

## Stage 6 — Ship it

- [ ] Push everything to GitHub
- [ ] Confirm `.env` and `secrets.h` are NOT in the repo (`git status`, and look at your repo on GitHub)
- [ ] Deploy per Chapter 14
- [ ] Open it on someone else's phone
- [ ] Update `CLAUDE.md` with everything you learned along the way

---

## Test it properly before you call it done

Do not only test the happy path. Deliberately break things:

| Break this | Expected behavior |
|---|---|
| Unplug the ESP32 | Dashboard shows "offline" after 15 min, does not crash |
| Turn off WiFi at the ESP32 | Keeps reading, keeps showing OLED, retries, uploads when back |
| Remove the Gemini key | Falls back to rule-based advice with a caption |
| Empty database | Clean message, not a crash |
| No photo taken yet | AI says no photo available, still assesses sensors |
| Photo from yesterday | AI notes the photo may be stale |

**A system that handles failure well is worth more than one with extra features.** This table is also, not coincidentally, the list of things a good judge will try to poke at.

---

## Then make it yours

Once it works, change something. This is where it stops being a tutorial and becomes yours.

**Easy:** different plant with different ranges · a light/dark theme · a "days since planted" counter · export data to CSV

**Medium:** email or SMS alert when soil goes dry · a second plant with a second ESP32 · weekly summary from the AI · show sunrise/sunset against the light chart

**Ambitious:** an automatic water pump the dashboard can trigger · ask the AI to predict when watering will next be needed · let the user ask the AI questions about their plant · compare two plants grown under different conditions

That last cluster is where a science fair project becomes a research project.

---

## If you get stuck

Go back to the last thing that worked, and change one thing.

Read the error. All of it.

Ask Claude Code with full context — the error, the file, what you changed, what still works.

Look at the finished project. It is your answer key.

Sleep on it. This genuinely works and nobody knows why.

---

## One last thing

When you finish, you will have built a system that senses the physical world, stores data in the cloud, presents it on the internet, and reasons about it with artificial intelligence.

Most professional software developers have not built something that spans all four of those layers.

You will have, and you will be in high school.

---

[← Previous](14-deploy.md) · [Contents](README.md) · [Next: When Things Break →](16-when-it-breaks.md)
