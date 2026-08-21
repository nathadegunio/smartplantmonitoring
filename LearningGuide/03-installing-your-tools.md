# Chapter 03 — Installing Your Tools

[← Previous](02-the-command-line.md) · [Contents](README.md) · [Next: Meeting Claude Code →](04-claude-code.md)

---

This chapter is a checklist. Work through it top to bottom. After each install there is a **verification step** — a command you run to prove it worked. Do not skip those. Finding out now that Python did not install correctly is a two-minute fix. Finding out in Chapter 15 is an evening lost.

Set aside an hour. Some downloads are large.

---

## The shopping list

| Tool | What it is for |
|---|---|
| **Python** | Runs the web app |
| **VS Code** | Where you read and edit code |
| **Git** | Saves versions of your work |
| **Node.js** | Required to install Claude Code |
| **Claude Code** | Your AI teammate |
| **Arduino IDE** | Programs the ESP32 chip |

Plus three free online accounts:

| Account | For |
|---|---|
| **GitHub** | Storing your code online |
| **Supabase** | Your cloud database |
| **Google AI Studio** | Your Gemini AI key |

---

## 1. Python

**What it is:** The language the web app is written in. Installing Python means installing the interpreter that reads and runs `.py` files.

**Get it:** [python.org/downloads](https://www.python.org/downloads/) → the big yellow "Download Python 3.x" button.

### The critical part

When the installer opens, before clicking Install:

> ## ✅ TICK THE BOX THAT SAYS "Add python.exe to PATH"
>
> It is at the **bottom** of the first installer screen. It is **unticked by default**. It is easy to miss.

If you miss it, `python` will not work in your terminal and you will get "is not recognized." (You now know what that means — Chapter 01, section 5.) The fix is to run the installer again and choose Modify, so it is not fatal. But just tick it.

Then click **Install Now** and wait.

### Verify it

Open a **new** PowerShell window (new is important — PATH changes only apply to windows opened afterward) and run:

```
python --version
```

You want to see something like:

```
Python 3.13.1
```

The exact numbers do not matter as long as it starts with 3.

Also check pip, which is Python's tool for installing add-on libraries:

```
pip --version
```

> **If you see the Microsoft Store open instead:** Windows has fake `python` placeholders that hijack the command. Fix: Windows Settings → Apps → Advanced app settings → App execution aliases → turn **off** the entries for `python.exe` and `python3.exe`. Then open a new terminal and try again.

---

## 2. VS Code

**What it is:** Your text editor. Where you will actually look at the project.

**Get it:** [code.visualstudio.com](https://code.visualstudio.com/) → Download for Windows.

During install, tick these when offered — they make life much nicer:

- ✅ Add "Open with Code" action to file context menu
- ✅ Add "Open with Code" action to directory context menu
- ✅ Add to PATH

### Verify it

Open VS Code. Then:

- **File → Open Folder** → pick your project folder. The whole project appears in a sidebar on the left.
- **Terminal → New Terminal** (or press `` Ctrl + ` `` — the key above Tab). A command line opens *inside* VS Code, already standing in your project folder.

That second one is a genuinely big deal. It means you never have to `cd` to your project again — VS Code puts you there automatically. From here on, "open a terminal" means this.

### Two extensions worth installing

Click the Extensions icon in the left sidebar (four squares), search, install:

- **Python** (by Microsoft) — colors and checks Python code
- **Markdown Preview Enhanced** — lets you read `.md` files like this one nicely formatted, instead of as raw text

---

## 3. Git

**What it is:** The tool that tracks every version of your files, so you can never truly lose work. Chapter 05 explains it properly.

**Get it:** [git-scm.com/downloads](https://git-scm.com/downloads) → Windows.

The installer asks a lot of questions. **Accept every default.** They are all sensible. Just keep clicking Next.

### Verify it

New terminal:

```
git --version
```

You want something like `git version 2.47.1`.

### Tell Git who you are

Do this once, ever. Git stamps your name on every save you make.

```
git config --global user.name "Nathaniel"
git config --global user.email "your-email@example.com"
```

Use the same email you will use for GitHub.

---

## 4. Node.js

**What it is:** A different programming language runtime. You are not going to write any JavaScript — you need it purely because Claude Code is distributed through Node's package installer.

**Get it:** [nodejs.org](https://nodejs.org/) → the **LTS** version (Long Term Support — the stable one).

Accept the defaults through the installer.

### Verify it

New terminal:

```
node --version
npm --version
```

Both should print a version number.

---

## 5. Claude Code

**What it is:** The AI assistant that will do the actual coding with you. This is the important one.

Install it with Node's package manager:

```
npm install -g @anthropic-ai/claude-code
```

The `-g` means "global" — install it for the whole computer, not just one folder.

This takes a minute and prints a lot of text. That is normal.

### Verify it

```
claude --version
```

### First run

Navigate to a folder and start it:

```
cd Desktop
mkdir claude-test
cd claude-test
claude
```

The first time, it opens your browser to log in to your Anthropic account. Follow it through, come back to the terminal.

You should land at a prompt where you can type. Try:

```
Hello! Explain what you are and what you can do for me, in simple terms.
```

Congratulations — that is your teammate. Chapter 04 is entirely about working with it.

Type `/exit` to leave.

---

## 6. Arduino IDE

**What it is:** The program that compiles your firmware and copies it onto the ESP32 chip. You only need this for the hardware half of the project.

**Get it:** [arduino.cc/en/software](https://www.arduino.cc/en/software) → Arduino IDE 2.x for Windows.

### Teaching it about ESP32

The Arduino IDE only knows about Arduino boards out of the box. The ESP32 is made by a different company, so you have to tell it where to find that board's definitions.

1. Open Arduino IDE
2. **File → Preferences**
3. Find the box labeled **Additional boards manager URLs**
4. Paste in:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
5. Click OK
6. In the left sidebar click the **Boards Manager** icon (a chip)
7. Search `esp32`, install **esp32 by Espressif Systems**

This download is big and slow. Let it finish.

### Installing the sensor libraries

A **library** is code someone else wrote so you do not have to. Talking to a DHT22 temperature sensor involves precise electrical timing that would take weeks to figure out — instead, Adafruit wrote a library, and you write `dht.readTemperature()`.

That is not laziness, that is the entire point of software. Nobody rebuilds the bottom layers.

Sidebar → **Library Manager** icon (books) → search and install each of these:

| Library | What it talks to |
|---|---|
| `DHT sensor library` (Adafruit) | Temperature + humidity sensor |
| `Adafruit Unified Sensor` | Required by the DHT library |
| `BH1750` | Light sensor |
| `Adafruit GFX Library` | Drawing shapes and text |
| `Adafruit SH110X` | The little OLED screen |
| `ArduinoJson` | Building the data packet sent to the cloud |

Those six are exactly the libraries this project's firmware imports. If you open the `.ino` file you can see them listed at the top as `#include` lines.

### The driver problem

When you plug in an ESP32 via USB, Windows must recognize it as a serial device. Often it does not, because the ESP32 uses a USB chip Windows does not ship a driver for.

**Symptom:** you plug it in and no COM port appears in Arduino IDE's Tools → Port menu.

**Fix:** install the driver for your board's USB chip. Most ESP32 dev boards use one of two:

- **CP2102** → search "Silicon Labs CP210x VCP driver"
- **CH340** → search "CH340 driver Windows"

If you do not know which, look at the small chip near the USB port on your board — the name is printed on it. Or just install both; they do not conflict.

---

## 7. The three online accounts

All free. Sign up now so they are ready.

### GitHub — [github.com](https://github.com)

Where your code lives online. Free account. Pick a username you would not mind a future employer seeing.

### Supabase — [supabase.com](https://supabase.com)

Your cloud database and file storage. Sign in with your GitHub account — it is faster and one less password. The free tier is generous and this project fits inside it comfortably.

### Google AI Studio — [aistudio.google.com](https://aistudio.google.com)

Where you get the Gemini API key that powers the AI insight. Sign in with a Google account, then look for **Get API key**.

**When it shows you the key: copy it immediately and paste it somewhere safe.** Many services show a key exactly once and never again. If you lose it you have to make a new one.

Chapter 13 covers how to store these safely. For now, just have them.

---

## Final check

Open a fresh terminal and run all of these:

```
python --version
pip --version
git --version
node --version
npm --version
claude --version
```

Six version numbers, no errors.

If any one fails:

1. Did you open a **new** terminal after installing? PATH changes need a fresh window.
2. Did you tick "Add to PATH" during that installer?
3. Ask Claude Code. Genuinely — `claude` then *"I installed Python but `python --version` says it is not recognized. I am on Windows 11. Help me fix this."* It is very good at exactly this.

---

## What you just did

Take a second and notice: you installed a programming language, a code editor, a version control system, a package manager, an AI coding assistant, and an embedded systems toolchain.

Two chapters ago you had never used a terminal.

---

[← Previous](02-the-command-line.md) · [Contents](README.md) · [Next: Meeting Claude Code →](04-claude-code.md)
