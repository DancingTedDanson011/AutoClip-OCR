@echo off
REM Start script für OCR ClipText (Test-Version)

echo ========================================
echo  OCR ClipText - Test Start
echo ========================================
echo.

REM Prüfe ob Python installiert ist
python --version >nul 2>&1
if errorlevel 1 (
    echo FEHLER: Python nicht gefunden!
    echo Bitte installiere Python von python.org
    pause
    exit /b 1
)

REM Prüfe ob Dependencies installiert sind
echo Pruefe Dependencies...
pip show pytesseract >nul 2>&1
if errorlevel 1 (
    echo Dependencies nicht vollstaendig installiert!
    echo Installiere jetzt...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo FEHLER beim Installieren!
        pause
        exit /b 1
    )
    echo.
    echo Installation abgeschlossen!
)

echo.
echo Starte OCR ClipText...
echo.
echo Hotkey: STRG+ALT+S
echo Zum Beenden: STRG+C
echo.
echo ========================================
echo.

REM Starte das Python-Skript
python ocr_snip.py

echo.
echo Programm beendet.
pause
