# Chapter 09 — The Cloud Database

[← Previous](08-firmware.md) · [Contents](README.md) · [Next: The Web App →](10-web-app.md)

---

## What "the cloud" actually means

The cloud is not a metaphor for something mysterious. It means: **somebody else's computer, in a building somewhere, that is always on and always connected to the internet.**

That is genuinely all it is. When your ESP32 "uploads to the cloud," it sends data over the internet to a computer in a data center that Supabase rents. When you open your dashboard, your phone asks that same computer for the data back.

The value is not magic. The value is:

- It is **always on**, so the ESP32 can send data at 3 AM
- It is **reachable from anywhere**, so your phone can get it from another city
- It is **not your problem** — you do not maintain it, back it up, or fix it when it breaks

Twenty years ago you would have needed your own server, a fixed internet connection, and knowledge of system administration to build this project. Now it is a free signup form.

---

## What a database is

A database is a program that stores data in an organized way and answers questions about it quickly.

You already understand the shape of it, because you have used Excel. A database table is a spreadsheet with strict rules:

```
   ┌──────┬─────────────────────┬──────────────┬──────────┬─────────────────┬───────────────┐
   │  id  │     time_stamp      │temperature_c │ humidity │ light_intensity │ soil_moisture │
   ├──────┼─────────────────────┼──────────────┼──────────┼─────────────────┼───────────────┤
   │ 1201 │ 2026-08-21 06:00:00 │     29.4     │   61.0   │      38000      │      55       │
   │ 1202 │ 2026-08-21 06:05:00 │     29.8     │   60.5   │      41000      │      54       │
   │ 1203 │ 2026-08-21 06:10:00 │     30.1     │   59.8   │      43500      │      54       │
   │ 1204 │ 2026-08-21 06:15:00 │     30.6     │   58.9   │      45000      │      53       │
   └──────┴─────────────────────┴──────────────┴──────────┴─────────────────┴───────────────┘
      ↑            ↑                                    ↑
    unique      when it              each reading is one ROW
      id       happened
```

**Table** — the whole grid. This one is called `esp32_log`.

**Column** — a vertical strip. Each column holds one kind of thing, and it has a fixed **type**: `time_stamp` holds dates, `temperature_c` holds decimal numbers. You cannot put the word "hot" in `temperature_c`; the database will refuse. That strictness is a feature — it stops garbage from creeping in.

**Row** — one horizontal record. **One row = one moment in time = one complete sensor reading.**

**Primary key** — the `id`, a unique number for each row so you can refer to exactly one.

### Every reading is a new row

This matters. The ESP32 never updates an existing row. Every five minutes it **adds a new one**.

At one reading every five minutes, that is 288 rows a day, about 105,000 a year. That is a small database by any standard, and it means you have **the complete history**. Nothing is ever overwritten.

That history is what makes the trend charts possible, and it is what lets the AI say "soil moisture has been dropping steadily for three hours" instead of just "soil moisture is 45%." Without stored history there is no trend, and without trend there is no real insight.

---

## Supabase

**Supabase** gives you a PostgreSQL database, plus an API in front of it, plus file storage, plus a web dashboard to look at everything. Free tier, no credit card.

What matters here is that second part. Normally, talking to a database from a program requires a database driver, connection strings, and a query language. Supabase puts a **web API** in front of the database, so anything that can make an HTTP request can use it.

That is precisely why the ESP32 can talk to it. A tiny microcontroller cannot run a Postgres driver. But it can absolutely make an HTTPS request — and that is all Supabase needs.

---

## Setting it up

### Create the project

