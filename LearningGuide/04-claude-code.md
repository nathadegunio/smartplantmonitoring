# Chapter 04 — Meeting Claude Code

[← Previous](03-installing-your-tools.md) · [Contents](README.md) · [Next: Git and GitHub →](05-github-and-git.md)

---

## What you are actually working with

Claude Code is an AI that lives in your terminal and can read and write the files in your project.

That second half is what makes it different from a chatbot in a browser. A chatbot can tell you what code to write. Claude Code can:

- Read your actual files
- Create new files
- Edit existing files
- Run commands and read what they printed
- See the error, and fix it

So the conversation is not "explain to me how I would do this." It is **"do this, and let us look at the result together."**

That is a genuinely new kind of tool, and it is the reason a high school student can build a system like SmartGrow. It removes the years of syntax memorization that used to sit between having an idea and having a working thing.

---

## Starting it

Open a terminal **standing in your project folder** (in VS Code: Terminal → New Terminal does this automatically), then:

```
claude
```

You get a prompt. Type in plain English. Press Enter.

To leave: type `/exit`, or press `Ctrl + C` twice.

---

## The loop

Everything you will do with Claude Code is one loop, repeated:

```
        ┌──────────────────────────────┐
        │  1. You describe what you    │
        │     want, in plain English   │
        └──────────────┬───────────────┘
                       ↓
        ┌──────────────────────────────┐
        │  2. Claude reads files,      │
        │     writes code, explains    │
        └──────────────┬───────────────┘
                       ↓
        ┌──────────────────────────────┐
        │  3. YOU RUN IT AND LOOK      │
        │     ← this step is yours     │
        └──────────────┬───────────────┘
                       ↓
              Does it do what
              you actually wanted?
                  ╱          ╲
              No ╱            ╲ Yes
                ↓              ↓
    ┌───────────────────┐   ┌──────────────┐
    │ 4. Describe what  │   │  Next thing  │
    │    is wrong.      │   └──────────────┘
    │    Go to step 2.  │
    └───────────────────┘
```

Step 3 is the one people skip, and skipping it is the single biggest mistake beginners make with AI tools.

Claude is good. It is not perfect. It sometimes builds exactly what you asked for instead of what you meant. It occasionally makes something up. **If you never check, you accumulate broken things you do not understand.**

Running the thing and looking at it is not optional. It is your actual job in this partnership.

---

## Good prompts vs bad prompts

You will get dramatically better results from this tool once you learn to describe things well. This is the real skill — Chapter 12 goes deep on it. Here is the starter version.

### Bad

> make the dashboard better

Better how? Faster? Prettier? More information? Claude will guess, and the guess will probably not be yours.

### Good

> The dashboard currently shows the sensor readings as plain text. Change it so each reading is in its own card with a colored border — green when the value is in the ideal range, red when it is outside. The ideal ranges are already defined in `services/health.py`.

Look at what that second one gives:

- **The current state** — "currently shows plain text"
- **The desired state** — "cards with colored borders"
- **The rule** — green inside range, red outside
- **A pointer to context** — where the ranges already live

That last one is worth its weight in gold. Telling Claude where the relevant existing code is stops it from reinventing something you already have.

### Another pair

**Bad:**
> its broken

**Good:**
> When I run `streamlit run main.py` I get this error:
>
> ```
> KeyError: 'soil_moisture'
> ```
>
> It happens right after the page loads. It worked before I changed `services/database.py`. What is going on?

The second one gives the exact command, the exact error, when it happens, and what changed recently. That is often enough for an instant fix.

**Paste the whole error.** All of it, even the ugly parts. The line numbers and file paths that look like noise to you are the most useful part to Claude.

---

## Ask it to explain things

This is worth its own section because it is the most underused feature.

Claude Code is not only a builder. It is a patient tutor that never gets tired of you and never makes you feel stupid.

Try these, right now, in the project folder:

> Read `services/health.py` and explain what it does. I am a beginner — no jargon, and explain any term you have to use.

> What is a virtual environment and why does Python need one? Explain it like I am 15.

