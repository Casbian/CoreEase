##==================================================##
## MAIN SCRIPT
##==================================================##
if (-not ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Start-Process -FilePath "powershell.exe" -ArgumentList "-File `"$PSCommandPath`"" -Verb RunAs
    exit
}
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public class ConsoleHelper {
    const int STD_INPUT_HANDLE = -10;
    const uint ENABLE_QUICK_EDIT = 0x0040;
    const uint ENABLE_EXTENDED_FLAGS = 0x0080;
    [DllImport("kernel32.dll", SetLastError = true)]
    static extern IntPtr GetStdHandle(int nStdHandle);
    [DllImport("kernel32.dll")]
    static extern bool GetConsoleMode(IntPtr hConsoleHandle, out uint lpMode);
    [DllImport("kernel32.dll")]
    static extern bool SetConsoleMode(IntPtr hConsoleHandle, uint dwMode);
    public static void DisableQuickEdit() {
        IntPtr consoleHandle = GetStdHandle(STD_INPUT_HANDLE);
        uint mode;
        if (!GetConsoleMode(consoleHandle, out mode)) return;
        mode &= ~ENABLE_QUICK_EDIT;
        mode |= ENABLE_EXTENDED_FLAGS;
        SetConsoleMode(consoleHandle, mode);
    }
}
"@
[ConsoleHelper]::DisableQuickEdit();
$Host.UI.RawUI.BackgroundColor = "Black";
Clear-Host;
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$INSTALLERPATH = Join-Path $ScriptDir "root\\sys\\assets\\InstallerPython.exe"
$FONTDIR = Join-Path $ScriptDir "root\ui\fonts"
$FONTFILES = Get-ChildItem -Path $FONTDIR -Include *.ttf, *.otf -Recurse
Start-Process -FilePath $INSTALLERPATH -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1" -Wait
foreach ($FONT in $FONTFILES) {
    $DEST = Join-Path -Path $env:WINDIR\Fonts -ChildPath $FONT.Name
    if (-not (Test-Path $DEST)) {
        Copy-Item -Path $FONT.FullName -Destination $DEST
        $FONTREG = "HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Fonts"
        $EXT = $FONT.Extension.ToLower()
        if ($EXT -eq ".ttf") {
            $FONTNAME = $FONT.BaseName + " (TrueType)"
        } elseif ($EXT -eq ".otf") {
            $FONTNAME = $FONT.BaseName + " (OpenType)"
        } else {
            continue
        }
        New-ItemProperty -Path $FONTREG -Name $FONTNAME -PropertyType String -Value $FONT.Name -Force | Out-Null
    }
}