1. [supabase.com](https://supabase.com) → sign in with GitHub
2. **New Project**. Pick a name, set a database password (save it somewhere), pick the region closest to you — Singapore is the nearest to the Philippines.
3. Wait a couple of minutes while it builds.

### Create the table

**Table Editor → New table.** Name it `esp32_log`. Add these columns:

| Column | Type | Notes |
|---|---|---|
| `id` | `int8` | Created automatically, primary key |
| `time_stamp` | `timestamptz` | Default value: `now()` |
| `temperature_c` | `float8` | Decimal number |
| `humidity` | `float8` | |
| `light_intensity` | `float8` | |
| `soil_moisture` | `float8` | |

Two things worth understanding:

**`timestamptz`** means "timestamp with time zone." Supabase stores every time in **UTC** — the world's reference time zone. The Philippines is UTC+8, so a reading taken at 2:00 PM Manila time is stored as 6:00 AM UTC.

This confuses everyone once. If you look at your raw database and every time is eight hours off, nothing is broken — you are looking at UTC. The web app converts it back to Manila time before showing you anything (that is what `utils/helpers.py` does).

**`now()` as the default** means the database stamps the time itself when a row arrives. The ESP32 does not send a timestamp. Why? Because the database's clock is authoritative and always correct, while the ESP32's clock depends on NTP having worked. Let the reliable clock do it.

### Get your keys

**Settings → API.** Two things:

- **Project URL** — `https://something.supabase.co`
- **anon / public key** — a long string of characters

Both go into your `.env` (for the web app) and your `secrets.h` (for the firmware).

### Create the storage bucket

**Storage → New bucket.** Name it `app-files`. This is where `latest.jpg` lives.

A **bucket** is a folder in the cloud for files that do not fit in a database table — images, PDFs, videos.

---

## Row Level Security — the wall that blocks you first

This one deserves a real explanation, because it will stop you and the error is unhelpful.

Supabase's API is on the public internet. Anyone who knows your URL can send it requests. So by default, Supabase **blocks everything**. New table, no access. Not for you, not for your ESP32, not for anyone.

You then write **policies** saying who can do what. That system is called **Row Level Security (RLS)**.

The four operations:

| Operation | Meaning |
|---|---|
| `SELECT` | Read rows |
| `INSERT` | Add new rows |
| `UPDATE` | Change existing rows |
| `DELETE` | Remove rows |

For this project you need, on the `esp32_log` table:

- **INSERT** — so the ESP32 can add readings
- **SELECT** — so the web app can read them

And on the `app-files` storage bucket:

- **INSERT** and **UPDATE** — so the app can upload and overwrite the photo
- **SELECT** — so the app can list and download it

> **The trap that will get you, documented from this actual project:**
>
> Storage `list()` **succeeds even with no policies at all — as long as the bucket is empty.** An empty list is a perfectly valid answer to "what is in here," so it does not error.
>
> So you test, it works, you move on. Then you upload the first photo, and suddenly reading breaks — because now there *is* something to list, and now the missing SELECT policy actually matters.
>
> Also: marking a bucket **"Public"** in the dashboard is a **completely separate setting** from RLS policies. Public does not substitute for a SELECT policy. Many people assume it does, including for a while on this project.

When something works in the Supabase web dashboard but fails from your code, **suspect RLS first.** The dashboard uses a master key that bypasses all policies. Your app does not.

---

## How the app talks to Supabase

`services/database.py` handles it all. The setup:

```python
from supabase import create_client

SUPABASE_URL = get_secret("SUPABASE_URL")
SUPABASE_KEY = get_secret("SUPABASE_KEY")
TABLE_NAME = get_secret("TABLE_NAME", "esp32_log")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
```

Read the URL and key from secrets, build a client. One connection, used by the whole app.

Then getting the newest reading:

```python
response = (
    supabase.table(TABLE_NAME)
    .select("*")
    .order("time_stamp", desc=True)
    .limit(1)
    .execute()
)
```

Read that as a sentence: *"From the table esp32_log, select all columns, ordered by timestamp newest first, give me just 1, go."*

That is a database query, and you just read it without being taught a query language. It is designed to be readable, and it is.

Getting history is the same with a bigger limit:

```python
.limit(1440)      # about 5 days at one reading every 5 minutes
```

### Everything gets converted to Manila time

Every function in that file passes its result through:

```python
def convert_to_ph_time(df):
    df["time_stamp"] = (
        pd.to_datetime(df["time_stamp"], utc=True, errors="coerce")
        .dt.tz_convert("Asia/Manila")
    )
    return df
```

UTC comes out of the database; Manila time goes into the app. **The conversion happens once, at the boundary**, so no other part of the app ever has to think about time zones.

That is a good pattern in general: handle a messy conversion at the edge of your system, so the inside stays clean.

---

## The photo storage

`services/storage.py` handles the picture, and it is short:

```python
def upload_plant_image(image_bytes):
    supabase.storage.from_(SUPABASE_BUCKET).upload(
        "latest.jpg",
        image_bytes,
        file_options={"content-type": "image/jpeg", "upsert": "true"},
    )
```

`upsert: true` means "if a file with this name already exists, replace it."

**There is exactly one photo. Ever.** Taking a new one destroys the old one. There is no history of photos.

That is a deliberate design decision, not an oversight. The requirement was "show the latest photo," storage is finite, and keeping every photo forever would grow without limit for no benefit.

Design decisions like this are worth being able to defend. If a judge asks *"why don't you keep photo history?"* the answer is: *"we only need the current state, and unbounded storage growth is a real cost."* That is an engineering answer.

### Where does the photo's timestamp come from?

Not the filename — it is always `latest.jpg`. Supabase stores an `updated_at` field on the file itself, so the code lists the bucket and reads it:

```python
entries = supabase.storage.from_(SUPABASE_BUCKET).list()
match = next((e for e in entries if e.get("name") == "latest.jpg"), None)
captured_at = match.get("updated_at") or match.get("created_at")
```

That timestamp is what gets sent to the AI as "photo taken at," and it is why the system can tell you the photo might be stale.

---

## Looking at your data

The Supabase dashboard has a **Table Editor** where you can just look at your rows like a spreadsheet, and a **SQL Editor** where you can ask questions directly:

```sql
select * from esp32_log order by time_stamp desc limit 10;
```

The ten most recent readings.

```sql
select avg(temperature_c) from esp32_log
where time_stamp > now() - interval '1 day';
```

The average temperature over the last day.

You do not need to learn SQL. But knowing you *can* look directly at the data is valuable — when the dashboard shows something strange, checking the raw database tells you instantly whether the problem is in the data or in the display. That single check narrows a bug from "somewhere in the whole system" to "in one half of it."

---

## Common problems

**"Missing SUPABASE_URL or SUPABASE_KEY"** — your `.env` is missing, misspelled, or in the wrong folder.

**Data uploads but the app shows nothing** — RLS. You have INSERT but not SELECT.

**Times are 8 hours off** — you are looking at raw UTC in the dashboard. Expected. The app converts.

**ESP32 says upload failed with 401** — bad or missing API key in `secrets.h`.

**ESP32 says upload failed with 404** — wrong table name, or wrong URL.

**Storage worked, then broke after the first upload** — the empty-bucket RLS trap above.

---

[← Previous](08-firmware.md) · [Contents](README.md) · [Next: The Web App →](10-web-app.md)
