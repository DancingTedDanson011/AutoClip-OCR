# PyInstaller spec for OCR ClipText

block_cipher = None

# Only the really required packages
excludes = [
    'torch', 'torchvision', 'torchaudio',
    'tensorflow', 'tensorboard',
    'scipy', 'pandas', 'numpy',  # Pillow doesn't need NumPy
    'matplotlib', 'seaborn',
    'pytest', 'unittest',
    'IPython', 'jupyter',
    'boto3', 'botocore',
    'sklearn', 'transformers',
    'grpc', 'google',
    'cryptography',
    'lxml', 'xml',
]

a = Analysis(
    ['ocr_snip_v2.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL._tkinter_finder',
        'win32timezone',
        'pystray._win32',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=excludes,
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OCR_ClipText',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app_icon.ico',
    version_file=None,
)
