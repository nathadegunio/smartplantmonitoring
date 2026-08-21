# Chapter 14 — Putting It Online

[← Previous](13-secrets-and-safety.md) · [Contents](README.md) · [Next: Build It Yourself →](15-build-it-yourself.md)

---

## The gap between "it works" and "it's real"

Right now the app runs when you type `streamlit run main.py` on your laptop. Close the laptop, it is gone. Nobody else can see it.

**Deploying** means putting it on a computer that is always on, with a public address, so anyone with the link can open it on any device.

This is the step that changes the project from a demo you show to a system that exists.

For a science fair, it is worth doing for one specific reason: **a judge can open it on their own phone, right there.** That lands differently than watching you use your laptop. It stops being a school project and becomes a thing that works.

---

## The platform

**Streamlit Community Cloud** — free, made by the people who make Streamlit, connects directly to GitHub.

The mechanism: it watches your GitHub repository. It reads `requirements.txt`, installs those libraries, and runs `main.py`. **Push a change to GitHub and the live site updates itself within a minute.**

That is your deployment pipeline, and it is free.

---

## Before you start

Three things must be true:

**1. Your code is on GitHub.** All of it that matters, committed and pushed.

**2. `requirements.txt` is accurate.** The cloud machine has no libraries installed — it only installs what is in that file. If something is missing, the app crashes on startup.

Generate it from your working environment:

```
pip freeze > requirements.txt
```

**3. Your secrets are NOT on GitHub.** `.env` must be ignored. You will paste the values into the platform separately.

---

## Deploying, step by step

### 1. Sign in

[share.streamlit.io](https://share.streamlit.io) → sign in with GitHub → authorize it to read your repositories.

### 2. Create the app

Click **New app**, then fill in:

| Field | Value |
|---|---|
| Repository | `your-username/smartplantmonitoring` |
| Branch | `main` |
| Main file path | `main.py` |

If your `main.py` is inside a subfolder, give the full path from the repo root — e.g. `plantmonitoring/main.py`. Getting this wrong is the most common first failure.

### 3. Add your secrets — do this before it runs

Click **Advanced settings** → **Secrets**. Paste in TOML format:

```toml
SUPABASE_URL = "https://yourproject.supabase.co"
SUPABASE_KEY = "eyJhbGciOi..."
TABLE_NAME = "esp32_log"
SUPABASE_BUCKET = "app-files"
GEMINI_API_KEY = "AIzaSy..."
```

Note the differences from `.env`: spaces around the `=`, and **values in quotes**. TOML, not env format. Easy to get wrong.

These are stored by Streamlit and never appear in your repository. This is what `get_secret()` finds first — Chapter 13.

### 4. Deploy

Click **Deploy** and watch the log. It will:

- Clone your repo
- Install every library from `requirements.txt` (this is the slow part, a few minutes)
- Run `main.py`

Then you get a URL like:

```
https://smartplantmonitoring.streamlit.app
```

Open it on your phone. That is your project, live on the internet.

---

## When it fails on the first try

It usually does. Here is what the failures mean.

### `ModuleNotFoundError: No module named 'X'`

`X` is missing from `requirements.txt`. Add it, commit, push. It redeploys automatically.

Most common cause: you installed something with `pip install` while building and never regenerated `requirements.txt`.

### `Missing SUPABASE_URL or SUPABASE_KEY`

The secrets are not set, or a name is misspelled, or you used `.env` format instead of TOML. Check for the quotes.

### `FileNotFoundError` on `main.py`

Wrong main file path. Check whether your file is in a subfolder.

### It loads, but shows "No sensor data available"

The app is fine — it reached Supabase and got nothing back. Either the table is empty, or **RLS is blocking SELECT** (Chapter 09).

### The camera does not work

Browsers only allow camera access over **HTTPS**. Streamlit Cloud gives you HTTPS automatically, so this works when deployed.

Locally, `localhost` is treated as secure so it also works. But if you access your local app by typing your laptop's IP address from your phone, the camera will be blocked. That is a browser security rule, not a bug in your app.

### It worked, then went to sleep

Free apps sleep after a period of no visitors. The first person to open it waits ~30 seconds while it wakes.

**For a presentation: open your app a few minutes beforehand so it is awake.** Then it is instant when a judge opens it. Small thing, saves an awkward silence.

---

## After deployment

Your workflow becomes:

```
   edit code on your laptop
        ↓
   streamlit run main.py       ← test locally
        ↓
   git add . && git commit -m "..."
        ↓
   git push
        ↓
   live site updates in about a minute
```

Test locally, push when it works. Do not debug on the live site.

---

## What is still running on your side

Worth being clear about, because a judge may ask:

- **The web app** — Streamlit Cloud. Always on. ✅
- **The database and photo storage** — Supabase. Always on. ✅
- **The ESP32** — in your garden, plugged in, on your WiFi. ⚠️

That third one is the fragile link. If the ESP32 loses power or WiFi, the dashboard keeps working perfectly — it just shows the last reading it received and, after 15 minutes, marks the device offline.

That behavior is correct and deliberate. **The dashboard tells the truth about what it knows.** It does not pretend the data is current.

Be ready to say that if a judge notices an "offline" badge during your demo. It is not a failure, it is honesty — and honestly, that answer is more impressive than a demo where nothing ever goes wrong.

---

## For your presentation

A few practical notes that are worth more than they look:

**Have the link ready as a QR code.** Judges can scan it and open your project on their own phone in three seconds. This is the single highest-impact five minutes of preparation you can do.

**Open it beforehand** so it is awake.

**Make sure there is recent data.** Have the ESP32 running and uploading, or at minimum have data from earlier that day so the charts are not empty.

**Take a fresh photo right before you present** so the AI insight is current and the timestamps line up. If the photo is stale, the AI will say so — which is a great feature but a confusing thing to demo cold.

**Have a screenshot backup.** Venue WiFi fails. Have images of the working dashboard on your phone and in your slides. Presenting is not the moment to discover the network is down.

---

[← Previous](13-secrets-and-safety.md) · [Contents](README.md) · [Next: Build It Yourself →](15-build-it-yourself.md)
