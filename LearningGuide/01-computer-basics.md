# Chapter 01 — How Computers Actually Work

[← Previous](00-before-you-start.md) · [Contents](README.md) · [Next: The Command Line →](02-the-command-line.md)

---

You already use a computer. You open Chrome, you type in Word, you save a file to the Desktop. That is real computer use and it counts.

But there is a layer underneath that you have never had to look at, and everything in this project lives in that layer. This chapter takes you down one floor.

---

## 1. A computer only does one thing

A computer stores numbers, and follows instructions about those numbers. That is the entire machine.

Everything else — a photo, a song, a chili plant's temperature, this sentence — is numbers with an agreement about what the numbers mean. A photo is a long list of numbers where every three numbers mean "the redness, greenness, and blueness of one dot." Change the agreement, and the same numbers become a song.

Why does this matter to you? Because when your soil sensor reads the dirt, it produces **a number**. Not "wet." A number, like 2400. Somebody had to decide that 2400 means "reasonably damp." That decision is called *calibration*, and you will meet it in Chapter 07.

The computer does not know what wet means. **Meaning is always something a human added.** Hold onto that idea — it comes back in a big way when we get to the AI chapter.

---

## 2. Files and folders — the precise version

You know files and folders from Windows Explorer. Let us make it exact.

**A file** is a named box of numbers sitting on your disk.

**A folder** (also called a **directory**) is a box that holds files and other folders.

**A path** is the full address of a file — the directions from the top of the disk down to the file itself.

```
C:\Users\Nathaniel\Desktop\PlantMonitoring2\plantmonitoring\main.py
│  │     │         │       │                │               │
│  │     │         │       │                │               └─ the file
│  │     │         │       │                └─ a folder
│  │     │         │       └─ a folder
│  │     │         └─ a folder
│  │     └─ your user folder
│  └─ a folder
└─ the drive
```

Read that top to bottom: *"On drive C, in Users, in Nathaniel, on the Desktop, in PlantMonitoring2, in plantmonitoring, there is a file called main.py."*

That is all a path is. An address, written with backslashes instead of commas.

