# OCR Snip to Clipboard - Windows Hintergrund-Tool
# Hotkey: Ctrl+Alt+S zum Starten der Bildschirmauswahl

import tkinter as tk
from PIL import Image, ImageGrab, ImageFilter
import pytesseract
import pyperclip
import keyboard
import threading
import time
import sys
import os
import winreg
from pathlib import Path

# --- Konfiguration ---
APP_NAME = "OCR ClipText"
HOTKEY = "ctrl+alt+s"
OCR_LANG = "eng"  # oder "deu" für Deutsch, "deu+eng" für beides

# Tesseract-Pfad automatisch erkennen oder setzen
def find_tesseract():
    """Versucht Tesseract automatisch zu finden"""
    # AppData-Pfad (häufig bei Benutzer-Installation)
    appdata_path = os.path.join(
        os.path.expanduser("~"),
        "AppData", "Local", "Programs", "Tesseract-OCR", "tesseract.exe"
    )

    possible_paths = [
        appdata_path,  # Zuerst AppData prüfen
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.join(os.path.dirname(sys.executable), "tesseract.exe"),
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    # Versuche aus PATH
    try:
        import shutil
        path = shutil.which("tesseract")
        if path:
            return path
    except:
        pass

    return None

# Setze Tesseract-Pfad
tesseract_path = find_tesseract()
if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    # Fallback - wird Fehler werfen wenn Tesseract nicht gefunden wird
    pass

# --- Autostart-Funktionen ---
def add_to_autostart():
    """Fügt die Anwendung zum Windows-Autostart hinzu"""
    try:
        exe_path = sys.executable if getattr(sys, 'frozen', False) else __file__
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, f'"{exe_path}"')
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"Fehler beim Hinzufügen zum Autostart: {e}")
        return False

def remove_from_autostart():
    """Entfernt die Anwendung aus dem Windows-Autostart"""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, APP_NAME)
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return True  # War nicht im Autostart
    except Exception as e:
        print(f"Fehler beim Entfernen aus Autostart: {e}")
        return False

def is_in_autostart():
    """Prüft ob die Anwendung im Autostart ist"""
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

# --- Toast-Benachrichtigungen (robuste Fallback-Lösung) ---
class SimpleToast:
    """Einfache Benachrichtigungen mit Tkinter (robust & zuverlässig)"""

    @staticmethod
    def show(title, message, duration=3):
        """Zeigt eine einfache Benachrichtigung"""
        def show_notification():
            try:
                root = tk.Tk()
                root.title(title)
                root.attributes('-topmost', True)
                root.overrideredirect(True)  # Kein Rahmen

                # Position: Rechts unten
                screen_width = root.winfo_screenwidth()
                screen_height = root.winfo_screenheight()
                width = 300
                height = 100
                x = screen_width - width - 20
                y = screen_height - height - 60
                root.geometry(f'{width}x{height}+{x}+{y}')

                # Styling
                root.configure(bg='#2b2b2b')

                # Title Label
                title_label = tk.Label(
                    root,
                    text=title,
                    bg='#2b2b2b',
                    fg='#ffffff',
                    font=('Arial', 10, 'bold'),
                    padx=10,
                    pady=5
                )
                title_label.pack(anchor='w')

                # Message Label
                message_label = tk.Label(
                    root,
                    text=message,
                    bg='#2b2b2b',
                    fg='#dddddd',
                    font=('Arial', 9),
                    wraplength=280,
                    justify='left',
                    padx=10,
                    pady=5
                )
                message_label.pack(anchor='w', fill='both', expand=True)

                # Click zum Schließen
                root.bind('<Button-1>', lambda e: root.destroy())
                title_label.bind('<Button-1>', lambda e: root.destroy())
                message_label.bind('<Button-1>', lambda e: root.destroy())

                # Auto-close
                root.after(duration * 1000, root.destroy)

                root.mainloop()
            except Exception as e:
                # Letzter Fallback: Konsolen-Ausgabe
                print(f"[{title}] {message}")

        threading.Thread(target=show_notification, daemon=True).start()

TOAST = SimpleToast()

