@echo off
REM Build script for OCR ClipText

echo ========================================
echo  OCR ClipText - Build Script
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

echo [1/4] Installiere Dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo FEHLER beim Installieren der Dependencies!
    pause
    exit /b 1
)
echo.

echo [2/4] Räume alte Builds auf...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
echo.

echo [3/4] Baue EXE mit PyInstaller...
pyinstaller --clean --noconfirm ocr_snip.spec
if errorlevel 1 (
    echo FEHLER beim Bauen der EXE!
    pause
    exit /b 1
)
echo.

echo [4/4] Kopiere Tesseract-Hinweis...
echo WICHTIG: Tesseract OCR muss installiert sein! > dist\TESSERACT_REQUIRED.txt
echo Download: https://github.com/tesseract-ocr/tesseract/releases >> dist\TESSERACT_REQUIRED.txt
echo.

echo ========================================
echo  Build erfolgreich!
echo ========================================
echo.
echo Die EXE befindet sich in: dist\OCR_ClipText.exe
echo.
echo Naechster Schritt: Installer bauen mit Inno Setup
echo   - Oeffne OCR_ClipText_Installer.iss mit Inno Setup
echo   - Klicke auf "Compile"
echo.
pause