> Walk me through what happens, step by step, from the moment the ESP32 reads the temperature sensor to the moment I see that number on the dashboard.

> I do not understand what an API is. Explain it with an analogy that is not about restaurants.

This is how you turn the finished project into a teacher. You have a working system and an AI that can read it and explain any part on demand. That is a better learning setup than most university courses provide.

Use it constantly. Being confused and asking is not a weakness in this workflow — it *is* the workflow.

---

## Useful things to know

### Slash commands

Type `/` to see commands. The ones you will use:

| Command | What it does |
|---|---|
| `/help` | List everything available |
| `/clear` | Wipe the conversation and start fresh |
| `/init` | Create a `CLAUDE.md` file (see below) |
| `/exit` | Quit |

### `/clear` when you switch tasks

Claude remembers the current conversation. That is usually good — it means it knows what you have been doing.

But when you finish the firmware and move to the web app, all that firmware conversation is now noise. `/clear` gives you a clean slate. Long, meandering conversations produce worse results than short focused ones.

Rule of thumb: **new task, new conversation.**

### Referring to files

Just name them naturally:

> Look at `components/insight.py` and tell me why the photo is uploaded twice.

Claude will go read it. You do not need to paste file contents.

### CLAUDE.md — the memory file

This is important enough that Chapter 12 devotes real space to it, but meet it now.

`CLAUDE.md` is a file in your project folder that Claude reads automatically every time it starts. It is where you write down things you would otherwise have to repeat in every single conversation:

```markdown
# CLAUDE.md

This project monitors a chili pepper plant.

- The web app is Streamlit, in Python. Run it with `streamlit run main.py`
- Sensor data lives in Supabase, table `esp32_log`
- Never put API keys directly in code — they go in `.env`
- The firmware is Arduino C++ for an ESP32

I am a beginner. Explain what you are doing as you go.
```

That last line changes every response you get. Try it.

This project already has a `CLAUDE.md` at the top level. Open it and read it — it is a good example of what a real one looks like after a project has been running for a while. Notice that it records not just *what* the project is, but *why* certain decisions were made. That is the valuable part.

### Permission prompts

Claude will ask before doing anything significant — writing a file, running a command. **Read what it is asking to do before approving.** It is a good habit, and occasionally it will be about to do something you did not intend.

---

## What Claude Code is bad at

An honest list, so you are not surprised:

**It cannot see your hardware.** It cannot tell you that your sensor wire is in the wrong hole. Physical debugging is entirely yours.

**It cannot see your screen.** If the dashboard looks wrong, you have to describe the wrongness in words.

**It sometimes states things confidently that are not true.** Especially about very new tools, or exact details of services that changed recently. If something it says does not match reality, trust reality. Say so, and it will correct itself.

**It does not know your intent.** It knows your words. If those diverge, you get the words.

**It does not know what you have not told it.** If you have a constraint — must be free, must run offline, teacher said it must use this specific sensor — say so up front. Claude cannot infer what is in your head.

---

## The mindset that works

Do not think of this as "the AI builds it for me." That framing leads to a pile of code you cannot explain, which will collapse the first time something breaks — and which you will be humiliated by if a science fair judge asks you a follow-up question.

Think of it as: **you are the architect, Claude is the builder.**

You decide what the building is for, what rooms it has, and whether the finished room is right. Claude lays the bricks quickly and knows every brick technique. Neither of you can produce the building alone.

The architect does not lay bricks. But the architect absolutely understands what the building does and why every room is there.

That is the level of understanding you are aiming for. Not "I could type this code from memory," but "I know exactly what this does, why it is here, and what would break if it were gone."

---

## Practice before moving on

Do these three, actually:

1. Start Claude Code in the SmartGrow project folder. Ask it to explain what the project does overall.
2. Ask it to explain one file you find confusing, in beginner terms.
3. Create a small `CLAUDE.md` in a test folder, put "I am a beginner, explain everything" in it, and notice how the responses change.

---

[← Previous](03-installing-your-tools.md) · [Contents](README.md) · [Next: Git and GitHub →](05-github-and-git.md)
