# AutoClip-OCR - Screenshot OCR with System Tray & Settings
# Version 2.0 - Hybrid EXE with integrated Settings Dialog

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageGrab, ImageFilter, ImageDraw
import pytesseract
import pyperclip
import keyboard
import threading
import time
import sys
import os
import winreg
import json
from pathlib import Path

# Configuration
APP_NAME = "AutoClip-OCR"
VERSION = "2.0"
HOTKEY = "ctrl+alt+s"
CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".autoclip-ocr", "config.json")

# Config Management
class Config:
    def __init__(self):
        self.config_dir = os.path.dirname(CONFIG_FILE)
        self.config = self.load()

    def load(self):
        """Loads config or creates default"""
        default_config = {
            "first_run": True,
            "autostart": False,
            "ocr_language": "eng",
            "hotkey": "ctrl+alt+s"
        }

        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r') as f:
                    loaded = json.load(f)
                    # Merge with defaults (in case new keys were added)
                    return {**default_config, **loaded}
        except:
            pass

        return default_config

    def save(self):
        """Saves config"""
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving: {e}")
            return False

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value

    def is_first_run(self):
        return self.config.get("first_run", True)

    def mark_not_first_run(self):
        self.config["first_run"] = False
        self.save()

# Global config instance
config = Config()

