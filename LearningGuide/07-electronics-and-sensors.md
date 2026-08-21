# Chapter 07 — Electronics and Sensors

[← Previous](06-the-big-picture.md) · [Contents](README.md) · [Next: The Firmware →](08-firmware.md)

---

You do not need electrical engineering. You need to understand four ideas and know which wire goes where.

---

## 1. Electricity, the useful minimum

Three words. That is genuinely enough for this project.

**Voltage** — how hard the electricity is pushing. Measured in volts (V). Think water pressure.

**Current** — how much electricity is flowing. Measured in amps (A). Think water flow rate.

**Ground (GND)** — the return path. Electricity flows out from a power pin, through a component, and back through ground. Every circuit needs it.

Rule you must not break: **components expect a specific voltage.** The ESP32 runs at 3.3V. Some sensors want 5V. Feeding 5V into a 3.3V pin can destroy the chip permanently.

So: read what your component wants, give it that. If unsure, ask before plugging in — Claude Code is good at this. Describe the exact sensor model and ask what voltage it needs.

---

## 2. The ESP32 — the brain

The ESP32 is a **microcontroller**: a complete tiny computer on one small board.

What makes it a microcontroller rather than a computer:

- It runs **one program**, forever, from the moment it powers on
- It has no screen, keyboard, or operating system
- It has **pins** — metal legs you connect things to
- It is cheap (a few hundred pesos) and sips power

And crucially for this project: **it has WiFi built in.** That single feature is what makes it an IoT device instead of a data logger. Without WiFi you would have to walk out to the garden with a USB cable to collect readings.

### Pins

Pins are the ESP32's senses and hands. Each one has a number, and each can be used in different ways:

- **Power pins** — `3V3` gives out 3.3 volts, `GND` is ground
- **Digital pins** — read or write on/off signals
- **Analog pins** — read a *range* of voltage, not just on/off (this is how the soil sensor works)
- **I2C pins** — a two-wire system many sensors speak, explained below

Here are the pins this project actually uses, straight out of the firmware:

```c
#define SDA_PIN      21    // I2C data      → light sensor + OLED
#define SCL_PIN      22    // I2C clock     → light sensor + OLED
#define DHTPIN        5    // temp/humidity sensor
#define SOIL_PIN     34    // soil moisture (analog input)
#define BUZZER_PIN   18    // the beeper
```

That is a wiring diagram written as code. Pin 5 has the DHT22 on it. Pin 34 has the soil probe. Pins 21 and 22 are shared by the light sensor and the screen.

---

## 3. How a sensor turns the world into a number

This is the idea worth understanding deeply, because it demystifies the whole hardware layer.

**Every sensor is a component whose electrical behavior changes with a physical condition.**

That is it. That is the trick behind all of them.

### The soil moisture sensor — the clearest example

It is a plastic blade you stick in the dirt. Wet soil and dry soil have different electrical properties, so the sensor's output voltage changes with moisture.

The ESP32 reads that voltage on pin 34 as a raw number between 0 and 4095.

But nothing about `2100` means "moist." Somebody has to teach it. That is **calibration**, and here it is in the firmware:

```c
const int DRY_VALUE = 3200;   // reading with the probe in bone-dry air
const int WET_VALUE = 1200;   // reading with the probe in a glass of water
```

Those two numbers were **measured by hand**. Somebody held the probe in dry air, wrote down 3200. Dunked it in water, wrote down 1200. Now every reading in between can be turned into a percentage.

Notice that dry is a *higher* number than wet. That surprises people. It is just how this sensor is wired — more moisture, less resistance, lower reading.

> **This matters for you:** your sensor will have different values than 3200 and 1200. Every probe is slightly different. If you build this, you must calibrate your own, or every soil reading will be wrong. This is the single most common reason a plant monitor reports nonsense.

**Calibration is the moment a raw number becomes meaningful.** It is a human deciding what the machine's numbers mean. Remember Chapter 01: meaning is always something a human added.

### DHT22 — temperature and humidity

A single small blue component that measures both. It has a chip inside that does its own conversion and sends the answer as a digital signal, so you get actual degrees and actual percentage — no calibration needed on your end.

It is not fast (about one reading every two seconds) and occasionally returns garbage. The firmware handles that:

```c
// Validate DHT22 readings before uploading.
...
Serial.println("Reason : Invalid DHT22 reading.");
```

If the sensor returns nonsense, the upload is **skipped** rather than sending bad data to the database. That is a small, important piece of engineering: **a system that knows when not to trust itself.**

Think about what that prevents. Without it, one glitched reading of `-999` degrees ends up in the database, gets averaged into the trend, and the AI confidently tells you your plant is freezing.

### BH1750 — light

Measures light in **lux**. Direct tropical noon sun is around 100,000 lux. A bright room is maybe 500. The chili pepper ideal band in this project is 10,000–50,000 lux — bright outdoor light, not full blazing noon.

