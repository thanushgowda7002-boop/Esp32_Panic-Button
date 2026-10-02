"""
Self-Destruct Button - laptop side (100% fake, deletes NOTHING)
Install:  pip install pyserial
Run:      python self_destruct.py

Button press -> fake hacker terminal -> 5..1 flashing red countdown
             -> fake blue screen -> "SYSTEM DELETED" black screen.
Press the button again (or hit Esc) at any time to exit.
Uses the same ESP32 code as the panic button, no reflashing needed.
"""

import queue
import random
import threading
import time
import tkinter as tk

import serial
import serial.tools.list_ports

# ---------------- Settings ----------------
PORT = None        # e.g. "COM3". None = auto-detect
BAUD = 115200
COUNTDOWN_FROM = 5
# -------------------------------------------

events = queue.Queue()

FAKE_LINES = [
    "> INITIALIZING SELF-DESTRUCT SEQUENCE...",
    "> Authorization accepted: ROOT",
    "> Disabling antivirus............ OK",
    "> Disabling firewall............. OK",
    "> Encrypting C:\\Users\\Documents...... [##########] 100%",
    "> Deleting C:\\Users\\Pictures\\holiday_2024.zip",
    "> Deleting C:\\Users\\Desktop\\homework_FINAL.docx",
    "> Deleting C:\\Windows\\System32\\...",
    "> Wiping browser history......... OK",
    "> Uploading secrets to the internet... 87%",
    "> Overheating CPU................ WARNING",
    "> Fan speed: MAX",
    "> !!! POINT OF NO RETURN REACHED !!!",
    "> DETONATION IN T-MINUS...",
]


def find_port():
    if PORT:
        return PORT
    for p in serial.tools.list_ports.comports():
        desc = (p.description or "").lower()
        if any(k in desc for k in ("cp210", "ch340", "usb serial", "uart", "silicon labs")):
            return p.device
    ports = list(serial.tools.list_ports.comports())
    return ports[0].device if ports else None


def serial_listener():
    port = find_port()
    if not port:
        print("No serial port found. Is the ESP32 plugged in?")
        return
    print(f"Listening on {port}...")
    while True:
        try:
            with serial.Serial(port, BAUD, timeout=1) as ser:
                while True:
                    if ser.readline().decode(errors="ignore").strip() == "PANIC":
                        events.put("PRESS")
        except serial.SerialException:
            time.sleep(2)


def beep(freq):
    try:
        import winsound  # Windows only; silently skipped elsewhere
        threading.Thread(target=winsound.Beep, args=(freq, 150), daemon=True).start()
    except ImportError:
        pass


class SelfDestruct:
    def __init__(self, root):
        self.root = root
        self.win = None

    @property
    def running(self):
        return self.win is not None

    def start(self):
        w = self.win = tk.Toplevel(self.root)
        w.attributes("-fullscreen", True)
        w.attributes("-topmost", True)
        w.configure(bg="black", cursor="none")
        w.bind("<Escape>", lambda e: self.stop())
        w.focus_force()
        self.terminal()

    def stop(self):
        if self.win:
            self.win.destroy()
            self.win = None

    def after(self, ms, fn):
        if self.win:
            self.win.after(ms, fn)

    def clear(self):
        for child in self.win.winfo_children():
            child.destroy()

    # ---- Phase 1: fake hacker terminal ----
    def terminal(self):
        t = tk.Text(self.win, bg="black", fg="#00ff41", font=("Consolas", 16),
                    bd=0, highlightthickness=0, cursor="none")
        t.pack(fill="both", expand=True, padx=30, pady=30)
        self.type_line(t, 0)

    def type_line(self, t, i):
        if not self.win:
            return
        if i >= len(FAKE_LINES):
            self.after(500, lambda: self.countdown(COUNTDOWN_FROM))
            return
        t.insert("end", FAKE_LINES[i] + "\n")
        t.see("end")
        self.after(random.randint(120, 320), lambda: self.type_line(t, i + 1))

    # ---- Phase 2: flashing countdown ----
    def countdown(self, n):
        if not self.win:
            return
        if n == 0:
            self.bsod()
            return
        self.clear()
        title = tk.Label(self.win, text="SELF-DESTRUCT IN", font=("Consolas", 40, "bold"))
        big = tk.Label(self.win, text=str(n), font=("Consolas", 320, "bold"))
        title.pack(pady=(80, 0))
        big.pack(expand=True)
        beep(1500 if n == 1 else 1000)
        self.flash([title, big], 0, n)

    def flash(self, widgets, k, n):
        if not self.win:
            return
        if k == 4:
            self.countdown(n - 1)
            return
        bg, fg = ("red", "white") if k % 2 == 0 else ("black", "red")
        self.win.configure(bg=bg)
        for w in widgets:
            w.configure(bg=bg, fg=fg)
        self.after(250, lambda: self.flash(widgets, k + 1, n))

    # ---- Phase 3: fake blue screen ----
    def bsod(self):
        self.clear()
        self.win.configure(bg="#0078d7")
        style = dict(bg="#0078d7", fg="white", anchor="w", justify="left")
        tk.Label(self.win, text=":(", font=("Segoe UI", 160), **style).pack(
            anchor="w", padx=120, pady=(100, 0))
        tk.Label(self.win, font=("Segoe UI", 28), **style,
                 text="Your PC ran into a problem and needs to restart.\n"
                      "We're just collecting some error info, and then we'll restart for you."
                 ).pack(anchor="w", padx=130, pady=20)
        pct = tk.Label(self.win, text="0% complete", font=("Segoe UI", 28), **style)
        pct.pack(anchor="w", padx=130)
        self.progress(pct, 0)

    def progress(self, label, value):
        if not self.win:
            return
        if value >= 100:
            label.configure(text="100% complete")
            self.after(700, self.final)
            return
        label.configure(text=f"{value}% complete")
        self.after(150, lambda: self.progress(label, value + random.randint(4, 14)))

    # ---- Phase 4: it's over ----
    def final(self):
        if not self.win:
            return
        self.clear()
        self.win.configure(bg="black")
        tk.Label(self.win, text="SYSTEM DELETED", bg="black", fg="#555555",
                 font=("Consolas", 40, "bold")).pack(expand=True)


def main():
    root = tk.Tk()
    root.withdraw()
    sd = SelfDestruct(root)

    def poll():
        try:
            while True:
                events.get_nowait()
                sd.stop() if sd.running else sd.start()
        except queue.Empty:
            pass
        root.after(50, poll)

    threading.Thread(target=serial_listener, daemon=True).start()
    poll()
    root.mainloop()


if __name__ == "__main__":
    main()