> **Windows quirk:** Windows uses backslashes `\`. Almost everything else in the world — the internet, Python, Mac, Linux — uses forward slashes `/`. You will see both. They mean the same thing. Do not let it confuse you.

**Try it right now:** open any folder in Windows Explorer and click once on the address bar at the top. It turns into the text path. That is the same address — you just never looked at it as text before.

---

## 3. File extensions — the part after the dot

In `main.py`, the `.py` is the **extension**. It is a label telling you and the computer what kind of file this is.

You will meet these in this project:

| Extension | What it is |
|---|---|
| `.py` | Python code — the web app |
| `.ino` | Arduino code — the program for the ESP32 chip |
| `.h` | A C++ header file — in this project, where the secret passwords live |
| `.md` | Markdown — formatted text. This guide is made of `.md` files. |
| `.json` | Structured data that programs pass to each other |
| `.txt` | Plain text, no formatting |
| `.jpg` | A photo |
| `.env` | Settings and secrets for the web app |

Here is the important part: **all of these are just text files** except `.jpg`. You can open `main.py` in Notepad and read it. It is not encrypted, not compiled, not magic. It is text that happens to follow rules.

> **Do this now, it is genuinely worth it:** Windows hides extensions by default, which is confusing and unhelpful. Open Windows Explorer → **View** menu → **Show** → tick **File name extensions**. Now you can always see what kind of file you are looking at.

---

## 4. What a program actually is

A program is a text file full of instructions, plus something that reads those instructions and carries them out.

There are two ways this happens.

**Interpreted** — a second program reads your file line by line and performs each instruction as it goes. Python works this way. `main.py` is just text until you run `python main.py`, and then the Python interpreter reads it and acts.

**Compiled** — your text file gets translated ahead of time into raw machine numbers, and *those* get run. The ESP32 firmware works this way. The Arduino IDE takes `esp32PlantMonitoring_multiwifi_v3.ino` and converts it into a block of numbers that gets copied onto the chip.

Why the difference? Compiled code is faster and does not need an interpreter sitting alongside it — which matters enormously on a tiny chip with almost no memory. Interpreted code is easier to change and test — which matters enormously when you are building a website and want to see your change immediately.

You do not need to memorize this. You just need to not be surprised when Python "just runs" while the ESP32 needs a compile-and-upload step that takes a minute.

---

## 5. Installing software — what is really happening

When you install a program, three things happen:

1. Files get copied onto your disk (usually into `C:\Program Files\` or similar).
2. Windows gets told "this program exists, here is its icon, here is how to start it."
3. Sometimes, the program's location gets added to something called the **PATH**.

That third one causes more beginner pain than anything else in computing, so let us kill it right now.

### The PATH, explained once, properly

When you type `python` into a command window, Windows has to find a file called `python.exe`. It does not search your whole hard drive — that would take forever.

Instead, Windows keeps a list of folders to check. That list is called the **PATH**. If `python.exe` is in one of those folders, typing `python` works. If it is not, you get this:

```
'python' is not recognized as an internal or external command,
operable program or batch file.
```

That error means exactly one thing: **the program is probably installed fine, but Windows does not know where to look for it.**

This is why the Python installer has a checkbox that says *"Add Python to PATH"*, and why Chapter 03 will tell you in bold letters to tick it. Something like ninety percent of all "Python does not work" problems in the world are that one unticked checkbox.

Now you know. When you see "is not recognized," you will not panic — you will think *"ah, PATH."*

---

## 6. Text editors vs word processors

MS Word is a **word processor**. When you type in Word and save, it stores your words *plus* fonts, colors, margins, spacing — a large pile of invisible formatting.

Code files must contain **only** the characters you typed. One stray invisible formatting character and the program breaks in a way that is very hard to see.

So you never write code in Word. You use a **text editor** — a program that saves exactly the characters you typed and nothing else.

Notepad is a text editor. It works, but it is bare. We will use **VS Code**, which is a text editor with helpful extras: it colors your code so it is readable at a glance, it underlines mistakes before you run anything, and it has a command line built into the same window so you are not juggling programs.

---

## 7. The internet, in one page

Your web app talks to a database in the cloud. Your ESP32 talks to that same database. Your app talks to Google's AI. All of that runs on the same small handful of ideas.

**A server** is a computer that sits somewhere, always on, waiting for other computers to ask it for things.

**A client** is a computer that asks. Your laptop is a client. Your phone is a client. Your ESP32 is a client.

**A request** is a client asking a server for something. **A response** is what comes back.

**A URL** is the address of a thing on a server:

```
https://generativelanguage.googleapis.com/v1beta/interactions
```

Same idea as a file path, different punctuation.

**An API** — Application Programming Interface — is a door on a server designed for *programs* to knock on rather than people.

That distinction is worth a second. A website is a door for humans: you knock, and it sends back a pretty page with colors and buttons. An API is a door for programs: you knock, and it sends back raw data with no decoration, because the thing knocking is a program that will do its own formatting.

This project knocks on two APIs:

- **Supabase's API** — the ESP32 and the web app use it to store and fetch sensor readings.
- **Google Gemini's API** — the web app uses it to ask an AI what it thinks of the plant.

**An API key** is a password for a door. It proves you are allowed through, and it lets the owner track how much you use. Guard it exactly like a password, because that is precisely what it is. Chapter 13 is entirely about not leaking these.

---

## 8. The vocabulary you now own

Test yourself. Can you explain each of these to a friend, out loud, without looking?

- file · folder · path · extension
- program · interpreted · compiled
- PATH (the Windows list of places to look)
- text editor
- server · client · request · response
- URL · API · API key

If any of those are fuzzy, reread that section now. Everything from here builds on this vocabulary, and it is far cheaper to fix confusion here than in Chapter 09.

---

## What is next

You now know what files and programs are. Next you learn to talk to your computer without a mouse — which sounds worse than it is, and which unlocks everything else in this guide.

---

[← Previous](00-before-you-start.md) · [Contents](README.md) · [Next: The Command Line →](02-the-command-line.md)