It talks over I2C.

### I2C — the two-wire conversation

I2C is a system that lets **many** devices share just two wires:

- **SDA** — the data line (pin 21 here)
- **SCL** — the clock line (pin 22 here)

Every device on those two wires has a unique **address**, so the ESP32 can say "hey, device number 0x23, what is your reading?" and only that device answers.

That is why both the light sensor and the OLED screen connect to pins 21 and 22 in this project. Two devices, two wires, no conflict.

Without I2C you would run out of pins fast. It is one of those quiet ideas that makes everything else possible.

---

## 4. The output parts

### The OLED screen (SH1106, 128×64)

A small screen showing the current readings and the plant's status right there in the garden.

Why bother, when there is a whole dashboard? Because **the dashboard depends on WiFi, the cloud, and a phone.** The OLED works when all of that is down. Someone standing at the plant can always see what is happening.

Local display, remote dashboard. Two independent ways to know. That is not redundancy for its own sake — that is what makes the thing trustworthy.

### The buzzer

Beeps when a condition goes outside the safe range. Immediate physical attention. Nobody has to be looking at anything.

The number of beeps encodes the number of problems — one beep, one alert; three beeps, three alerts.

---

## 5. Wiring it up

A **breadboard** is a plastic block full of holes with hidden metal strips connecting them in rows. It lets you build circuits by pushing wires into holes instead of soldering. Nothing is permanent, everything can be pulled out and redone. Perfect for learning.

The connections for this project:

```
ESP32                     Component
──────────────────────────────────────────────────
3V3          ────────►    DHT22 VCC
GND          ────────►    DHT22 GND
GPIO 5       ────────►    DHT22 DATA

3V3          ────────►    BH1750 VCC
GND          ────────►    BH1750 GND
GPIO 21      ────────►    BH1750 SDA
GPIO 22      ────────►    BH1750 SCL

3V3          ────────►    Soil sensor VCC
GND          ────────►    Soil sensor GND
GPIO 34      ────────►    Soil sensor AOUT   (analog!)

3V3          ────────►    OLED VCC
GND          ────────►    OLED GND
GPIO 21      ────────►    OLED SDA           (shared with BH1750)
GPIO 22      ────────►    OLED SCL           (shared with BH1750)

GPIO 18      ────────►    Buzzer +
GND          ────────►    Buzzer −
```

Two things to notice:

- **Everything shares GND.** All grounds connect together. This is not optional — without a shared ground, nothing works.
- **21 and 22 are shared.** That is I2C doing its job.

> **Before you power anything on, check every wire twice.** A wrong connection can cost you a component. There is no undo in hardware. Take a photo of your wiring before you turn it on — it makes debugging much easier later.

---

## 6. Debugging hardware

Software tells you what went wrong. Hardware just sits there silently being broken. Different skill.

**Nothing turns on at all**
Power problem. Is the USB cable plugged in properly? Is it a *data* cable or a charge-only cable? (Charge-only cables are the source of endless wasted hours — they physically fit and carry power but no data.) Are VCC and GND connected the right way around?

**One sensor reads nonsense, the others are fine**
That sensor's wiring, or its calibration. Check its three wires. For soil, check your DRY/WET values.

**The I2C devices are dead (screen blank, light reads zero)**
SDA and SCL swapped, most likely. Or a bad connection. Ask Claude Code for an "I2C scanner sketch" — it is a tiny program that lists every I2C device it can find. If your device does not appear on that list, it is a wiring problem, not a code problem. That single test saves hours.

**Readings jump around wildly**
Loose wire. Breadboard connections work themselves free. Push everything in firmly and wiggle-test each one.

**Works on USB, dies when on battery**
Not enough power. The ESP32 draws a real spike of current when the WiFi radio transmits. A weak battery or power bank browns out at exactly that moment.

### The Serial Monitor is your eyes

The ESP32 can print text back to your computer over the USB cable. In Arduino IDE: **Tools → Serial Monitor**, set the speed to **115200**.

This firmware prints a lot — what it read, whether WiFi connected, whether the upload worked, and why it failed if it did not.

**When hardware misbehaves, open the Serial Monitor first.** Every time. It is the difference between guessing and knowing.

---

## What you should take from this chapter

You do not need to understand electronics. You need to understand:

- A sensor is a component whose electrical behavior changes with physical conditions
- The ESP32 reads that as a number
- **A human decides what that number means** (calibration)
- Wires go in specific holes, and getting them wrong has physical consequences
- The Serial Monitor is how you see inside

Everything above this line — the actual physics — someone else has already solved and packaged into a library you can call in one line.

---

[← Previous](06-the-big-picture.md) · [Contents](README.md) · [Next: The Firmware →](08-firmware.md)
