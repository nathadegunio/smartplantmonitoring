# Chapter 12 — Prompting and Context Engineering

[← Previous](11-ai-layer.md) · [Contents](README.md) · [Next: Secrets and Safety →](13-secrets-and-safety.md)

---

**If you only master one chapter, make it this one.**

Everything else here is knowledge you could look up. This is a skill — and it is the skill that determines whether you can actually build things, or whether you just have an AI that produces plausible-looking rubbish.

---

## Two kinds of prompting in this project

Do not confuse them. They are related but different.

**1. Prompting Claude Code — to build the project.**
You describing what you want, so working code appears.

**2. The prompt inside the project — the chili expert prompt.**
Instructions written *once*, in code, that run *every time* the app calls Gemini.

Both are "writing instructions for an AI." But the second is harder in an important way: you write it once and it has to work for every future situation you will never see. You cannot clarify. You cannot follow up. It has to be right in advance.

---

## The core principle

> **An AI can only work with what it can see. Your job is to make sure it can see the right things.**

That is it. That is the whole discipline.

When an AI gives you a bad answer, the cause is almost always one of three things:

1. It did not know something it needed
2. It misunderstood what you actually wanted
3. You genuinely did not know what you wanted either

Notice that all three are about **information**, not intelligence. Which means all three are fixable by you.

---

## Part 1 — Prompting Claude Code well

### The four ingredients of a good request

**Context** — what exists now
**Goal** — what you want to exist
**Constraints** — what must or must not be true
**Verification** — how you will know it worked

You do not need all four every time. But when a request goes badly, one of them was missing.

### Watch a prompt get better

**Attempt 1:**
> add charts

Claude will produce *a* chart. Of *something*. Probably not what you meant.

**Attempt 2:**
> add charts to show the sensor data

Better. Still: which sensors? What kind of chart? Over what period? Where on the page?

**Attempt 3:**
> Add a line chart for each of the four sensors showing the last 24 hours.

Good. Now it will build something reasonable.

**Attempt 4:**
> In `components/trends.py`, add a line chart for each of the four sensors (temperature, humidity, soil moisture, light) showing the last 24 hours of data from the `history` dataframe.
>
> Put them in a 2×2 grid. Each chart should have a shaded horizontal band showing that sensor's ideal range — the ranges are already defined in `services/health.py`, reuse them rather than hardcoding.
>
> Match the styling of the existing charts in that file.

That is a professional request. Look at what it does:

- **Names the file** — no guessing
- **Names the data source** — `history`
- **Specifies the layout** — 2×2 grid
- **Adds the interesting feature** — shaded ideal-range bands
- **Points at existing code to reuse** — do not duplicate the ranges
- **Sets a consistency requirement** — match existing style

That last two are what separate beginners from people who get good results. **Telling the AI what already exists prevents it from rebuilding it slightly differently.** Duplicated, slightly-inconsistent code is the most common damage that careless AI use causes to a project.

### Say what you do not want

Constraints are as informative as goals:

> Do not add any new libraries — use what is already in `requirements.txt`.

> Keep this in one file. Do not reorganize the project structure.

> Do not change how the database functions work. Only change the display.

> This runs on a free tier. Do not add anything that makes extra API calls.

Each one closes off a direction you would have had to undo later.

### Describe problems properly

Bad:
> the chart is broken

Good:
> The temperature chart in `components/trends.py` shows a flat line at zero, but `services/database.py` is definitely returning real temperature values — I checked by printing them. This started after I changed the time zone conversion. The chart for humidity works fine.

That second one contains: where, what is wrong, what you already ruled out, when it started, and what still works. **What still works is often the most useful clue of all** — it tells you exactly where the problem is not.

### Ask for explanations as you go

> Add the offline detection, and explain each part as you write it. I want to understand this, not just have it.

This changes the output. You get commented, explained code you can actually defend when questioned.

Do this **always** while learning. The extra thirty seconds of reading is the entire difference between owning your project and hosting it.

### Work in small steps

Do not ask for the whole app at once. You will get a large amount of code you cannot check, and if something is wrong you will not know where.

Ask for one piece. Run it. Confirm it works. Commit it. Next piece.

**If you cannot verify it, it is too big a step.** That rule will serve you for your entire career.

---

## Part 2 — Context engineering

Prompting is what you say. **Context engineering is everything you make available.**

Same request, different context, completely different result.

### CLAUDE.md — persistent context

`CLAUDE.md` is a file Claude Code reads automatically at the start of every conversation. It is where you put the things you would otherwise repeat forever.

A starter one:

```markdown
# CLAUDE.md

## What this is
A chili pepper monitoring system for a school garden project.

## Structure
- `main.py` — Streamlit app, runs top to bottom
- `services/` — logic, no visuals
- `components/` — visuals, no logic
- `utils/` — shared helpers

## How to run
    streamlit run main.py

## Rules
- Never put API keys in code. They go in `.env`, read via `utils/secrets.py`
- All timestamps come from Supabase in UTC and must be converted to Manila time
- Keep the free tier in mind — do not add repeated API calls

## About me
I am a high school student and a beginner. Explain what you are doing as you go.
```

That file makes every future conversation better, permanently.

### Read this project's real CLAUDE.md

Open the `CLAUDE.md` at the top of this project. It is a mature example, and it is worth studying as a document in its own right.

Notice what it records:

