# Chapter 13 — Secrets and Safety

[← Previous](12-prompting.md) · [Contents](README.md) · [Next: Putting It Online →](14-deploy.md)

---

## Why this chapter is short but not optional

This project's GitHub repository is **public**. Anyone on Earth can read every file in it, right now.

That is a deliberate choice — it lets you show your work, share it with a teacher, and put a link in a presentation. But it means one careless commit publishes your WiFi password to the entire internet permanently.

Not dramatically. Literally. There are automated bots that scan every new public commit on GitHub specifically hunting for API keys. They find them in **minutes**.

---

## What counts as a secret

In this project:

| Secret | If leaked |
|---|---|
| WiFi SSID + password | Someone can join your school's network |
| Supabase URL + key | Someone can read, write, or wipe your data |
| Gemini API key | Someone uses your quota, or runs up charges on your account |

General rule: **if it proves you are you, or gets you into something, it is a secret.**

---

## The solution: separate the values from the code

The idea is simple and it is used by every professional project in the world.

**Code goes in Git. Secret values do not. The code reads the values from somewhere else at runtime.**

```
   ┌─────────────────────┐         ┌──────────────────────┐
   │      YOUR CODE      │         │    YOUR SECRETS      │
   │                     │  reads  │                      │
   │  key = get_secret(  │────────►│  GEMINI_API_KEY=     │
   │      "GEMINI_API_   │         │      AIzaSy...       │
   │       KEY")         │         │                      │
   └─────────────────────┘         └──────────────────────┘
            │                                 │
            ▼                                 ▼
      ✅ goes to GitHub              ❌ NEVER goes to GitHub
```

The code says *"get me the Gemini key."* It does not say what the key is. So the code is safe to publish.

---

## How the web app does it

### The `.env` file

In `plantmonitoring/` there is a file called `.env`:

```
SUPABASE_URL=https://yourproject.supabase.co
SUPABASE_KEY=eyJhbGciOi...
TABLE_NAME=esp32_log
SUPABASE_BUCKET=app-files
GEMINI_API_KEY=AIzaSy...
```

Plain text, one setting per line.

And in `.gitignore`:

```
# Environment Variables
.env
```

Git pretends the file does not exist. It never gets committed, never gets pushed, never appears on GitHub.

### Reading it

Every service reads config through one function in `utils/secrets.py`:

```python
def get_secret(key, default=None):
    try:
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass
    return os.getenv(key, default)
```

Try Streamlit's secrets store first (that is where they live when deployed online), fall back to `.env` / the environment (that is where they live on your laptop).

**One function, two environments, no code changes between them.**

### The bug that made this function necessary

This is a genuinely good story and worth understanding, because it teaches something about reading documentation versus reading reality.

The obvious way to write that would be:

```python
return st.secrets.get(key, default)     # looks fine. is broken.
```

`.get()` with a default is standard Python — if the key is missing, return the default. Safe.

Except **`st.secrets.get()` does not behave that way when there is no secrets file at all.** Instead of returning the default, it raises `StreamlitSecretNotFoundError`.

On your laptop there is no `secrets.toml` — you use `.env`. So that innocent-looking line **crashes every service module the moment it is imported**, and the whole app dies before it renders anything.

Hence the `try / except`. It looks like defensive clutter until you know the story, and then it is obviously necessary.

> **The lesson:** a function behaving unexpectedly at an edge case is extremely common. When something fails in a way that "should not be possible," the answer is usually that a library does something you assumed it did not. Read the actual error, do not assume.

This is recorded in this project's `CLAUDE.md` with a warning not to "simplify" it back. Without that note, someone would eventually tidy it up and break local development for everyone.

---

## How the firmware does it

Same idea, different mechanics.

`secrets.h` — the real file, on your computer only:

```c
#pragma once

WiFiCredential wifiNetworks[] = {
  {"Garden_WiFi", "the-real-password"},
  {"Home_WiFi",   "another-real-password"},
};

#define SUPABASE_URL "https://realproject.supabase.co"
#define SUPABASE_KEY "eyJhbGciOi..."
```

`secrets.h.example` — the committed template:

```c
#pragma once

WiFiCredential wifiNetworks[] = {
  {"YOUR_WIFI_SSID_1", "YOUR_WIFI_PASSWORD_1"},
  {"YOUR_WIFI_SSID_2", "YOUR_WIFI_PASSWORD_2"},
};

#define SUPABASE_URL "https://YOUR_PROJECT_REF.supabase.co"
#define SUPABASE_KEY "YOUR_SUPABASE_PUBLISHABLE_KEY"
```

And in `.gitignore`:

```
firmware/**/secrets.h
```

**Why keep the `.example` file at all?** Because otherwise someone downloading your project has no idea what settings are required. The example shows the exact *shape* — what variables exist, what format they take — with none of the actual values.

Copy it, rename it, fill it in. Standard practice everywhere.

> **Note:** the firmware exists twice in this project — the working copy at the top level, and a mirror inside `plantmonitoring/firmware/` so it is visible on GitHub. Only the `.example` lives in the mirror. The real `secrets.h` stays out of the repo entirely. If you edit the firmware you must copy the `.ino` into the mirror by hand — nothing does it automatically, and this is recorded in `CLAUDE.md` precisely because it is easy to forget.

---

## Rules to actually follow

**1. Never type a real key into a code file.** Not "just for testing." Not "I'll move it later." You will forget, and then you will commit it.

**2. Add to `.gitignore` before creating the secret file.** Order matters. If you create `.env` first and commit before ignoring it, it is already in the history.

**3. Check before every push.**

```
git status
```

Look at the list. If you see `.env` or `secrets.h`, stop and fix `.gitignore`.

**4. If you leak a key, revoke it. Immediately.**

This is the one that surprises people: **deleting the file does not fix it.** Git keeps history. The key is still recoverable from previous commits, and it has already been scraped by bots.

The only real fix:

1. Go to the service (Supabase, Google AI Studio)
2. **Delete / revoke** the exposed key
3. Generate a new one
4. Put the new one in `.env` — which is properly ignored now
5. Change the WiFi password if that is what leaked

It takes five minutes and it is the only thing that actually works. Do not skip it out of embarrassment — every developer has done this at least once.

---

## Secrets when deployed online

When your app runs on Streamlit Community Cloud, there is no `.env` — you did not upload it, correctly.

Instead you paste the values into the platform's **Secrets** settings, in the same format:

```toml
SUPABASE_URL = "https://yourproject.supabase.co"
SUPABASE_KEY = "eyJhbGciOi..."
TABLE_NAME = "esp32_log"
SUPABASE_BUCKET = "app-files"
GEMINI_API_KEY = "AIzaSy..."
```

Streamlit makes those available as `st.secrets`, which `get_secret()` checks first.

Same code, different source, no changes. Chapter 14 walks through it.

---

## One more thing: the "publishable" key

Supabase gives you two kinds of key. The one in this project is the **anon / public / publishable** key — designed to be used from client applications, and safe *only* because Row Level Security limits what it can do.

The other kind — the **service role** key — bypasses all RLS and can do anything to your database.

**Never put a service role key in an app, a firmware file, or anywhere near a browser.** If you ever see instructions telling you to use it to "fix" a permissions problem, the real fix is an RLS policy.

That is one of those distinctions that separates people who understand what they built from people who made the error go away.

---

[← Previous](12-prompting.md) · [Contents](README.md) · [Next: Putting It Online →](14-deploy.md)