# --- Auswahlfenster / Screenshot ---
class SnipTool:
    def __init__(self):
        self.start_x = None
        self.start_y = None
        self.rect = None
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-alpha", 0.6)  # Dunkler wie Snipping Tool (0.6 = 60% sichtbar)
        self.root.attributes("-topmost", True)
        self.root.config(cursor="cross", bg='black')

        self.canvas = tk.Canvas(self.root, cursor="cross", bg="gray10", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        self.root.bind("<Escape>", lambda e: self.exit_cancel())

        # Anleitung anzeigen
        instruction_text = f"Ziehe ein Rechteck um den Text • ESC zum Abbrechen"
        self.instruction = self.canvas.create_text(
            self.root.winfo_screenwidth() // 2,
            30,
            text=instruction_text,
            fill="white",
            font=("Arial", 14, "bold")
        )

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y,
            outline='red', width=3
        )

    def on_move_press(self, event):
        curX, curY = event.x, event.y
        self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)

    def on_button_release(self, event):
        end_x = event.x
        end_y = event.y

        left = int(min(self.start_x, end_x))
        top = int(min(self.start_y, end_y))
        right = int(max(self.start_x, end_x))
        bottom = int(max(self.start_y, end_y))

        self.root.destroy()

        # Kleine Verzögerung damit Fenster komplett geschlossen ist
        time.sleep(0.1)

        if right - left > 10 and bottom - top > 10:  # Mindestgröße
            process_screenshot((left, top, right, bottom))
        else:
            TOAST.show("OCR Snip", "Auswahl zu klein", duration=2)

    def exit_cancel(self):
        self.root.destroy()
        TOAST.show("OCR Snip", "Abgebrochen", duration=2)

def process_screenshot(bbox):
    """Verarbeitet den Screenshot und führt OCR aus"""
    try:
        # Screenshot
        img = ImageGrab.grab(bbox=bbox)

        # Bildverbesserung für bessere OCR
        img = img.convert("L")  # Graustufen

        # Bild vergrößern für bessere Erkennung
        width, height = img.size
        img = img.resize((width * 2, height * 2), Image.LANCZOS)

        # Schärfen
        img = img.filter(ImageFilter.SHARPEN)

        # OCR durchführen
        text = pytesseract.image_to_string(img, lang=OCR_LANG)
        text = text.strip()

        if text:
            pyperclip.copy(text)
            preview = text[:100] + ("..." if len(text) > 100 else "")
            TOAST.show("OCR Snip", f"Text kopiert:\n{preview}", duration=4)
        else:
            TOAST.show("OCR Snip", "Kein Text erkannt", duration=3)

    except Exception as e:
        error_msg = str(e)
        if "tesseract" in error_msg.lower():
            TOAST.show("OCR Snip Fehler", "Tesseract OCR nicht gefunden!", duration=5)
        else:
            TOAST.show("OCR Snip Fehler", f"Fehler: {error_msg}", duration=5)

# --- Hotkey Listener ---
def start_selection():
    """Startet das Auswahl-Tool"""
    try:
        tool = SnipTool()
        tool.root.mainloop()
    except Exception as e:
        TOAST.show("Fehler", f"Fehler beim Starten: {e}", duration=5)

def main():
    """Hauptfunktion - startet den Hotkey-Listener"""

    # Prüfe ob Tesseract verfügbar ist
    try:
        pytesseract.get_tesseract_version()
    except Exception as e:
        print(f"WARNUNG: Tesseract OCR nicht gefunden!")
        print(f"Bitte installiere Tesseract von: https://github.com/tesseract-ocr/tesseract")
        TOAST.show(
            "OCR ClipText",
            "Tesseract OCR nicht gefunden!\nBitte installieren von github.com/tesseract-ocr",
            duration=8
        )

    # Autostart hinzufügen wenn noch nicht vorhanden
    if not is_in_autostart():
        if add_to_autostart():
            print(f"✓ {APP_NAME} zum Autostart hinzugefügt")

    print(f"\n{'='*50}")
    print(f"  {APP_NAME} läuft im Hintergrund")
    print(f"{'='*50}")
    print(f"  Hotkey: {HOTKEY.upper()}")
    print(f"  Sprache: {OCR_LANG}")
    print(f"  Autostart: {'✓ Aktiv' if is_in_autostart() else '✗ Inaktiv'}")
    print(f"{'='*50}\n")

    # Hotkey registrieren
    keyboard.add_hotkey(HOTKEY, start_selection)

    # Initiale Benachrichtigung
    TOAST.show(
        APP_NAME,
        f"Bereit! Drücke {HOTKEY.upper()} für Screenshot-OCR",
        duration=4
    )

    # Programm läuft im Hintergrund
    try:
        keyboard.wait()  # Wartet auf Hotkeys
    except KeyboardInterrupt:
        print(f"\n{APP_NAME} beendet.")
        sys.exit(0)

if __name__ == "__main__":
    # Verhindere mehrere Instanzen (einfache Methode)
    import socket
    try:
        # Versuche einen Port zu binden - wenn erfolgreich, sind wir die einzige Instanz
        lock_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lock_socket.bind(('127.0.0.1', 48127))  # Zufälliger Port
    except OSError:
        print(f"{APP_NAME} läuft bereits!")
        sys.exit(1)

    main()