# Find Tesseract Path
def find_tesseract():
    """Tries to find Tesseract automatically"""
    appdata_path = os.path.join(
        os.path.expanduser("~"),
        "AppData", "Local", "Programs", "Tesseract-OCR", "tesseract.exe"
    )

    possible_paths = [
        appdata_path,
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.path.dirname(sys.executable), "tesseract.exe"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    try:
        import shutil
        path = shutil.which("tesseract")
        if path:
            return path
    except:
        pass

    return None

tesseract_path = find_tesseract()
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path

# Autostart Management
def is_in_autostart():
    """Checks if app is in autostart"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_READ
        )
        winreg.QueryValueEx(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False
    except:
        return False

def set_autostart(enabled):
    """Enables/Disables autostart"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )

        if enabled:
            exe_path = sys.executable if getattr(sys, 'frozen', False) else __file__
            winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
        else:
            try:
                winreg.DeleteValue(key, APP_NAME)
            except FileNotFoundError:
                pass

        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Autostart error: {e}")
        return False

# Toast Notifications
class SimpleToast:
    """Simple notifications with Tkinter"""

    @staticmethod
    def show(title, message, duration=3):
        """Shows notification"""
        def show_notification():
            try:
                root = tk.Tk()
                root.title(title)
                root.attributes('-topmost', True)
                root.overrideredirect(True)

                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                width = 320
                height = 100
                x = screen_width - width - 20
                y = screen_height - height - 60
                root.geometry(f'{width}x{height}+{x}+{y}')

                root.configure(bg='#2b2b2b')

                title_label = tk.Label(
                    root, text=title, bg='#2b2b2b', fg='#ffffff',
                    font=('Segoe UI', 10, 'bold'), padx=10, pady=5
                )
                title_label.pack(anchor='w')

                message_label = tk.Label(
                    root, text=message, bg='#2b2b2b', fg='#dddddd',
                    font=('Segoe UI', 9), wraplength=300, justify='left',
                    padx=10, pady=5
                )
                message_label.pack(anchor='w', fill='both', expand=True)

                root.bind('<Button-1>', lambda e: root.destroy())
                title_label.bind('<Button-1>', lambda e: root.destroy())
                message_label.bind('<Button-1>', lambda e: root.destroy())

                root.after(duration * 1000, root.destroy)
                root.mainloop()
            except Exception as e:
                print(f"[{title}] {message}")

        threading.Thread(target=show_notification, daemon=True).start()

TOAST = SimpleToast()

# Settings Dialog
class SettingsDialog:
    def __init__(self, parent=None):
        self.root = tk.Toplevel(parent) if parent else tk.Tk()
        self.root.title(f"{APP_NAME} - Einstellungen")
        self.root.geometry("500x400")
        self.root.resizable(False, False)

        # Set icon (if available)
        try:
            icon_path = os.path.join(os.path.dirname(sys.executable if getattr(sys, 'frozen', False) else __file__), "app_icon.ico")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass

        self.changes_made = False
        self.initial_values = {}

        self.setup_ui()
        self.load_current_settings()

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.root.winfo_screenheight() // 2) - (400 // 2)
        self.root.geometry(f"500x400+{x}+{y}")

    def setup_ui(self):
        """Creates the UI"""
        # Header
        header_frame = tk.Frame(self.root, bg='#2b2b2b', height=60)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)

        tk.Label(
            header_frame, text=APP_NAME, bg='#2b2b2b', fg='white',
            font=('Segoe UI', 16, 'bold')
        ).pack(pady=10, padx=20, anchor='w')

        tk.Label(
            header_frame, text=f"Version {VERSION}", bg='#2b2b2b', fg='#888888',
            font=('Segoe UI', 9)
        ).pack(padx=20, anchor='w')

        # Content
        content = tk.Frame(self.root, padx=20, pady=20)
        content.pack(fill='both', expand=True)

        # Autostart
        autostart_frame = tk.LabelFrame(content, text="Autostart", padx=10, pady=10)
        autostart_frame.pack(fill='x', pady=(0, 15))

        self.autostart_var = tk.BooleanVar()
        autostart_cb = tk.Checkbutton(
            autostart_frame,
            text="Automatisch mit Windows starten (empfohlen)",
            variable=self.autostart_var,
            command=self.on_change
        )
        autostart_cb.pack(anchor='w')

        tk.Label(
            autostart_frame,
            text="Das Programm startet automatisch im Hintergrund und ist sofort einsatzbereit.",
            font=('Segoe UI', 8),
            fg='#666666',
            wraplength=450,
            justify='left'
        ).pack(anchor='w', pady=(5, 0))

        # OCR-Sprache
        lang_frame = tk.LabelFrame(content, text="OCR-Sprache", padx=10, pady=10)
        lang_frame.pack(fill='x', pady=(0, 15))

        self.lang_var = tk.StringVar()
        lang_options = [
            ("Englisch", "eng"),
            ("Deutsch", "deu"),
            ("Deutsch + Englisch", "deu+eng")
        ]

        for text, value in lang_options:
            tk.Radiobutton(
                lang_frame,
                text=text,
                variable=self.lang_var,
                value=value,
                command=self.on_change
            ).pack(anchor='w')

        # Info
        info_frame = tk.LabelFrame(content, text="Information", padx=10, pady=10)
        info_frame.pack(fill='both', expand=True)

        info_text = f"""Hotkey: Strg+Alt+S
Funktion: Screenshot-Bereich auswählen und Text automatisch in Zwischenablage kopieren

Status: {"Tesseract OCR gefunden ✓" if tesseract_path else "⚠ Tesseract OCR nicht gefunden!"}

Bei Problemen: github.com/DancingTedDanson011/AutoClip-OCR"""

        tk.Label(
            info_frame,
            text=info_text,
            font=('Segoe UI', 9),
            justify='left',
            anchor='nw'
        ).pack(fill='both', expand=True)

        # Buttons
        button_frame = tk.Frame(self.root, padx=20, pady=10)
        button_frame.pack(fill='x', side='bottom')

        self.save_btn = tk.Button(
            button_frame,
            text="Speichern",
            command=self.save_settings,
            bg='#0078d4',
            fg='white',
            font=('Segoe UI', 10),
            padx=20,
            pady=8,
            state='disabled'
        )
        self.save_btn.pack(side='right', padx=(5, 0))

        tk.Button(
            button_frame,
            text="Abbrechen",
            command=self.root.destroy,
            font=('Segoe UI', 10),
            padx=20,
            pady=8
        ).pack(side='right')

    def load_current_settings(self):
        """Loads current settings"""
        self.autostart_var.set(is_in_autostart())
        self.lang_var.set(config.get("ocr_language", "eng"))

        # Save initial values
        self.initial_values = {
            "autostart": self.autostart_var.get(),
            "language": self.lang_var.get()
        }

    def on_change(self):
        """Called when changes are made"""
        current_values = {
            "autostart": self.autostart_var.get(),
            "language": self.lang_var.get()
        }

        self.changes_made = (current_values != self.initial_values)
        self.save_btn.config(state='normal' if self.changes_made else 'disabled')

    def save_settings(self):
        """Saves settings"""
        try:
            # Autostart
            set_autostart(self.autostart_var.get())
            config.set("autostart", self.autostart_var.get())

            # Language
            config.set("ocr_language", self.lang_var.get())

            # Save
            if config.save():
                TOAST.show("Einstellungen", "Erfolgreich gespeichert!", duration=2)
                self.root.destroy()
            else:
                messagebox.showerror("Fehler", "Einstellungen konnten nicht gespeichert werden!")
        except Exception as e:
            messagebox.showerror("Fehler", f"Fehler beim Speichern: {e}")

    def show(self):
        """Shows dialog"""
        self.root.mainloop()

