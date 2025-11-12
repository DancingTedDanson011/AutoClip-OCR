; AutoClip-OCR Installer Script für Inno Setup 6
; https://jrsoftware.org/isinfo.php

#define MyAppName "AutoClip-OCR"
#define MyAppVersion "1.0"
#define MyAppPublisher "DancingTedDanson"
#define MyAppURL "https://github.com/DancingTedDanson011/AutoClip-OCR"
#define MyAppExeName "OCR_ClipText.exe"

[Setup]
AppId={{B3E9C8D1-7F2A-4E5B-9C3D-8A1F4E6B2D9C}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=installer_output
OutputBaseFilename=AutoClip-OCR_Setup
SetupIconFile=app_icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[CustomMessages]
german.WelcomeLabel2=Willkommen beim AutoClip-OCR Installer!%n%nDieses Programm ermöglicht es Ihnen, Text von überall auf Ihrem Bildschirm zu kopieren - auch wenn der Text nicht markierbar ist.%n%nWie funktioniert's?%n1. Drücken Sie Strg+Alt+S%n2. Markieren Sie den gewünschten Bereich%n3. Der Text wird automatisch erkannt und kopiert%n%nWas ist OCR?%nOCR (Optical Character Recognition) ist eine Technologie, die Text in Bildern erkennt und in bearbeitbaren Text umwandelt. Perfekt für Screenshots, PDFs oder eingescannte Dokumente!%n%nWICHTIG: Tesseract OCR wird benötigt (siehe nächster Schritt)
english.WelcomeLabel2=Welcome to the AutoClip-OCR installer!%n%nThis program allows you to copy text from anywhere on your screen - even when the text is not selectable.%n%nHow it works:%n1. Press Ctrl+Alt+S%n2. Select the desired area%n3. Text is automatically recognized and copied%n%nWhat is OCR?%nOCR (Optical Character Recognition) is a technology that recognizes text in images and converts it into editable text. Perfect for screenshots, PDFs or scanned documents!%n%nIMPORTANT: Tesseract OCR is required (see next step)

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startmenu"; Description: "Verknüpfung im Startmenü erstellen / Create Start Menu shortcut"; GroupDescription: "Startmenü / Start Menu:"; Flags: checkedonce
Name: "startup"; Description: "Automatisch mit Windows starten (empfohlen) / Auto-start with Windows (recommended)"; GroupDescription: "Autostart:"; Flags: checkedonce

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "LICENSE"; DestDir: "{app}"; Flags: ignoreversion
Source: "app_icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: startmenu
Name: "{group}\README"; Filename: "{app}\README.md"; Tasks: startmenu
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"; Tasks: startmenu
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{#MyAppName} jetzt starten / Start {#MyAppName} now"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: startup

[UninstallRun]
Filename: "{cmd}"; Parameters: "/C taskkill /F /IM {#MyAppExeName} /T"; Flags: runhidden

[Code]
var
  TesseractPage: TOutputMsgWizardPage;

procedure InitializeWizard;
var
  TesseractInstalled: Boolean;
  TesseractPath: String;
begin
  // Tesseract-Hinweis-Seite
  TesseractPage := CreateOutputMsgPage(wpWelcome,
    'Tesseract OCR benötigt / Tesseract OCR Required',
    'AutoClip-OCR benötigt Tesseract OCR',
    'AutoClip-OCR verwendet Tesseract OCR zur Texterkennung.' + #13#10 + #13#10 +
    'Was ist Tesseract?' + #13#10 +
    'Tesseract ist eine kostenlose Open-Source OCR-Engine, die Text in Bildern erkennt.' + #13#10 + #13#10 +
    'WICHTIG: Tesseract muss separat installiert werden!' + #13#10 + #13#10 +
    'Download: https://github.com/UB-Mannheim/tesseract/wiki' + #13#10 +
    'Datei: tesseract-ocr-w64-setup-5.x.x.exe' + #13#10 + #13#10 +
    'Nach der Installation von AutoClip-OCR:' + #13#10 +
    '1. Installieren Sie Tesseract OCR' + #13#10 +
    '2. Wählen Sie bei der Installation "German" (für deutsche Texte)' + #13#10 +
    '3. Starten Sie AutoClip-OCR neu' + #13#10 + #13#10 +
    'AutoClip-OCR funktioniert NICHT ohne Tesseract!' + #13#10 + #13#10 +
    '---' + #13#10 + #13#10 +
    'AutoClip-OCR requires Tesseract OCR for text recognition.' + #13#10 + #13#10 +
    'What is Tesseract?' + #13#10 +
    'Tesseract is a free open-source OCR engine that recognizes text in images.' + #13#10 + #13#10 +
    'IMPORTANT: Tesseract must be installed separately!' + #13#10 + #13#10 +
    'Download: https://github.com/UB-Mannheim/tesseract/wiki' + #13#10 +
    'File: tesseract-ocr-w64-setup-5.x.x.exe' + #13#10 + #13#10 +
    'After installing AutoClip-OCR:' + #13#10 +
    '1. Install Tesseract OCR' + #13#10 +
    '2. Select "German" during installation (for German texts)' + #13#10 +
    '3. Restart AutoClip-OCR' + #13#10 + #13#10 +
    'AutoClip-OCR will NOT work without Tesseract!');

  // Prüfe ob Tesseract installiert ist
  TesseractInstalled := RegQueryStringValue(HKLM, 'SOFTWARE\Tesseract-OCR', 'InstallDir', TesseractPath);
  if not TesseractInstalled then
    TesseractInstalled := RegQueryStringValue(HKLM64, 'SOFTWARE\Tesseract-OCR', 'InstallDir', TesseractPath);

  if not TesseractInstalled then
  begin
    // Zeige Warnung wenn Tesseract nicht gefunden wurde
    if MsgBox('Tesseract OCR wurde nicht auf Ihrem System gefunden!' + #13#10 + #13#10 +
              'AutoClip-OCR benötigt Tesseract OCR um zu funktionieren.' + #13#10 + #13#10 +
              'Möchten Sie die Tesseract-Download-Seite jetzt öffnen?' + #13#10 + #13#10 +
              '---' + #13#10 + #13#10 +
              'Tesseract OCR was not found on your system!' + #13#10 + #13#10 +
              'AutoClip-OCR requires Tesseract OCR to work.' + #13#10 + #13#10 +
              'Do you want to open the Tesseract download page now?',
              mbConfirmation, MB_YESNO) = IDYES then
    begin
      ShellExec('open', 'https://github.com/UB-Mannheim/tesseract/wiki', '', '', SW_SHOW, ewNoWait, TesseractInstalled);
    end;
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ResultCode: Integer;
begin
  // Beende laufende Instanz
  Exec('taskkill', '/F /IM {#MyAppExeName} /T', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Result := '';
end;