- That the top folder is not a git repo, but `plantmonitoring/` is
- That the firmware exists in two places and must be manually kept in sync
- That the older Gemini API is deprecated for this project's key, so use the Interactions API
- **Why** `gemini-3.1-flash-lite` was chosen over `gemini-3.6-flash`
- That the AI caching is "load-bearing for staying within the free tier"
- That the photo and sensor timestamps must stay separate — *"Don't reunify these into a single timestamp — the whole point is that they can diverge"*
- That the Supabase storage `list()` trap exists and how it hides a missing policy

Every one of those is a **hard-won fact**. Something that was discovered by trying, failing, and figuring it out. Without the file, that knowledge dies — and six months later somebody "simplifies" the timestamps back into one and quietly breaks the honesty of the whole system.

> **This is the real lesson: context engineering is not just about the AI. It is about capturing knowledge that is otherwise invisible in code.**
>
> Code shows you *what*. It almost never shows you *why*. `CLAUDE.md` is where the *why* goes.

Write yours as you build. Every time you discover something that surprised you, add a line.

### Give Claude the actual evidence

Do not summarize errors. **Paste them whole.**

Bad:
> it says something about a key error

Good:
```
Traceback (most recent call last):
  File "C:\...\main.py", line 68, in <module>
    latest["soil_moisture"],
KeyError: 'soil_moisture'
```

The file, the line number, the exact key — all of it is signal. What looks like noise to you is the most useful part.

Same for anything else: Serial Monitor output, the JSON a server returned, the actual numbers you are seeing versus the ones you expected.

---

## Part 3 — Writing prompts that live inside your program

This is the harder skill, and it is what makes the AI layer of SmartGrow actually work.

The chili expert prompt runs unattended, forever, on data nobody has seen yet. It has to be right in advance.

Here is what it does, generalized into rules you can reuse.

### Rule 1 — Assign a specific role

Not: *"You are a helpful assistant."*

But: *"You are an expert agronomist specializing in chilli pepper (Capsicum annuum / Sili) cultivation in a tropical outdoor Philippine climate."*

The role sets the vocabulary, the assumptions, and the depth. It is the single highest-leverage sentence in any system prompt.

### Rule 2 — Supply the domain knowledge

Do not assume the model will pick the same standards you use:

```
Ideal ranges for this plant:
- Temperature: 24-32 C
- Humidity: 50-70%
- Soil moisture: 40-70%
- Light: 10,000-50,000 lux
```

Now it judges against *your* thresholds, and its answers agree with your dashboard instead of contradicting it.

### Rule 3 — Tell it how to weigh each input

This is the sophisticated one, and it is what most people miss entirely.

```
- The PHOTO only tells you what the plant looked like at the moment it was
  captured. Use it only to describe visual appearance — do not use it
  to judge current environmental conditions, since it may be old.
- The CURRENT sensor reading and the HISTORICAL trend are the actual basis
  for assessing environmental conditions.
```

When you give a model multiple sources, it will blend them unless told otherwise. If one source is less reliable than another, **you must say so explicitly.**

Ask yourself, every time: *is everything I am sending equally trustworthy?* Usually not. Say which is which.

### Rule 4 — Demand acknowledgment of uncertainty

```
- If the photo and sensor timestamps are more than about 15 minutes apart, briefly
  note that the photo may not reflect current conditions.
```

A system that flags its own limits is one people trust. A system that is always confident is one people stop believing the first time it is confidently wrong.

### Rule 5 — Constrain the output shape

```
- 3 to 5 short sentences, plain language, no markdown, no headers, no bullet points.
- End with one concrete, actionable tip.
```

Without this you get an essay. With it you get something that fits on a phone screen and ends with a next step.

Specify: length, tone, format, and what the last line should be.

### Rule 6 — Provide the trend, not just the value

The prompt receives min/max/average history, not only current readings. That is what enables "drying out faster than usual" instead of "soil is at 42%."

**Context turns a measurement into a meaning.** If you want an AI to reason about change, you must send it the change.

---

## Testing prompts

You cannot know a prompt works by reading it. You have to try it against real situations.

Test with:

- **The normal case** — everything fine
- **One problem** — soil dry
- **Several problems at once** — hot and dry and dim
- **Missing data** — no photo yet
- **Stale data** — photo from yesterday, sensors from now
- **Weird data** — a sensor returning something impossible

Each failure teaches you a line to add. That is exactly where the timestamp-separation rule in this project came from — someone noticed the AI treating an old photo as current, and fixed it in the prompt rather than in code.

> **That is worth its own line: many bugs in AI features are fixed by editing English, not code.** That is a genuinely new kind of debugging, and it is a large part of what "context engineering" means as a job.

---

## The mindset

Think of an AI as **an extremely capable colleague who just walked in and knows nothing about your specific situation.**

They are experienced. They are fast. They are willing.

They have never seen your project, do not know your constraints, do not know what you tried yesterday, and cannot read your mind.

Everything you would tell that person on their first day is what belongs in your prompt and your `CLAUDE.md`.

---

## Practice

Try these in order:

**1.** Ask Claude Code the same question two ways — once vaguely, once with full context — and compare the answers. Actually do this; the difference is startling.

**2.** Write a `CLAUDE.md` for a small project of your own.

**3.** Take the chili expert prompt and rewrite it for a different plant — tomatoes, or kangkong. What changes? What stays? What new instructions does that plant need?

**4.** Deliberately break it. Remove the "3 to 5 sentences" rule and see what happens. Remove the photo/sensor separation and see if the output becomes dishonest.

Number 4 is the most instructive. **Breaking a working thing on purpose teaches you what each part was actually doing.**

---

[← Previous](11-ai-layer.md) · [Contents](README.md) · [Next: Secrets and Safety →](13-secrets-and-safety.md)
