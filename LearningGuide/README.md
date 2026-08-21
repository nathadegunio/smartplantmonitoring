# SmartGrow — The Build Guide

### For Nathaniel

Hi Nathaniel.

You are holding a working project: a system that watches a chili pepper plant, sends what it sees to the internet, and asks an artificial intelligence what the plant needs. It is real. It runs. People can open it on their phone right now.

This guide exists to answer one question:

> **"Could I have built this myself?"**

The answer is yes. Not "yes, if you study computer science for four years." Yes, **now**, this year, with the tools in this guide.

That is not a motivational slogan. It is a description of how this project was actually made.

---

## Read this part carefully, it matters more than the rest

You probably assume the person who built this knew how to write every line of code in it.

They did not.

This project was built by **describing what it should do, in plain English, to an AI assistant called Claude Code** — and then checking the result, testing it, and asking for changes. Over and over. That is the whole method.

Look at any file in this project. There is Python, there is C++, there is SQL, there are API calls. Nobody sat down and typed all of that from memory. It was *conversed* into existence.

So the skill you need is **not** "memorize programming."

The skill you need is:

1. **Understand what you are building** — the parts, and how they connect.
2. **Describe it clearly** — say what you want precisely enough that a machine can act on it.
3. **Check the result** — run it, look at it, notice when it is wrong.
4. **Say what is wrong** — and go around again.

That loop is the job. This guide teaches you that loop, and gives you just enough understanding of computers, electronics, cloud, and AI to do step 1 and step 3 well.

---

## What you will NOT have to do

Let's take some fear off the table right away. You will **not** need to:

- Memorize programming syntax
- Understand electrical engineering or circuit theory
- Learn database theory
- Do advanced math
- Know what any of the code "means" line by line

You will need to be **curious, patient, and honest about what you don't understand.** That's it. Honestly, that's it.

---

## How to use this guide

**Read it in order.** The chapters are numbered because each one assumes the one before it.

**Don't rush.** If a chapter takes you two days, that is normal and fine.

**Type things yourself.** Do not copy-paste blindly. Typing is slow, and slow is how understanding happens.

**When you get stuck, that IS the lesson.** Getting stuck and unstuck is the actual experience of building software. Everyone who does this gets stuck constantly. The difference between people who build things and people who don't is not that one group gets stuck less — it's that one group keeps going.

---

## The chapters

### Part 1 — Ground floor (start here, skip nothing)

| # | Chapter | What it gives you |
|---|---|---|
| 00 | [Before You Start](00-before-you-start.md) | The mindset. Why you're not too young or too new. |
| 01 | [How Computers Actually Work](01-computer-basics.md) | Files, folders, paths, programs. The vocabulary everything else uses. |
| 02 | [The Command Line](02-the-command-line.md) | The black window with text. Why it exists and why it stops being scary. |
| 03 | [Installing Your Tools](03-installing-your-tools.md) | Python, VS Code, Git, Arduino IDE, Node.js. Step by step. |
| 04 | [Meeting Claude Code](04-claude-code.md) | Your AI teammate. Install it, log in, learn the loop. |
| 05 | [Git and GitHub](05-github-and-git.md) | Saving your work forever, and putting it on the internet. |

### Part 2 — Understanding SmartGrow

| # | Chapter | What it gives you |
|---|---|---|
| 06 | [The Big Picture](06-the-big-picture.md) | The whole system in one diagram. Read this twice. |
| 07 | [Electronics and Sensors](07-electronics-and-sensors.md) | How a plant becomes a number. |
| 08 | [The Firmware](08-firmware.md) | The program living inside the ESP32 chip. |
| 09 | [The Cloud Database](09-cloud-database.md) | Where the numbers go and why they don't disappear. |
| 10 | [The Web App](10-web-app.md) | The dashboard, and why it's split into little files. |
| 11 | [The AI Layer](11-ai-layer.md) | **The heart of the innovation.** What an LLM is and how you talk to one from code. |

### Part 3 — The real skill

| # | Chapter | What it gives you |
|---|---|---|
| 12 | [Prompting and Context Engineering](12-prompting.md) | How to actually direct an AI. The most valuable chapter here. |
| 13 | [Secrets and Safety](13-secrets-and-safety.md) | How not to leak your passwords to the entire internet. |
| 14 | [Putting It Online](14-deploy.md) | Going from "works on my laptop" to "works on anyone's phone." |
| 15 | [Build It Yourself](15-build-it-yourself.md) | The full rebuild plan, with the actual prompts to use. |
| 16 | [When Things Break](16-when-it-breaks.md) | Debugging without panicking. |
| 17 | [Glossary](17-glossary.md) | Every scary word, explained plainly. Keep this open. |

---

## One promise

By the end of Chapter 15 you will have rebuilt this project — or something like it — with your own hands and your own words.

And then the interesting part starts, because you will realize the method works for *anything*. A different plant. A fish tank. An attendance system. A weather station for your barangay. The system you learn here is a shape you can pour any idea into.

Welcome. Start with [Chapter 00](00-before-you-start.md).
