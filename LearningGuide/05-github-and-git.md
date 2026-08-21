# Chapter 05 — Git and GitHub

[← Previous](04-claude-code.md) · [Contents](README.md) · [Next: The Big Picture →](06-the-big-picture.md)

---

## The problem this solves

You have written a school report before. You probably have files like:

```
report.docx
report_final.docx
report_final_v2.docx
report_final_REAL.docx
report_final_REAL_use_this_one.docx
```

Everyone does this. It is a bad system, and you know it is a bad system, because after a week you cannot remember which one is actually current, and if you delete the wrong one you lose work.

**Git is the professional solution to that exact problem.**

With Git you keep **one** file. Git remembers every version of it that ever existed, who changed it, when, and why. You can look at any old version. You can go back to any old version. Nothing is ever lost.

---

## Git and GitHub are different things

People mix these up constantly. Get it straight now:

**Git** is a program on your computer. It tracks changes to files. It works with no internet.

**GitHub** is a website. It stores copies of Git projects online, so you can access them from anywhere and other people can see them.

An analogy: Git is the camera. GitHub is the photo album you share with people.

You can use Git alone forever and never touch GitHub. But GitHub gives you a backup, a way to work from another computer, and a public link you can put in a science fair presentation.

This project's GitHub album is at:

```
https://github.com/nathadegunio/smartplantmonitoring
```

---

## The four words

Git has hundreds of commands. You need four ideas.

### Repository (repo)

A folder that Git is watching. Once a folder is a repo, Git notices every change inside it.

Make one:

```
git init
```

This creates a hidden `.git` folder inside. That hidden folder is Git's memory — every version of everything lives in there. Do not delete it. Do not go poking around inside it.

### Commit

A **commit** is a saved snapshot of your whole project at one moment, with a note explaining what changed.

This is the core idea in Git. Not "save the file" — "save the state of everything, and say why."

Making a commit is two steps:

```
git add .
git commit -m "Add temperature chart to the dashboard"
```

- `git add .` — "include everything that changed" (the `.` means "this folder and everything in it")
- `git commit -m "..."` — "save that snapshot with this message"

**Write real commit messages.** "update" and "fix stuff" are useless to future-you. Look at this project's actual history:

```
Log the actual reason when AI insight generation fails
Show both timestamps + values, and separate photo from analysis in AI insight
Replace ESP32-CAM with in-app browser camera capture
Add 5-minute boot-settle delay before first capture/upload
Add camera integration and Gemini AI plant insights
Fix health.py status logic
Fix timezone conversion and improve chart display
```

Read those in order. You can see the project being built. That is a genuinely useful record — and notice `Replace ESP32-CAM with in-app browser camera capture`, which is the moment a whole approach was abandoned and replaced. Six months later, that message is the only thing that explains why there is no camera board.

### Push

**Push** sends your commits up to GitHub.

```
git push
```

Commits live on your computer until you push. Push regularly — a commit that has not been pushed does not survive a dead laptop.

### Pull

**Pull** brings down changes from GitHub that you do not have yet.

```
git pull
```

You need this when you work on two computers, or with other people.

---

## The rhythm

In practice your day looks like this:

```
   work, work, work
        ↓
   git add .
   git commit -m "what I just did"
        ↓
   work, work, work
        ↓
   git add .
   git commit -m "what I just did"
        ↓
   git push          ← now it is safe on GitHub
```

**Commit often.** After every piece that works. Not once a week.

The reason is not tidiness — it is fear reduction. When your last commit was ten minutes ago, experimenting is free. Break something horribly? Throw it away, go back, lose ten minutes. When your last commit was three days ago, every change feels dangerous, so you stop trying things, and you learn less.

Frequent commits make you braver. That is the actual benefit.

---

## The commands you will use

| Command | What it does |
|---|---|
| `git status` | What has changed since the last commit? **Run this constantly.** |
| `git add .` | Stage all changes for the next commit |
| `git commit -m "message"` | Save a snapshot |
| `git push` | Send commits to GitHub |
| `git pull` | Get commits from GitHub |
| `git log --oneline` | See the history, one line each |
| `git diff` | Show exactly what changed, line by line |

`git status` is the one to build a habit around. Lost? Confused? Not sure what state things are in? `git status`. It tells you where you are and usually suggests what to do next.

---

## .gitignore — the "do not track this" list

Some files should never go into Git:

- **Secrets** — API keys, WiFi passwords
- **Junk** — temporary files Python generates
- **Huge things** — downloaded libraries you can re-download

You list these in a file called `.gitignore`, and Git pretends they do not exist.

Here is the real one from this project:

```
# Python
__pycache__/
*.py[cod]
*.pyo

# Virtual Environment
plantmonitoring/
venv/
.venv/

# Environment Variables
.env

# Firmware secrets (WiFi credentials, API keys) — see secrets.h.example
firmware/**/secrets.h

# Streamlit cache
.streamlit/

# VS Code
.vscode/

# OS Files
.DS_Store
Thumbs.db
```

Look at the two secret lines: `.env` and `firmware/**/secrets.h`. Those two lines are the only thing standing between this public GitHub repository and the whole internet having the WiFi password.

That is not an exaggeration. Chapter 13 covers this properly, but understand now: **`.gitignore` is a security tool, not just a tidiness tool.**

---

## Getting this project onto your own GitHub

Say you want your own copy to work on.

### Option A: Clone it

```
cd Desktop
git clone https://github.com/nathadegunio/smartplantmonitoring.git
cd smartplantmonitoring
```

You now have the whole project plus its entire history.

### Option B: Fork it

On GitHub, click **Fork**. This makes a copy under *your* account that you own and can push to. Then clone your fork.

Fork if you want your own version to develop. Clone if you just want to look.

---

## Connecting a new project to GitHub

When you build your own version from scratch:

1. On GitHub click **New repository**. Give it a name. Do not tick "add a README" — you already have files.
2. GitHub shows you commands. They look like this:

```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

Line by line:

- `git init` — start tracking this folder
- `git add .` — stage everything
- `git commit -m "..."` — first snapshot
- `git branch -M main` — name the main line of development "main"
- `git remote add origin <url>` — remember this GitHub address, call it "origin"
- `git push -u origin main` — send it up

After that first time, it is just `git add .`, `git commit -m "..."`, `git push` forever.

---

## Public vs private

When creating a repo, GitHub asks: public or private?

**Public** — anyone can see your code. Good for a science fair project, a portfolio, showing a teacher.

**Private** — only you and people you invite.

This project is **public**. That is a deliberate choice, and it is exactly why the secrets handling in Chapter 13 matters so much. Public means public. Anyone, forever, including automated bots that scan GitHub specifically looking for leaked API keys. They find them within minutes.

---

## When you are scared to run a Git command

This is common. Git has a reputation for being confusing, and some of its commands genuinely can lose work.

Two rules that will keep you safe:

**1. Commit before you do anything scary.** If your work is committed, almost nothing can destroy it.

**2. Ask before running a command you do not understand.**

> I want to undo my last commit but keep the changes in my files. What command does that, and can it lose my work?

That is a perfectly good use of Claude Code. Ask first, run second. The commands that actually destroy work are few — `git reset --hard`, `git push --force`, `git clean -fd` — and now you know their names.

---

## What is next

You can now save your work permanently and put it online. That is the foundation under everything else.

Time to understand what SmartGrow actually is.

---

[← Previous](04-claude-code.md) · [Contents](README.md) · [Next: The Big Picture →](06-the-big-picture.md)
