; Inno Setup Script für OCR ClipText
; Benötigt Inno Setup 6.x: https://jrsoftware.org/isdl.php

#define MyAppName "OCR ClipText"
#define MyAppVersion "1.0"
#define MyAppPublisher "Your Name"
#define MyAppURL "https://github.com/yourusername/ocr-cliptext"
#define MyAppExeName "OCR_ClipText.exe"

[Setup]
AppId={{A8F9E3D2-1B4C-4E6F-9A2D-7C8B3E5F1A9C}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=
OutputDir=installer_output
OutputBaseFilename=OCR_ClipText_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "startup"; Description: "Automatisch mit Windows starten"; GroupDescription: "Autostart:"; Flags: checkedonce

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
; Füge hier weitere Dateien hinzu falls nötig

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Starte die App nach Installation
Filename: "{app}\{#MyAppExeName}"; Description: "{#MyAppName} jetzt starten"; Flags: nowait postinstall skipifsilent

[Registry]
; Autostart Registry-Eintrag (nur wenn Task ausgewählt)
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "{#MyAppName}"; ValueData: """{app}\{#MyAppExeName}"""; Flags: uninsdeletevalue; Tasks: startup

[UninstallRun]
; Beende laufende Instanz vor Deinstallation
Filename: "{cmd}"; Parameters: "/C taskkill /F /IM {#MyAppExeName} /T"; Flags: runhidden

[Code]
// Prüfe ob Tesseract installiert ist und warne ggf.
function InitializeSetup(): Boolean;
var
  TesseractPath: String;
  ResultCode: Integer;
begin
  Result := True;

  // Prüfe ob Tesseract installiert ist
  if not RegQueryStringValue(HKLM, 'SOFTWARE\Tesseract-OCR', 'InstallDir', TesseractPath) then
  begin
    if not RegQueryStringValue(HKLM64, 'SOFTWARE\Tesseract-OCR', 'InstallDir', TesseractPath) then
    begin
      if MsgBox('Tesseract OCR wurde nicht gefunden.' + #13#10 + #13#10 +
                'OCR ClipText benötigt Tesseract OCR um zu funktionieren.' + #13#10 + #13#10 +
                'Möchten Sie Tesseract jetzt herunterladen?',
                mbConfirmation, MB_YESNO) = IDYES then
      begin
        ShellExec('open', 'https://github.com/tesseract-ocr/tesseract/releases', '', '', SW_SHOW, ewNoWait, ResultCode);
      end;
    end;
  end;
end;

// Beende laufende Instanz vor Installation
function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  ResultCode: Integer;
begin
  Exec('taskkill', '/F /IM {#MyAppExeName} /T', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Result := '';
end;
