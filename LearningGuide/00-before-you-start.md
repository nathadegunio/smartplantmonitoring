# Chapter 00 — Before You Start

[← Back to contents](README.md) · [Next: How Computers Actually Work →](01-computer-basics.md)

---

## The lie you might already believe

There is a story people tell about programmers. In the story, they are geniuses. They stare at black screens full of green symbols and understand all of it. They started coding at age six. Their brains work differently from yours.

It is a lie. A useful lie, for the people it flatters, but a lie.

Here is what building software actually looks like:

- You want something to happen.
- You describe it.
- It doesn't work.
- You look at *why* it doesn't work.
- You change one thing.
- Repeat 40 times.
- It works.
- You feel like a god for about ten minutes.
- You want the next thing.

That's the job. Every single person doing this, at every level, is doing that loop. The experienced ones just go around the loop faster and panic less.

---

## What actually changed recently

For most of computing history, step 2 — "describe it" — had to be done in a programming language. That's why it took years to learn: before you could build anything, you had to become fluent in an extremely picky artificial language where a missing semicolon breaks everything.

That barrier is gone.

You can now describe what you want **in English** to an AI that writes the picky language for you. Tools like **Claude Code** do this. You say:

> "Read the temperature from the sensor every five minutes and save it to the database."

And working code appears.

This is not cheating. This is a change in what the job *is* — the same way that calculators didn't end mathematics, they just moved the interesting part somewhere else.

The interesting part is now: **knowing what to ask for, and knowing whether you got it.**

---

## So what do you actually need to learn?

Three things, in this order of importance:

### 1. Architecture — how systems fit together

You need to know that SmartGrow has four parts: a sensor board, a cloud database, a web dashboard, and an AI. You need to know what each one does and how they hand things to each other.

You do **not** need to know how any of them work internally. You need to know the *shape*.

Think of it like a school. You know there's an office, classrooms, a canteen, a clinic. You know a sick student goes classroom → clinic. You don't need to know how the clinic's medicine cabinet is organized to understand the school.

### 2. Vocabulary — enough words to describe a problem

If you can't say "the API call is failing" you'll say "the thing is broken," and nobody — human or AI — can help you with "the thing is broken."

Half of this guide is honestly just vocabulary. That's not filler. Vocabulary is power here.

### 3. The loop — describe, check, correct

This is the skill. Chapter 12 is entirely about it. Everything else is setup.

---

## What you honestly don't need

Let me be very specific, so you can stop worrying about these:

| You do NOT need | Why not |
|---|---|
| To memorize Python syntax | Claude writes it. You read it. Reading is far easier than writing. |
| To understand electronics theory | You need to know which wire goes in which hole. That's a diagram, not a theory. |
| To know math beyond high school | There is no advanced math in this project. Averages. That's it. |
| A powerful computer | Any laptop that runs a browser runs all of this. |
| To be "good at computers" | You need to be *willing to look at computers*. Different thing. |

---

## The three habits that will decide whether you succeed

I want to be honest with you rather than encouraging, because honest is more useful.

**Habit 1: Read the error message.**

When something breaks, the computer usually tells you exactly what's wrong. Beginners panic and don't read it. The message looks scary — lots of red text, file paths, line numbers. But somewhere in it there is one line of plain English that says what happened. Find that line. Read it. Ninety percent of the time it tells you the answer.

**Habit 2: Change one thing at a time.**

When you're stuck and you change five things at once and it works, you have learned nothing, and you cannot repeat it. Change one thing. Test. Change the next thing.

**Habit 3: Say "I don't understand this" out loud.**

To Claude, to a teacher, to yourself in a notebook. The instinct is to nod and hope it becomes clear later. It won't. Naming your confusion is how you fix it.

Literally type this to Claude Code: *"I don't understand what a virtual environment is. Explain it to me like I'm 15 and have never used a command line."* It will. And it won't judge you, ever, no matter how many times you ask.

---

## About the fact that this project already exists

You have been handed a finished project. That is a strange gift — it can feel like being handed a finished painting and told "now learn to paint."

Use it this way instead: **the finished project is your answer key.**

When you build your own version and get stuck, the working version is sitting right there. You can look at how it was solved. You can ask Claude "the existing project does X here, explain why."

Most people learning this have no answer key. You do. That's a real advantage — use it.

---

## A realistic timeline

If you work on this a few hours a week:

- **Week 1–2:** Chapters 00–05. Tools installed, command line no longer scary, first conversation with Claude Code.
- **Week 3:** Chapters 06–11. You understand the system. You can explain it to someone else — which is the actual test.
- **Week 4–6:** Chapters 12–15. You build it.
- **After that:** You build something that isn't this.

If it takes longer, it takes longer. Nobody is timing you.

---

## One last thing

At some point in this process you are going to hit a wall that feels personal. You'll be three hours into an error you can't fix and you'll think: *maybe I'm just not smart enough for this.*

Everyone thinks that. Everyone. The people who build things are simply the ones who came back the next day.

That's the whole secret. Come back the next day.

---

[← Back to contents](README.md) · [Next: How Computers Actually Work →](01-computer-basics.md)
