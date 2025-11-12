@echo off
REM Build Installer für AutoClip-OCR

echo ========================================
echo  AutoClip-OCR - Installer Build
echo ========================================
echo.

REM Prüfe ob EXE existiert
if not exist "dist\OCR_ClipText.exe" (
    echo FEHLER: dist\OCR_ClipText.exe nicht gefunden!
    echo Bitte zuerst build.bat ausfuehren!
    pause
    exit /b 1
)

REM Prüfe ob Inno Setup installiert ist
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%INNO_PATH%" (
    set "INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
)

if not exist "%INNO_PATH%" (
    echo.
    echo FEHLER: Inno Setup 6 nicht gefunden!
    echo.
    echo Bitte installiere Inno Setup 6 von:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo Oder kompiliere den Installer manuell:
    echo 1. Oeffne installer.iss mit Inno Setup
    echo 2. Druecke F9 oder klicke "Compile"
    echo.
    pause
    exit /b 1
)

echo Inno Setup gefunden: %INNO_PATH%
echo.

REM Erstelle Output-Verzeichnis
if not exist "installer_output" mkdir installer_output

echo Kompiliere Installer...
echo.

"%INNO_PATH%" "installer.iss"

if errorlevel 1 (
    echo.
    echo FEHLER beim Kompilieren!
    pause
    exit /b 1
)

echo.
echo ========================================
echo  Installer erfolgreich erstellt!
echo ========================================
echo.
echo Datei: installer_output\AutoClip-OCR_Setup.exe
echo.
pause
