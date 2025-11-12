# AutoClip-OCR 📸✨

<div align="center">

![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.8+-green)

**Fast, lightweight screenshot OCR tool for Windows with hotkey support**

[Features](#-features) • [Download](#-download) • [Installation](#-installation) • [Usage](#-usage) • [Building](#-building-from-source)

</div>

---

## 🎯 Overview

AutoClip-OCR is a lightweight Windows application that lets you capture text from anywhere on your screen using OCR (Optical Character Recognition). Just press a hotkey, select an area, and the text is automatically copied to your clipboard!

Perfect for:
- 📄 Extracting text from images or PDFs
- 🎮 Copying text from games or apps that don't allow text selection
- 📊 Grabbing data from screenshots
- 🌐 Extracting text from videos or presentations
- 📱 Converting text from mobile screenshots

---

## ✨ Features

- ⌨️ **Global Hotkey** - Press `Ctrl+Alt+S` from anywhere to start capturing
- 🚀 **Instant OCR** - Powered by Tesseract OCR for accurate text recognition
- 📋 **Auto-Copy** - Text is automatically copied to clipboard after recognition
- 🎨 **Visual Selection** - Snipping Tool-style overlay for precise area selection
- 🔔 **Notifications** - Clean, non-intrusive toast notifications
- ⚡ **Lightweight** - Runs silently in the background
- 🔄 **Auto-Start** - Optional Windows startup integration
- 🌍 **Multi-Language** - Support for English, German, and many more languages

---

## 📥 Download

### Option 1: Direct Download (Easiest)

Download the standalone executable directly from the repository:

**[⬇️ Download OCR_ClipText.exe](https://github.com/DancingTedDanson011/AutoClip-OCR/raw/main/dist/OCR_ClipText.exe)** (18.3 MB)

Just download and run - no installation needed!

### Option 2: With Installer (Coming Soon)

A full installer with guided setup will be available in [Releases](https://github.com/DancingTedDanson011/AutoClip-OCR/releases).

Want to build the installer yourself? See [INSTALLER_BUILD.md](INSTALLER_BUILD.md)

### Requirements

- Windows 10/11
- **Tesseract OCR** (required) - [Download here](https://github.com/UB-Mannheim/tesseract/wiki)

---

## 🛠️ Installation

### Step 1: Install Tesseract OCR

1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run `tesseract-ocr-w64-setup-5.x.x.exe`
3. During installation:
   - ✅ Keep all default options
   - ✅ **Important**: Select **Additional language data** if you want to recognize non-English text
     - For German: Select "German" in the language list
     - For multiple languages: Select all needed languages

### Step 2: Run AutoClip-OCR

1. [Download OCR_ClipText.exe](https://github.com/DancingTedDanson011/AutoClip-OCR/raw/main/dist/OCR_ClipText.exe) (direct link)
2. Double-click to run
3. The app will start in the background (look for the notification)
4. ✅ Done! Press `Ctrl+Alt+S` to use it

**Note**: Windows Defender may show a warning for downloaded .exe files. Click "More info" → "Run anyway" (the app is safe, it's just unsigned).

### Auto-Start (Optional)

The app automatically adds itself to Windows startup on first run. To disable:
- Press `Win + R`, type `shell:startup`, and delete the AutoClip-OCR shortcut

---

## 🎮 Usage

### Basic Workflow

1. **Activate** - Press `Ctrl+Alt+S` anywhere on Windows
2. **Select** - Click and drag to create a rectangle around the text
3. **Done** - Text is automatically recognized and copied to clipboard
4. **Paste** - Use `Ctrl+V` to paste the text anywhere

### Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Alt+S` | Start screenshot OCR mode |
| `ESC` | Cancel current selection |
| Left-click + Drag | Select area to OCR |

### Tips for Best Results

- 📏 **Select tightly** around the text for better accuracy
- 🔆 **Good contrast** - Dark text on light background works best
- 📐 **Straight text** - Horizontal text is recognized better than rotated
- 🔍 **Size matters** - Larger text = better recognition

---

## ⚙️ Configuration

### Change Hotkey

Edit `ocr_snip.py`, line 18:

```python
HOTKEY = "ctrl+alt+s"  # Change to your preferred combination
```

Examples:
- `"ctrl+shift+s"`
- `"alt+x"`
- `"ctrl+alt+c"`

### Change OCR Language

Edit `ocr_snip.py`, line 19:

```python
OCR_LANG = "eng"        # English only
# OCR_LANG = "deu"      # German only
# OCR_LANG = "deu+eng"  # German + English
```

**Note**: Language data must be installed in Tesseract!

---

## 🏗️ Building from Source

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Tesseract OCR installed

### Quick Start

```bash
# Clone repository
git clone https://github.com/DancingTedDanson011/AutoClip-OCR.git
cd AutoClip-OCR

# Install dependencies
pip install -r requirements.txt

# Run from source
python ocr_snip.py
```

### Build Executable

```bash
# Build .exe
python -m PyInstaller --clean --noconfirm ocr_snip.spec

# Output: dist/OCR_ClipText.exe
```

---

## 📂 Project Structure

```
AutoClip-OCR/
├── ocr_snip.py              # Main application
├── ocr_snip.spec            # PyInstaller build config
├── app_icon.ico             # Application icon
├── requirements.txt         # Python dependencies
├── LICENSE                  # CC BY-NC 4.0 License
├── README.md                # This file
└── dist/                    # Built executable (after build)
    └── OCR_ClipText.exe
```

---

## 🐛 Troubleshooting

### "Tesseract OCR not found"

**Solution**: Install Tesseract OCR (see [Installation](#-installation))

If still not found after installation, manually set the path in `ocr_snip.py`:

```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

### "No text recognized"

- ✅ Try selecting a larger area
- ✅ Ensure text has good contrast
- ✅ Check that the correct language is configured
- ✅ Verify Tesseract language pack is installed

### Hotkey not working

- ✅ Check if another app is using the same hotkey
- ✅ Try running as Administrator
- ✅ Change the hotkey in configuration

### App won't start

- ✅ Install [Visual C++ Redistributable](https://aka.ms/vs/17/release/vc_redist.x64.exe)
- ✅ Check antivirus didn't block the .exe
- ✅ Ensure Python dependencies are installed (if running from source)

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

### Development Setup

```bash
git clone https://github.com/DancingTedDanson011/AutoClip-OCR.git
cd AutoClip-OCR
pip install -r requirements.txt
```

### Running Tests

```bash
# Test the application
start.bat
```

---

## 📜 License

This project is licensed under the **Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0)**.

**You are free to:**
- ✅ Use the software for personal, educational, or non-commercial purposes
- ✅ Share and redistribute
- ✅ Modify and adapt

**You must:**
- ℹ️ Give appropriate credit
- ℹ️ Indicate if changes were made

**You cannot:**
- ❌ Use for commercial purposes

See [LICENSE](LICENSE) for full details.

### Third-Party Software

This project uses:
- **Tesseract OCR** (Apache 2.0)
- **Pillow** (HPND)
- **pytesseract** (Apache 2.0)
- **pyperclip** (BSD)
- **keyboard** (MIT)
- **pywin32** (PSF)

All third-party licenses permit non-commercial use.

---

## 🙏 Acknowledgments

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - The OCR engine powering text recognition
- [PyInstaller](https://www.pyinstaller.org/) - For creating standalone executables
- All open-source contributors and maintainers

---

## 📞 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/DancingTedDanson011/AutoClip-OCR/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/DancingTedDanson011/AutoClip-OCR/issues)
- 📖 **Documentation**: See [README.md](README.md)

---

<div align="center">

**Made with ❤️ for the open-source community**

⭐ Star this repo if you find it useful!

</div>
