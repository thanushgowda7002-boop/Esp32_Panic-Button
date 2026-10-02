<div align="center">

# 💀 Self-Destruct Button

### A physical ESP32 button that makes your laptop *pretend* to self-destruct

![ESP32](https://img.shields.io/badge/ESP32-Arduino-00979D?logo=arduino&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?logo=windows&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Prank Level](https://img.shields.io/badge/Prank%20Level-MAXIMUM-red)

**[▶ Watch the YouTube Short](YOUR_YOUTUBE_SHORT_LINK)** · **[🔔 Subscribe]https://youtube.com/shorts/LqQP1PybSLA?si=lazatKBimj55vOaY**

<!-- Drop a GIF of your demo here: ![Demo](demo.gif) -->

</div>

---

## 🎬 What It Does

Press one button and your laptop goes through a full fake meltdown:

1. 🟢 **Hacker terminal**: fake "deleting your files" log
2. 🔴 **5-second flashing countdown**: red/black strobe with beeps
3. 🔵 **Fake blue screen of death**: with a loading percentage
4. ⚫ **"SYSTEM DELETED"**: and silence

Press the button again (or hit `Esc`) to exit at any time.

> ⚠️ **100% fake.** This project only draws fullscreen windows. It does **not** delete, modify, or upload any files. Perfect for pranks and YouTube Shorts, harmless to your PC.

---

## 🧠 How It Works

```
┌──────────┐   USB serial    ┌─────────────────┐
│  ESP32   │ ──── "PANIC" ─▶ │  Laptop (Python)│
│ + Button │                 │  fullscreen UI  │
└──────────┘                 └─────────────────┘
```

- The **ESP32** watches the button (with debouncing) and sends `PANIC` over USB serial.
- A **Python script** on the laptop listens on the serial port and triggers the fake destruction sequence using `tkinter`.

---

## 🛒 Parts List

| Part | Qty | Notes |
|---|---|---|
| ESP32 dev board | 1 | Any ESP32 with USB |
| Push button | 1 | Any momentary button |
| Breadboard | 1 | Half-size is fine |
| Jumper wires | 2 | |
| USB data cable | 1 | Some cables only charge, so use a data cable |

Total cost: just a few dollars 💸

---

## 🔌 Wiring

```
   ESP32                 Button
 ┌────────┐
 │  GPIO4 ├──────────────● ─┐
 │        │                 │ (push button)
 │    GND ├──────────────● ─┘
 └────────┘
```

| Button leg | ESP32 pin |
|---|---|
| One leg | **GPIO 4** |
| Other leg | **GND** |

No resistor needed, because the code uses the ESP32's internal pull-up.

---

## 🚀 Setup

### 1. Flash the ESP32

1. Open `esp32/panic_button/panic_button.ino` in the **Arduino IDE**.
2. Select your ESP32 board and COM port.
3. Click **Upload**.
4. Close the Serial Monitor afterwards, because it blocks the port.

### 2. Run the laptop script

```bash
pip install pyserial
python laptop/self_destruct.py
```

You should see:

```
Listening on COM3...
```

Leave it running, then **press the button** 💥

---

## ⚙️ Settings

Edit these at the top of `self_destruct.py`:

| Setting | Default | Description |
|---|---|---|
| `PORT` | `None` | Set to `"COM3"` (or your port) if auto-detect fails |
| `BAUD` | `115200` | Must match the ESP32 code |
| `COUNTDOWN_FROM` | `5` | Countdown length in seconds |

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| `No serial port found` | Check the USB cable carries data and the ESP32 is plugged in |
| `Port busy / access denied` | Close the Arduino Serial Monitor or any other serial tool |
| Wrong port picked | Find your port in Device Manager and set `PORT` manually |
| `pip` not recognized | Use `python -m pip install pyserial` |
| No beep sound | Beeps use `winsound`, which is Windows only. The visuals still work elsewhere |
| Button triggers twice | Increase `DEBOUNCE_MS` in the `.ino` file |

Stop the script with `Ctrl + C` in the terminal.

---

## 📁 Project Structure

```
.
├── esp32/
│   └── panic_button/
│       └── panic_button.ino      # ESP32 firmware
├── laptop/
│   ├── self_destruct.py          # Self-destruct prank
│   └── panic_laptop.py           # Bonus: "boss is coming" panic button
└── README.md
```

> 🎁 **Bonus:** `panic_laptop.py` is a second mode. One press mutes audio, hides all windows, and shows a fake Excel spreadsheet. Same hardware, different prank.

---

## 🗺️ Ideas for Next Version

- [ ] Wireless version over Bluetooth / Wi-Fi
- [ ] Custom sound effects and voice ("Self-destruct sequence initiated")
- [ ] Mac and Linux beep support
- [ ] A fake "Windows Update" mode
- [ ] 3D-printed big red button enclosure

Got a better idea? Open an issue or tell me on YouTube! 👇

---

## 🎥 Follow the Build

If you liked this project, you'll love the next ones.

- ▶️ **YouTube:** https://youtube.com/@embedx-1?si=zl8PIW-ixC057bGI
- 📸 **Instagram:** https://www.instagram.com/embedx_projects/?hl=en
- 🐦 **X / Twitter:** https://x.com/EmbedXTech

⭐ **Star this repo** if you had fun. It really helps!

---

## 📜 License

Released under the [MIT License](LICENSE). Use it, remix it, prank your friends. Please don't use it to scare people in a way that could cause real trouble (like at work during an actual presentation 😄).
