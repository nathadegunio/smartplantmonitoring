# Chapter 17 — Glossary

[← Previous](16-when-it-breaks.md) · [Contents](README.md)

---

Keep this open in a tab while you work. Every term is explained assuming you know nothing else on this page.

---

## A

**analog** — A signal that can be any value in a range, not just on/off. The soil sensor is analog — the ESP32 reads it as a number from 0 to 4095.

**API (Application Programming Interface)** — A door on a server built for programs to knock on rather than people. A website sends back a pretty page; an API sends back raw data.

**API key** — A password that proves your program is allowed to use an API. Treat it exactly like a password.

**Arduino IDE** — The program you use to write firmware and copy it onto an ESP32.

**argument** — The thing you give a command or function to work on. In `python main.py`, `main.py` is the argument.

---

## B

**base64** — A way of writing binary data (like a photo) using only ordinary text characters, so it can travel inside a text-based request.

**breadboard** — A plastic block full of holes with hidden metal strips inside, letting you build circuits by pushing wires in instead of soldering.

**bucket** — A folder in cloud storage for files that do not fit in a database table. This project's is `app-files`.

---

## C

**cache** — Remembering a result so you do not have to compute or fetch it again. `@st.cache_data` stops the app calling the AI on every refresh.

**calibration** — Measuring known conditions so raw sensor numbers can be converted into meaningful units. Dry air reads 3200, water reads 1200, so now 2100 means about 52%.

**client** — A computer that asks a server for something. Your phone, your laptop, your ESP32.

**cloud** — Somebody else's computer, in a data center, always on and always connected.

**command line** — A text window where you type program names to run them. Also terminal, console, shell, PowerShell.

**commit** — A saved snapshot of your whole project at one moment, with a note about what changed.

**compile** — Translate human-readable code into machine numbers ahead of time. Firmware is compiled; Python is not.

**component** — In this project, a file in `components/` that draws one section of the page.

**COM port** — The name Windows gives a connected serial device. Your ESP32 appears as something like `COM3`.

---

## D

**database** — A program that stores data in an organized way and answers questions about it fast.

**dataframe** — A table of data in Python, from the pandas library. Like a spreadsheet you can write code about.

**deploy** — Put your app on an always-on computer with a public address, so anyone can use it.

**DHT22** — The sensor that measures temperature and humidity.

**digital** — A signal that is only on or off, unlike analog.

**directory** — Another word for folder.

---

## E

**.env** — A file holding secret settings, kept out of Git.

**endpoint** — The specific URL of an API you send a request to.

**ESP32** — A small, cheap microcontroller with WiFi built in. The brain of the sensor board.

**extension** — The part of a filename after the dot: `.py`, `.ino`, `.md`. It says what kind of file it is.

---

## F

**fallback** — What a system does when the preferred path fails. Here, rule-based advice when the AI is unavailable.

**firmware** — A program that lives permanently inside a device and runs from the moment it gets power.

**flash** — Copy compiled firmware onto a chip.

**fork** — Your own copy of someone's GitHub repository, which you own and can change.

**function** — A named block of code you can run by name. `calculate_health()` is a function.

---

## G

**Gemini** — Google's family of AI models. This project uses `gemini-3.1-flash-lite`.

**Git** — A program on your computer that tracks every version of your files.

**GitHub** — A website that stores Git projects online.

**.gitignore** — A file listing things Git should pretend do not exist. Your security boundary for secrets.

**GPIO** — General Purpose Input/Output. The numbered pins on an ESP32 you connect things to.

**graceful degradation** — When part of a system fails, the rest keeps doing what it still can. The ESP32 keeps working offline; the dashboard falls back to rules without the AI.

**ground (GND)** — The return path in a circuit. Every component needs a connection to it.

---

## H

**header** — Extra information attached to a web request, separate from the main content. API keys usually travel in headers.

**HTTP / HTTPS** — The language computers use to talk over the web. The S means encrypted.

---

## I

**I2C** — A system letting many devices share just two wires (SDA for data, SCL for clock), each with its own address.

**IDE** — Integrated Development Environment. A program for writing code with helpful extras. VS Code, Arduino IDE.

**INSERT** — The database operation that adds new rows.

**interpreted** — Code read and executed line by line as it runs, rather than compiled ahead of time. Python.

**IoT (Internet of Things)** — Physical devices connected to the internet, sending or receiving data.

---

## J

**JSON** — A plain-text format for structured data that programs pass to each other:
```json
{"temperature_c": 31.2, "humidity": 58.0}
```