# Screenshot & OCR
class SnipTool:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.6)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="cross", bg='black')

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray10", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", lambda e: self.exit_cancel())

        instruction_text = "Ziehe ein Rechteck um den Text • ESC zum Abbrechen"
        self.instruction = self.canvas.create_text(
            self.root.winfo_screenwidth() // 2, 30,
            text=instruction_text, fill="white", font=("Segoe UI", 14, "bold")
        )

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='#0078d4', width=3
        )

    def on_move_press(self, event):
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_button_release(self, event):
        left = int(min(self.start_x, event.x))
        top = int(min(self.start_y, event.y))
        right = int(max(self.start_x, event.x))
        bottom = int(max(self.start_y, event.y))

        self.root.destroy()
        time.sleep(0.1)

        if right - left > 10 and bottom - top > 10:
            process_screenshot((left, top, right, bottom))
        else:
            TOAST.show("AutoClip-OCR", "Auswahl zu klein", duration=2)

    def exit_cancel(self):
        self.root.destroy()
        TOAST.show("AutoClip-OCR", "Abgebrochen", duration=2)

def process_screenshot(bbox):
    """OCR processing"""
    try:
        img = ImageGrab.grab(bbox=bbox)
        img = img.convert("L")

        width, height = img.size
        img = img.resize((width * 2, height * 2), Image.LANCZOS)
        img = img.filter(ImageFilter.SHARPEN)

        ocr_lang = config.get("ocr_language", "eng")
        text = pytesseract.image_to_string(img, lang=ocr_lang)
        text = text.strip()

        if text:
            pyperclip.copy(text)
            preview = text[:80] + ("..." if len(text) > 80 else "")
            TOAST.show("Text kopiert!", preview, duration=4)
        else:
            TOAST.show("Kein Text erkannt", "Versuche einen größeren Bereich", duration=3)

    except Exception as e:
        error_msg = str(e)
        if "tesseract" in error_msg.lower():
            TOAST.show("Fehler", "Tesseract OCR nicht gefunden!", duration=5)
        else:
            TOAST.show("Fehler", f"OCR-Fehler: {error_msg}", duration=5)

def start_selection():
    """Starts screenshot selection"""
    try:
        tool = SnipTool()
        tool.root.mainloop()
    except Exception as e:
        TOAST.show("Fehler", f"Fehler: {e}", duration=5)

# System Tray
def create_tray_icon():
    """Creates System Tray Icon"""
    try:
        import pystray
        from PIL import Image, ImageDraw

        # Create icon
        def create_icon_image():
            size = (64, 64)
            image = Image.new('RGB', size, color='#0078d4')
            dc = ImageDraw.Draw(image)
            dc.rectangle([16, 16, 48, 48], fill='white')
            return image

        icon_image = create_icon_image()

        # Menu
        menu = pystray.Menu(
            pystray.MenuItem("Screenshot (Strg+Alt+S)", lambda: start_selection()),
            pystray.MenuItem("Einstellungen", lambda: show_settings()),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Beenden", lambda: exit_app())
        )

        icon = pystray.Icon(APP_NAME, icon_image, APP_NAME, menu)

        # Start in thread
        threading.Thread(target=icon.run, daemon=True).start()

        return icon
    except ImportError:
        print("pystray nicht installiert - kein System Tray Icon")
        return None

tray_icon = None

def show_settings():
    """Opens settings"""
    dialog = SettingsDialog()
    dialog.show()

def exit_app():
    """Exits program"""
    if tray_icon:
        tray_icon.stop()
    sys.exit(0)

# Main
def main():
    global tray_icon

    # Prevent multiple instances
    import socket
    try:
        lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lock_socket.bind(('127.0.0.1', 48127))
    except OSError:
        messagebox.showwarning(APP_NAME, f"{APP_NAME} läuft bereits!")
        sys.exit(1)

    # Check Tesseract
    if not tesseract_path:
        TOAST.show(
            "Tesseract nicht gefunden!",
            "Bitte installiere Tesseract OCR von github.com/tesseract-ocr",
            duration=8
        )

    # First run?
    if config.is_first_run():
        TOAST.show("Willkommen!", f"{APP_NAME} wird eingerichtet...", duration=2)
        time.sleep(2)

        dialog = SettingsDialog()
        dialog.root.title(f"{APP_NAME} - Ersteinrichtung")
        dialog.show()

        config.mark_not_first_run()

    # System Tray Icon
    tray_icon = create_tray_icon()

    # Register hotkey
    keyboard.add_hotkey(HOTKEY, start_selection)

    # Notification
    TOAST.show(
        f"{APP_NAME} bereit!",
        f"Drücke {HOTKEY.upper().replace('+', ' + ')} für Screenshot-OCR",
        duration=4
    )

    print(f"\n{'='*50}")
    print(f"  {APP_NAME} v{VERSION} läuft")
    print(f"{'='*50}")
    print(f"  Hotkey: {HOTKEY.upper()}")
    print(f"  Autostart: {'✓' if is_in_autostart() else '✗'}")
    print(f"  OCR-Sprache: {config.get('ocr_language', 'eng')}")
    print(f"{'='*50}\n")

    # Block until program is terminated
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        exit_app()

if __name__ == "__main__":
    main()
