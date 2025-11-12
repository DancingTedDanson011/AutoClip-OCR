# Installer Build-Anleitung

## Voraussetzungen

1. **Inno Setup 6** installieren:
   - Download: https://jrsoftware.org/isdl.php
   - Version: 6.x (neueste)

2. **EXE bereits gebaut**:
   - `dist/OCR_ClipText.exe` muss existieren
   - Falls nicht: `build.bat` ausführen

## Installer bauen

### Methode 1: Automatisch (empfohlen)

```batch
build_installer.bat
```

Das Script:
- Prüft ob Inno Setup installiert ist
- Kompiliert den Installer automatisch
- Erstellt: `installer_output\AutoClip-OCR_Setup.exe`

### Methode 2: Manuell

1. Öffne `installer.iss` mit Inno Setup
2. Drücke **F9** oder klicke "**Compile**"
3. Warte bis fertig (~10 Sekunden)
4. Installer ist in: `installer_output\AutoClip-OCR_Setup.exe`

## Was macht der Installer?

### Willkommensseite:
- Erklärt was AutoClip-OCR ist
- Erklärt was OCR ist
- Warnt dass Tesseract benötigt wird

### Tesseract-Hinweis:
- Dedizierte Seite mit Tesseract-Erklärung
- Download-Link
- Installations-Anleitung
- Öffnet optional die Download-Seite

### Installation:
- Installiert die .exe
- Erstellt Startmenü-Verknüpfung (optional)
- Erstellt Desktop-Icon (optional)
- Richtet Autostart ein (optional)

### Nach Installation:
- Startet AutoClip-OCR optional
- Zeigt README

## Installer-Features

✅ Prüft ob Tesseract installiert ist
✅ Warnt wenn Tesseract fehlt
✅ Bietet an, Tesseract-Download-Seite zu öffnen
✅ Beendet laufende Instanzen vor Installation
✅ Entfernt alte Versionen bei Deinstallation
✅ Deutsch + Englisch Support

## Installer verteilen

Nach dem Build kannst du verteilen:
- `installer_output\AutoClip-OCR_Setup.exe` (~18 MB)

### GitHub Release:
1. Gehe zu: https://github.com/DancingTedDanson011/AutoClip-OCR/releases/new
2. Tag: `v1.0`
3. Title: `AutoClip-OCR v1.0`
4. Upload: `AutoClip-OCR_Setup.exe`
5. Beschreibung aus README kopieren

## Troubleshooting

### "Inno Setup nicht gefunden"
- Installiere Inno Setup 6 von: https://jrsoftware.org/isdl.php
- Standard-Installationspfad verwenden

### "EXE nicht gefunden"
- Führe zuerst `build.bat` aus
- Stelle sicher `dist/OCR_ClipText.exe` existiert

### Installer startet nicht
- Antivirus prüfen (kann Installer blockieren)
- Als Administrator ausführen

## Installer-Größe

- Setup.exe: ~18-19 MB
- Enthält: AutoClip-OCR.exe + README + LICENSE + Icon
- Benötigt NICHT Python (alles gebündelt)
