# Chapter 11 — The AI Layer

[← Previous](10-web-app.md) · [Contents](README.md) · [Next: Prompting and Context Engineering →](12-prompting.md)

---

**This is the chapter that matters most.**

Everything before this could be built by any competent student with a kit and a tutorial. Sensors sending numbers to a dashboard is a solved problem — you can buy it, and thousands of people have made one.

What is in this chapter is the part that makes SmartGrow an *innovation* rather than an *assembly*. Read it carefully enough to explain it to someone else, because you will need to.

---

## What a Large Language Model is

You have used ChatGPT, or seen someone use it. That is a **Large Language Model** — an LLM. Google's Gemini, which this project uses, is the same kind of thing.

Here is what one actually is, without mysticism:

An LLM is a program that was shown an enormous amount of human writing — books, articles, websites, scientific papers, manuals, forum posts — and learned, in extraordinary statistical detail, how language works and what tends to follow what.

Give it some text, and it produces the text that should come next.

That sounds trivially simple. It is not, and here is why: to reliably produce good text about chili pepper cultivation, a system has to have absorbed something that functions like knowledge of chili pepper cultivation. To answer a question about wilting leaves, it has to have absorbed how people describe wilting leaves and what causes them.

**The result is a program you can talk to about almost anything, that responds with something that reads like informed judgment.**

Whether that constitutes "real" understanding is a genuinely open philosophical question and you should not pretend to settle it. But for your purposes, the practical fact is what matters:

> **You can now write software that reasons about things in plain language — including things you never programmed it to handle.**

That capability did not exist in any usable form before roughly 2022. It is the newest tool in this entire project by a wide margin, and it is available to a high school student in the Philippines for free.

---

## Why this changes what your project is

Sit with this comparison. It is the core of your innovation, and it is the argument you will need to make.

### What every other plant monitor does

```
   IF soil_moisture < 40:
       PRINT "Water the plant."
```

A rule. A human wrote it. It fires when the number crosses a line.

This is what `services/health.py` does, and it is what essentially every IoT plant project ever built does.

It works. It is also fundamentally limited, in a way worth being precise about:

- **It only knows what was programmed.** No rule for a condition, no response to that condition.
- **It cannot see.** Yellow leaves, an insect infestation, a snapped stem, flowers dropping — invisible. Sensors do not measure those.
- **It has no memory of shape.** It knows soil is at 38%. It does not know 38% arrived after a slow three-hour decline versus a sudden drop after someone knocked the sensor loose. Those mean completely different things.
- **It cannot combine.** Hot AND dry AND recently transplanted is a different situation than any one of those alone. Rules fire independently; they do not reason about combinations.
- **It cannot say "I am not sure."** A rule is always confident, even when the data is stale or contradictory.

### What SmartGrow does

Send the LLM:

- **The photo** — what the plant actually looks like right now
- **The current reading** — all four sensors
- **The historical trend** — min, max, average over recent history
- **Both timestamps** — when the photo was taken, when the sensors were read
- **A role and a method** — "you are an expert chili pepper agronomist, here is how to weigh each source"

And get back something like:

> *"The leaves look healthy and upright with good color, and I can see early fruit developing. Soil moisture is at 42% and has been falling steadily from 58% over the past few hours, so the plant is drying out faster than usual — likely from today's high light levels. Temperature and humidity are both comfortable. Water lightly before noon rather than waiting for the reading to drop below 40."*

Look at what that response contains that no rule could produce:

- It **saw** the fruit developing — no sensor measures that
- It noticed a **trajectory**, not just a value
- It **connected** the drying to the high light readings — a causal link across two different sensors
- It gave **timing**, not just an action — before noon
- It recommended acting **before** the threshold, which no threshold-based rule can ever do by definition

That last point is worth stopping on. A rule that fires at 40% cannot warn you at 42%. **The AI is not a better version of the rule. It is a different kind of thing.**

---

## The honest framing for a judge

You should be able to say this clearly, and you should not overstate it:

> **The sensors and dashboard are the standard part. What is new is that the interpretation is done by a large language model — the same class of technology as ChatGPT — instead of by fixed if-then rules.**
>
> **That means the system can respond to situations nobody programmed in advance, combine visual and numerical evidence, reason about trends rather than thresholds, and explain its reasoning in plain language a farmer can act on.**

That is accurate, it does not overclaim, and it is genuinely the interesting part.

---

## What an API call actually is

You know ChatGPT as a website you type into. But there is a second door into the same technology: an **API**.

Same model. Instead of a human typing in a browser, **your program** sends text and gets text back.

That is the bridge that turns "an AI you can chat with" into "an AI that is a component inside your system."

The mechanics, stripped bare:

