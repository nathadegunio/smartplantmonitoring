# Chapter 16 — When Things Break

[← Previous](15-build-it-yourself.md) · [Contents](README.md) · [Next: Glossary →](17-glossary.md)

---

## The reframe

Things breaking is not a sign that something has gone wrong with your project.

Things breaking **is the project**. It is what building software consists of. Every experienced developer spends more time investigating why something does not work than writing new things.

The difference between someone who can build and someone who cannot is not that one of them gets fewer errors. It is that one of them has a **method** instead of a feeling.

Here is the method.

---

## Step 1 — Read the error. All of it.

The instinct when red text appears is to look away and feel bad. Resist it.

Error messages are written by programmers to tell you what happened. They usually succeed.

```
Traceback (most recent call last):
  File "C:\Users\Nathaniel\Desktop\plant\main.py", line 68, in <module>
    latest["soil_moisture"],
    ~~~~~~^^^^^^^^^^^^^^^^^
KeyError: 'soil_moisture'
```

Beginners see a wall of noise. Read it properly:

- **`File ... main.py`** — which file
- **`line 68`** — which line
- **`latest["soil_moisture"]`** — the exact code that failed
- **`KeyError: 'soil_moisture'`** — what went wrong: there is no key called `soil_moisture`

So: something asked `latest` for `soil_moisture` and it was not there. Which means the database row does not have that column — probably a typo, or the column is named differently in Supabase.

**Read the last line first.** In Python, the bottom line is the actual error. Everything above is the path that led there.

---

## Step 2 — What changed?

If it worked an hour ago and does not now, **something changed.** Software does not rot on its own.

Ask:
- What did I edit last?
- Did I install something?
- Did I change a setting in Supabase or Google?
- Did I move or rename a file?

`git diff` shows you exactly what you changed since your last commit. This is one of the strongest arguments for committing often — the smaller the diff, the shorter the list of suspects.

---

## Step 3 — Where is it actually breaking?

Your system has four layers. **Find the layer before you look for the bug.**

```
   Sensors  →  ESP32  →  Supabase  →  Web App  →  AI
      │          │          │           │         │
      └── check each junction, in order ──────────┘
```

Test each junction:

| Question | How to check |
|---|---|
| Are the sensors reading? | Serial Monitor |
| Is the ESP32 uploading? | Serial Monitor — look for the HTTP response code |
| Is the data in the database? | Supabase Table Editor — just look |
| Is the app fetching it? | Does the dashboard show numbers? |
| Is the AI responding? | Does the insight say "rule-based summary"? |

Whichever one is the first "no" — that is where your bug is. Everything before it is fine, everything after it is downstream noise.

**This one habit will save you more time than any other.** Most wasted debugging hours are spent looking in a layer that was never the problem.

---

## Step 4 — Change one thing

When you finally have a suspect, change **one** thing and test.

If you change five things and it works, you have learned nothing and cannot repeat it. If you change five things and it still fails, you now have five new possible problems.

One change. Test. Next.

---

## The errors you will actually meet

### Python

**`ModuleNotFoundError: No module named 'streamlit'`**
Virtual environment not activated, or requirements not installed. `venv\Scripts\activate`, then `pip install -r requirements.txt`.

**`KeyError: 'something'`**
Asked a dictionary for a key that is not there. Check the spelling against your actual database column names.

**`TypeError: unsupported operand type(s)`**
Doing maths on something that is not a number — often a `None` from a failed lookup, or a string that was never converted.

**`FileNotFoundError`**
Wrong path, or you are running the command from the wrong folder. Check where you are standing (Chapter 02).

### Streamlit

**Page loads then goes blank**
An error occurred mid-render. Look at the terminal where Streamlit is running — the real error is printed there, not in the browser.

**Changes not appearing**
Hard refresh the browser (`Ctrl + Shift + R`), or restart Streamlit.

**Camera not working**
Needs HTTPS. Works on `localhost` and on Streamlit Cloud; blocked if you open your laptop's IP from a phone.

### Supabase

