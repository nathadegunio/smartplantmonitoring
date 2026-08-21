# Chapter 02 — The Command Line

[← Previous](01-computer-basics.md) · [Contents](README.md) · [Next: Installing Your Tools →](03-installing-your-tools.md)

---

## The black window

You have seen it in movies. Hackers type furiously into a black window full of green text, and a building explodes.

The reality is far more boring and far more useful. The black window is called the **command line** — also **terminal**, **console**, **shell**, **CMD**, or **PowerShell**, depending on who you ask. All roughly the same thing.

It is a place where you type the name of a program and press Enter, and the program runs.

That is it. That is the whole concept.

---

## Why does this thing still exist?

Fair question. We have mice and windows and icons. Why is anyone still typing?

Three reasons, and they are good ones.

**1. Precision.** "Click the third icon from the left" is ambiguous. `python main.py` is not. There is exactly one thing that means.

**2. Repeatability.** You can save a command in a file and run it again in a year and get the same result. You cannot save a sequence of mouse clicks that way.

**3. Most developer tools have no buttons.** Git, Python, Claude Code, Streamlit — none of these come with a window and icons. They come with a name you type. If you refuse to use the command line, most of the software world is simply closed to you.

Here is the reframe that helps most: **the command line is not harder than clicking. It is just less discoverable.** With icons you can look around and guess. With commands you have to already know the word. That is the only real difference. Once you know ten words, it is faster than clicking.

You need about ten words. They are all below.

---

## Opening it

On Windows you have two: **Command Prompt** (old) and **PowerShell** (newer, better). Use PowerShell.

**To open it:** press the Windows key, type `powershell`, press Enter.

A window appears with something like:

```
PS C:\Users\Nathaniel>
```

That is the **prompt**. It is the computer saying *"I am ready, and right now I am standing in the folder C:\Users\Nathaniel."*

That last part is the piece beginners miss and it causes endless trouble, so let us make it the centerpiece.

---

## The single most important idea: you are always somewhere

The command line always has a **current folder**. Every command you type happens *in that folder*, the same way a person can only pick things up in the room they are standing in.

If you type `python main.py` while standing in the wrong folder, you get "file not found" — not because the file does not exist, but because it is not in the room you are in.

Say this to yourself until it is automatic: **"Where am I standing?"** It solves an amazing number of problems.

---

## The ten commands you actually need

### `pwd` — where am I?

```
pwd
```

Prints the folder you are currently standing in. (It stands for "print working directory.") The prompt usually shows it too, but when you are lost, this is the answer.

### `ls` — what is in here?

```
ls
```

Lists the files and folders in the current folder. Like opening the folder in Explorer, but as text.

> `dir` does the same thing on Windows. Both work in PowerShell. Use whichever sticks in your head.

### `cd` — go somewhere

```
cd Desktop
```

**c**hange **d**irectory. Moves you into the `Desktop` folder.

```
cd ..
```

Two dots means "up one level, to the folder containing me."

```
cd C:\Users\Nathaniel\Desktop\PlantMonitoring2
```

You can jump straight to a full path.

> **The trick that saves you from typos:** type `cd ` (with a space), then **drag the folder from Windows Explorer into the terminal window**. The full path types itself. This works everywhere, it is not cheating, and experienced people do it constantly.

> **The other trick:** start typing a folder name and press **Tab**. It completes it for you. Press Tab twice to see the options. Tab is your best friend on the command line.

### `mkdir` — make a new folder

```
mkdir myproject
```

### `cat` — show me what is inside this file

```
cat main.py
```

Dumps the whole file to the screen. Fine for short files, overwhelming for long ones.

### Up arrow — repeat what I just did

Not a command, but you will use it more than any command. Press the **up arrow** to bring back your previous command. Press it repeatedly to go further back.

You will run the same command dozens of times while testing. Up-arrow-Enter is the rhythm of the job.

### `Ctrl + C` — make it stop

If something is running and will not stop — a server, a stuck program, a wall of scrolling text — press **Ctrl + C**. That is the universal "stop this now."

You will need this every single time you run the web app, because Streamlit runs forever until you stop it. Remember it.

### `cls` — clean up the mess

```
cls
```

Clears the screen. Purely cosmetic, surprisingly calming.

### `python` — run Python

```
python --version
```

Runs Python. `--version` tells it to just report its version and quit. This is how you check something is installed correctly — Chapter 03 uses this repeatedly.

### `git` — version control

```
git status
```

You will meet this properly in Chapter 05.

---

## Reading command syntax

Commands often look like this:

```
pip install -r requirements.txt
```

Break it into pieces:

- `pip` — the **program** you are running
- `install` — the **subcommand**, what you want it to do
- `-r` — a **flag** (also called an option or switch). Flags start with `-` or `--` and change behavior. `-r` here means "read the list from a file."
- `requirements.txt` — the **argument**, the thing being acted on

Once you see that structure, commands stop looking like magic spells and start looking like sentences. Verb, adverb, object.

---

## Errors are messages, not punishment

You will type things wrong. Constantly. Everyone does. The terminal will respond with red text.

**Read it.** It is genuinely trying to help.

Here are the three you will actually meet:

**"is not recognized as an internal or external command"**

The program is not installed, or it is not on the PATH. Chapter 01, section 5. Usually you forgot to tick a box during install, or you need to close and reopen the terminal.

**"No such file or directory" / "cannot find path"**

You are standing in the wrong folder, or you typo'd the name. Run `pwd` and `ls` and look at where you actually are.

**"Access is denied" / "Permission denied"**

You are trying to touch something Windows is protecting. Rarely happens in this project. If it does, try opening PowerShell as Administrator (right-click → Run as administrator).

That is honestly most of them.

---

## A five-minute practice run

Do this now. Actually type it. Reading it is not the same.

```
pwd
cd Desktop
mkdir practice
cd practice
pwd
ls
mkdir inside
ls
cd inside
pwd
cd ..
cd ..
pwd
```

Then open Windows Explorer, go to your Desktop, and look at the `practice` folder you just made without ever touching the mouse.

That is the moment the command line clicks for most people: *oh, it is the same folders. I am just using different hands.*

You can delete the practice folder afterward, in Explorer, like a normal person.

---

## The mental model to keep

The command line is a conversation:

- You are standing in a folder.
- You type the name of a program plus what it should work on.
- It does the thing and prints what happened.
- You are still standing in that folder, ready for the next thing.

That is all. There is no hidden depth waiting to embarrass you.

---

## What is next

Now you can navigate. Next you install the actual tools — and you will use everything from this chapter to check that each one worked.

---

[← Previous](01-computer-basics.md) · [Contents](README.md) · [Next: Installing Your Tools →](03-installing-your-tools.md)