```
YOUR PROGRAM                                    GOOGLE'S SERVERS
     │                                                 │
     │  1. Build a message:                            │
     │     • the instructions                          │
     │     • the sensor data                           │
     │     • the photo                                 │
     │                                                 │
     │  2. Attach your API key ────────────────────►   │
     │     (proves you are allowed)                    │
     │                                                 │
     │  3. Send it over HTTPS ─────────────────────►   │
     │                                                 │
     │                                            [the model
     │                                             reads and
     │                                             responds]
     │                                                 │
     │  ◄──────────────────── 4. Text comes back       │
     │                                                 │
     │  5. Pull out the text                           │
     │     and show it on screen                       │
     ▼                                                 │
```

Five steps. That is the entire AI integration.

---

## Reading the actual code

Open `services/ai_insights.py`. Here is what matters.

### The configuration

```python
GEMINI_API_KEY = get_secret("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.1-flash-lite"
GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
REQUEST_TIMEOUT = 20
```

**The model choice was deliberate and worth understanding.** `gemini-3.1-flash-lite` was picked over the bigger `gemini-3.6-flash` for a specific reason recorded in this project's notes: the lite model returns `total_thought_tokens: 0`, meaning it does not do extended internal reasoning before answering.

For a hard maths problem you want that extended thinking. For "look at this plant and comment," you do not — it costs more and takes longer for no gain. And this call runs forever, on a free tier, every time the data changes.

**Choosing the smallest model that does the job well is real engineering.** Not everything needs the biggest available thing.

The 20-second timeout matters too: if Google is slow, the app gives up and falls back rather than leaving the user staring at a frozen page.

### The prompt — the most valuable text in this project

```python
CHILLI_EXPERT_PROMPT = """You are an expert agronomist specializing in chilli
pepper (Capsicum annuum / Sili) cultivation in a tropical outdoor Philippine
climate. You are reviewing an automated monitoring snapshot: a photo of the
plant, its current sensor reading, and its recent historical sensor trend.

Ideal ranges for this plant:
- Temperature: 24-32 C
- Humidity: 50-70%
- Soil moisture: 40-70%
- Light: 10,000-50,000 lux

How to use each source — this distinction matters:
- The PHOTO only tells you what the plant looked like at the moment it was
  captured (leaf color, wilting, posture, visible fruit/flowers, pests or
  discoloration). Use it only to describe visual appearance — do not use it
  to judge current environmental conditions, since it may be old.
- The CURRENT sensor reading and the HISTORICAL trend are the actual basis
  for assessing environmental conditions — whether they're improving,
  worsening, or stable — and for the advice you give.

The photo and the sensor reading are captured independently and may not be
from the same moment — the photo is taken manually by the plant's owner
whenever they choose, while the sensor reading comes from an automated
station reporting every 5 minutes. Both timestamps are given below.

Write a short assessment for the plant's owner.

Rules:
- 3 to 5 short sentences, plain language, no markdown, no headers, no bullet points.
- Start with what the photo visually shows (or say no photo is available).
- Then assess current conditions using the sensor reading and how it compares
  to the recent historical trend (e.g. drying out, stable, improving).
- If the photo and sensor timestamps are more than about 15 minutes apart, briefly
  note that the photo may not reflect current conditions.
- End with one concrete, actionable tip.
"""
```

**This block of English is the most important text in the entire project.** Not the Python around it — this.

It is worth understanding *why* each piece is there, because this is where the real skill lives.

**The role.** "Expert agronomist specializing in chilli pepper cultivation in a tropical outdoor Philippine climate." Not "a helpful assistant." Specific expertise, specific crop, specific climate. This shapes everything that follows — the model's answers about a Philippine outdoor chili are different from its answers about a generic houseplant.

**The domain knowledge.** The four ideal ranges are given explicitly, so the model judges against *your* standards, not whatever general figures it might reach for.

**The source separation.** This is the cleverest part. The photo may be old; the sensors are current. So the prompt assigns each source a *different job*: the photo describes appearance only, the sensors judge conditions.

Without this, the model would blend them — and confidently tell you conditions are fine based on a picture from three days ago. **This one instruction is the difference between a system that can be trusted and one that cannot.** It is not a technicality. It is the honesty of the whole product.

**The staleness rule.** If the timestamps are more than ~15 minutes apart, say so. The system flags its own uncertainty. Very few systems do this, and it is exactly what makes users trust one.

**The format rules.** Three to five sentences, plain language, no markdown, end with one action. Without these you get an essay. A farmer looking at a phone needs three sentences and a next step.

### Building the data block

```python
lines = [
    f"Sensor reading taken at: {sensor_timestamp_ph}",
    f"Temperature: {sensor_data.get('temperature_c')} C",
    f"Humidity: {sensor_data.get('humidity')}%",
    f"Soil moisture: {sensor_data.get('soil_moisture')}%",
    f"Light intensity: {sensor_data.get('light_intensity')} lux",
    f"Active alerts: {', '.join(plant_alerts)}",
    "",
    "Recent historical sensor trend:",
]
```

