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
$listener = [System.Net.HttpListener]::new()
$listener.Prefixes.Add("http://+:80/")
$listener.Start()
Write-Host "[*] HTTP server running at http://10.10.10.1:80/" -ForegroundColor Cyan
while ($listener.IsListening) {
    $context = $listener.GetContext()
    $request = $context.Request
    $response = $context.Response
    $path = "C:\PXE" + $request.Url.AbsolutePath
    if (Test-Path $path) {
        $bytes = [System.IO.File]::ReadAllBytes($path)
        $response.ContentLength64 = $bytes.Length
        $response.OutputStream.Write($bytes, 0, $bytes.Length)
        Write-Host "[>] Served: $($request.Url.AbsolutePath)" -ForegroundColor Green
    } else {
        $response.StatusCode = 404
        Write-Host "[!] 404: $($request.Url.AbsolutePath)" -ForegroundColor Red
    }
    $response.Close()
}