**`Missing SUPABASE_URL or SUPABASE_KEY`**
`.env` missing, in the wrong folder, or a name misspelled.

**Data uploads but the app shows nothing**
RLS. You have INSERT but not SELECT (Chapter 09).

**Works in the Supabase dashboard, fails from code**
Also RLS. The dashboard bypasses policies; your app does not.

**Timestamps 8 hours off**
That is UTC. Expected. The app converts.

### ESP32

**No COM port appears**
Missing USB driver (CP2102 or CH340), or a charge-only cable.

**`Failed to connect to ESP32`**
Hold the BOOT button while the upload starts.

**Compile error about `secrets.h`**
You have not created it. Copy `secrets.h.example`.

**WiFi will not connect**
Check SSID and password character by character. Also: **the ESP32 cannot use 5GHz networks.** It only does 2.4GHz. This catches a lot of people with modern routers that use the same name for both bands.

**Readings jump around wildly**
Loose wire. Push everything in firmly.

**Upload returns 401**
Bad API key. **404** — wrong URL or table name.

### AI

**Always shows "rule-based summary"**
The AI call is failing. Check that `GEMINI_API_KEY` is set. Then look at your terminal — `ai_insights.py` logs the actual reason, including the HTTP status and response body. That log line exists specifically so you are not guessing.

**Response is generic or wrong**
A prompt problem, not a code problem. Chapter 12.

**Quota errors**
Free tier limit reached. Check the caching is working — an uncached call every refresh will burn through a quota fast.

---

## Debugging hardware is different

Software tells you what is wrong. Hardware just silently does nothing.

**Simplify until it works.** Disconnect every sensor but one. Does that one work? Add the next. The moment it breaks, you have found the culprit.

**Suspect the wires first.** Breadboard connections come loose constantly. Before you doubt your code, re-seat every wire.

**Use the I2C scanner.** Ask Claude for one. It lists every I2C device it can see. If your sensor is not on that list, it is a wiring problem — do not touch your code.

**Print everything.** Add `Serial.println()` at each step so you can see how far it gets before something goes wrong.

---

## How to ask for help well

Whether you are asking Claude Code, a teacher, or the internet, a good question contains five things:

1. **What you were trying to do**
2. **What you did** — the exact command or change
3. **What happened** — the complete error, pasted, not summarized
4. **What you expected**
5. **What you already tried**

Compare:

> its not working can you help

versus

> I am trying to display the soil moisture on the dashboard. When I run `streamlit run main.py` I get `KeyError: 'soil_moisture'` at `main.py` line 68. The temperature and humidity display fine. I checked Supabase and the column is there with data. I tried restarting Streamlit. What should I look at?

The second one often gets solved in one reply. And here is the thing people underestimate: **writing that second version frequently solves the problem before you send it.** Forcing yourself to state it precisely reveals the answer surprisingly often. This is real enough that programmers have a name for it — rubber duck debugging — from the practice of explaining your problem out loud to a rubber duck on your desk.

---

## When you are truly stuck

**Take a break.** Not procrastination — a genuine technique. Step away for twenty minutes, or sleep on it. The number of bugs solved in the shower is not a joke.

**Go back to what worked.** `git log`, find the last good commit, look at what changed since.

**Rebuild the smallest version.** Make a new file that does only the broken thing and nothing else. Either it works — and the problem is elsewhere — or it fails, and now you have a tiny, simple case to examine.

**Explain it to someone.** Out loud. Even to nobody.

**Accept a workaround.** Sometimes you cannot fix it today. Find another way, write down what you know, move on. Coming back next week with fresh eyes is legitimate.

---

## The feeling

Being stuck feels bad. It feels like evidence you are not cut out for this.

It is not. It is the normal state of building things.

Every person who has ever built software has sat staring at something that should work and does not, feeling exactly the way you feel. The ones who ended up good at it are simply the ones who kept going.

Your first bug will take three hours. Your hundredth will take three minutes. That is the whole curve.

---

[← Previous](15-build-it-yourself.md) · [Contents](README.md) · [Next: Glossary →](17-glossary.md)