---

## L

**library** — Code someone else wrote that you use instead of writing your own. The DHT library handles the sensor's electrical timing so you can just call `readTemperature()`.

**LLM (Large Language Model)** — An AI trained on enormous amounts of human writing, which you can talk to in plain language. ChatGPT and Gemini are LLMs. **This is the core innovation in SmartGrow.**

**lux** — The unit of light intensity. Bright room ≈ 500. Direct tropical noon ≈ 100,000.

---

## M

**Markdown (.md)** — A simple way of writing formatted text with plain characters. This guide is Markdown.

**microcontroller** — A tiny complete computer on one board that runs a single program forever. The ESP32.

**model** — A specific AI. `gemini-3.1-flash-lite` is a model.

**multimodal** — An AI that handles more than one kind of input — here, images and text in the same request.

---

## N

**Node.js** — A runtime for JavaScript. Needed here only because Claude Code installs through it.

**NTP (Network Time Protocol)** — How a device gets the accurate current time from the internet.

---

## P

**package / library** — See library.

**pandas** — A Python library for working with tables of data.

**PATH** — The list of folders Windows searches when you type a program name. "Is not recognized" means the program is not on it.

**pin** — A metal connection point on the ESP32.

**pip** — Python's tool for installing libraries.

**POST** — The HTTP request type meaning "here is some new data, store it."

**PostgreSQL / Postgres** — The database engine Supabase runs.

**prompt** — (1) The `PS C:\>` symbol where you type commands. (2) The instructions you give an AI. Context makes it clear which.

**prompt engineering** — Writing AI instructions carefully so the output is reliable and useful.

**push** — Send your commits up to GitHub.

**Python** — The programming language the web app is written in.

---

## R

**repository (repo)** — A folder that Git is tracking, plus its full history.

**request / response** — A client asks; a server answers.

**requirements.txt** — A list of every Python library a project needs, with exact versions.

**rerun** — Streamlit re-executing your whole script from the top whenever anything changes.

**RLS (Row Level Security)** — Supabase's permission system. Blocks everything by default until you write policies. **The most common cause of "it works in the dashboard but not in my app."**

**row** — One record in a database table. Here, one complete sensor reading at one moment.

---

## S

**SDA / SCL** — The two I2C wires: data and clock.

**SELECT** — The database operation that reads rows.

**secret** — Any value that proves who you are or gets you into something. Never commit one.

**serial** — Communication over the USB cable between the ESP32 and your computer.

**Serial Monitor** — The Arduino IDE window showing what the ESP32 is printing. **Your primary debugging tool for hardware.**

**server** — A computer that is always on, waiting for requests.

**service** — In this project, a file in `services/` that knows how to do something (fetch data, call an AI) without drawing anything.

**session state** — Streamlit's box for values that must survive a rerun.

**SSID** — The name of a WiFi network.

**Streamlit** — A Python library that turns Python scripts into web apps without HTML, CSS, or JavaScript.

**Supabase** — The cloud service providing this project's database, file storage, and API.

---

## T

**table** — A grid of data in a database. This project's is `esp32_log`.

**terminal** — See command line.

**timestamp** — A recorded moment in time.

**timeout** — A limit on how long to wait before giving up. The Gemini call gives up after 20 seconds.

**TOML** — A settings file format. Streamlit Cloud secrets use it: `KEY = "value"`.

---

## U

**UPDATE** — The database operation that changes existing rows.

**upsert** — Insert if it does not exist, update if it does. How `latest.jpg` is always overwritten.

**URL** — The address of something on the internet.

**UTC** — The world's reference time zone. Supabase stores everything in it; the Philippines is UTC+8.

---

## V

**variable** — A named place to keep a value.

**venv (virtual environment)** — A private box of Python libraries for one project, so projects do not conflict.

**VS Code** — The code editor used in this project.

---

## W

**WiFi credentials** — A network's name and password. Secrets.

---

## The ten that matter most

If you are overwhelmed, these are the ones that carry the most weight in this project:

1. **API** — a door programs knock on
2. **API key** — the password for that door
3. **LLM** — the AI you talk to in plain language
4. **prompt** — the instructions you give it
5. **RLS** — Supabase's permission wall
6. **calibration** — teaching a sensor what its numbers mean
7. **fallback** — what happens when the good path fails
8. **cache** — remembering so you do not redo work
9. **commit** — a saved snapshot of everything
10. **PATH** — why "is not recognized" happens

---

[← Previous](16-when-it-breaks.md) · [Contents](README.md)