Then min/max/average for each sensor, then the photo timestamp.

Notice: **the data is formatted as clean, labeled, human-readable text.** Not raw JSON, not a database dump. The model reads text, so give it text a person could read. Well-organized input produces well-organized output — this is consistently true.

### Attaching the photo

```python
if image_bytes:
    input_parts.append({
        "type": "image",
        "mime_type": "image/jpeg",
        "data": base64.b64encode(image_bytes).decode("ascii"),
    })
```

**Base64** turns binary image data into plain text characters, because that is what can travel inside a text-based request. The image becomes a very long string of letters and numbers.

This is what makes the model **multimodal** — it takes images and text in the same request and reasons across both. That is a big deal. Five years ago, "look at this photo and combine what you see with these numbers" was a research project.

### Sending it

```python
response = requests.post(
    GEMINI_ENDPOINT,
    headers={
        "Content-Type": "application/json",
        "x-goog-api-key": GEMINI_API_KEY,
    },
    json=payload,
    timeout=REQUEST_TIMEOUT,
)
```

Send a POST request to the URL, with the API key in the headers. Same shape as the ESP32 talking to Supabase. **All APIs work this way.**

---

## The two things that make this production-quality

An AI feature that works when everything is perfect is a demo. These two details make it a product.

### 1. It never breaks the dashboard

```python
if not GEMINI_API_KEY:
    logger.warning("... falling back to rule-based advice.")
    return None
```

And in `components/insight.py`:

```python
insight = generate_plant_insight(...)

if insight:
    return insight, True

fallback = " ".join(plant_advice(...))
return fallback, False
```

If the AI fails **for any reason** — no key, quota exhausted, no internet, Google having a bad day, no photo taken yet — the app falls back to the rule-based advice from `services/health.py` and tells the user honestly:

> *"Rule-based summary (AI insight unavailable right now)."*

**The dashboard never breaks. It just gets less smart.**

Think about what this means for your science fair demo. If the venue WiFi is bad, or you hit a quota limit while presenting, your project does not show an error screen in front of judges. It quietly degrades to rule-based advice and keeps working.

That is graceful degradation again — the same principle as the ESP32 continuing offline. It shows up everywhere in well-built systems.

### 2. It does not waste the free tier

```python
@st.cache_data(ttl=86400, show_spinner=False)
def _cached_insight(sensor_timestamp_key, photo_timestamp_key, ...):
```

Remember from Chapter 10: Streamlit re-runs the entire script on every refresh, every 5 minutes, forever.

Without caching, that is an AI call every 5 minutes — 288 calls a day, 105,000 a year — most of them producing identical output, because most refreshes have no new data.

`@st.cache_data` means: remember the result, keyed on **the sensor timestamp and the photo timestamp**. If neither has changed, do not call Gemini — return the stored answer.

So a fresh call happens **only when there is genuinely something new to say.**

The comment in the code is blunt about it:

> *"Don't remove this caching, it's load-bearing for staying within the free tier."*

**This is a real engineering skill.** Understanding that a thing which works fine once becomes a problem when it runs forever. Cost, quota, and rate limits are constraints you design around, not afterthoughts.

---

## Two ways to be wrong about this

Be careful not to overclaim, and equally careful not to underclaim. Both mistakes will hurt you.

**Do not say:** "We trained our own AI model."

You did not. You used Google's. Training a model requires thousands of computers and millions of dollars. Anyone technical will catch this instantly and stop believing everything else you say.

**Do say:** "We integrated a large language model into an agricultural monitoring system, and engineered the prompt and context that make its output reliable and specific to chili peppers."

That is what you did, it is accurate, and it is genuinely impressive.

**Also do not say:** "It's just an API call, anyone could do it."

The API call is five lines. The **prompt design, the source separation, the trend context, the caching strategy, and the fallback** are the actual work — and they are what make it function rather than merely run.

Anyone can call an API. Making it produce trustworthy, specific, honest output is the part that took thought.

---

## The idea to carry forward

This pattern is not about plants.

**Any system that collects data can now have a layer that interprets that data in plain language.**

Attendance records → "Grade 9-B's absences spike on Mondays after long weekends; three specific students account for most of it."

Water quality sensors → "pH has been drifting down for a week; check the filter before it crosses the safe line."

Fish pond monitors, weather stations, machine sensors, health trackers — same shape. Sense, store, show, **decide**.

You just learned the fourth layer. Almost nobody at your level has.

---

[← Previous](10-web-app.md) · [Contents](README.md) · [Next: Prompting and Context Engineering →](12-prompting.md)
