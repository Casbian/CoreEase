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
$rrqListener = New-Object System.Net.Sockets.UdpClient 69
$rrqEndpoint = New-Object System.Net.IPEndPoint ([IPAddress]::Any, 0)
Write-Host "[*] TFTP server listening on UDP 69" -ForegroundColor Cyan
while ($true) {
    $received = $rrqListener.Receive([ref]$rrqEndpoint)
    if ($received.Length -lt 4 -or $received[1] -ne 1) {
        Write-Host "[!] Unsupported or malformed TFTP request." -ForegroundColor Red
        continue
    }
    $rawString = [System.Text.Encoding]::ASCII.GetString($received[2..($received.Length - 1)])
    $parts = $rawString.Split([char]0)
    $filename = $parts[0]; $mode = $parts[1]; $options = @{}
    for ($j=2; $j -lt $parts.Length -1; $j+=2) {
        if ($parts[$j] -and $parts[$j+1]) { $options[$parts[$j].ToLower()] = $parts[$j+1] }
    }
    Write-Host "[>] TFTP GET: $filename (mode: $mode)" -ForegroundColor Yellow
    Write-Host "[DEBUG] Options: $($options.Keys -join ', ')" -ForegroundColor Yellow
    $filepath = Join-Path "C:\PXE" $filename
    if (-not (Test-Path $filepath)) {
        $err = @(0,5,0,1) + [System.Text.Encoding]::ASCII.GetBytes("File not found") + 0
        $rrqListener.Send([byte[]]$err, $err.Length, $rrqEndpoint)
        Write-Host "[!] File not found: $filename" -ForegroundColor Red
        continue
    }
    $transferSocket = New-Object System.Net.Sockets.UdpClient 0
    $localEP = $transferSocket.Client.LocalEndPoint
    Write-Host "[DEBUG] Sending from local port: $($localEP.Port)" -ForegroundColor Yellow
    $clientEP = New-Object System.Net.IPEndPoint $rrqEndpoint.Address, $rrqEndpoint.Port
    $data = [System.IO.File]::ReadAllBytes($filepath)
    $blksize = 512; $windowsize = 1
    if ($options.ContainsKey("blksize")) {
        $val = [int]$options["blksize"]
        if ($val -ge 8 -and $val -le 65464) { $blksize = $val }
    }
    if ($options.ContainsKey("windowsize")) {
        $win = [int]$options["windowsize"]
        if ($win -ge 1 -and $win -le 64) { $windowsize = $win }
    }
    Write-Host "[DEBUG] Using blksize: $blksize" -ForegroundColor Yellow
    Write-Host "[DEBUG] Using windowsize: $windowsize" -ForegroundColor Yellow
    if ($options.Count -gt 0) {
        foreach ($opt in $options.GetEnumerator()) { Write-Host "[DEBUG] Client requested option: $($opt.Key)=$($opt.Value)" -ForegroundColor Yellow }
        $oack = [System.Collections.Generic.List[byte]]::new(); $oack.AddRange([byte[]](0,6))
        foreach ($key in $options.Keys) {
            switch ($key) {
                "blksize" { $value = $blksize.ToString() }
                "tsize" { $value = $data.Length.ToString() }
                "timeout" { $value = "2" }
                "windowsize" { $value = $windowsize.ToString() }
                default { continue }
            }
            $oack.AddRange([System.Text.Encoding]::ASCII.GetBytes($key)); $oack.Add(0)
            $oack.AddRange([System.Text.Encoding]::ASCII.GetBytes($value)); $oack.Add(0)
            Write-Host "[DEBUG] OACK -> $key=$value" -ForegroundColor Yellow
        }
        $transferSocket.Send($oack.ToArray(), $oack.Count, $clientEP)
        Write-Host "[DEBUG] OACK sent, waiting for ACK(0)" -ForegroundColor Yellow
        try {
            $ack = $transferSocket.Receive([ref]$clientEP)
            $ackHex = ($ack | ForEach-Object { "{0:X2}" -f $_ }) -join ' '
            Write-Host "[DEBUG] Received from $($clientEP.Address):$($clientEP.Port) → $ackHex" -ForegroundColor Yellow
            if ($ack[1] -ne 4 -or $ack[2] -ne 0 -or $ack[3] -ne 0) {
                Write-Host "[!] Invalid ACK for OACK" -ForegroundColor Red
                $transferSocket.Close()
                continue
            }
        } catch {
            Write-Host "[!] OACK ACK timeout" -ForegroundColor Red
            $transferSocket.Close()
            continue
        }
    }
    $block = 1; $i = 0
    while ($i -lt $data.Length) {
        for ($w = 0; $w -lt $windowsize -and $i -lt $data.Length; $w++) {
            $chunkLen = [Math]::Min($blksize, $data.Length - $i)
            $chunk = $data[$i..($i+$chunkLen-1)]
            $high = [byte](($block -shr 8) -band 0xFF); $low = [byte]($block -band 0xFF)
            $header = [byte[]](0,3,$high,$low); $packet = $header + $chunk
            $transferSocket.Send($packet, $packet.Length, $clientEP)
            Write-Host "[DEBUG] Sent block $block, size $chunkLen" -ForegroundColor Yellow
            $i += $chunkLen
            if ($block -lt 0xFFFF) { $block++ } else { $block = 1 }
        }
        try {
            $ack = $transferSocket.Receive([ref]$clientEP)
            $ackHex = ($ack | ForEach-Object { "{0:X2}" -f $_ }) -join ' '
            Write-Host "[DEBUG] Received from $($clientEP.Address):$($clientEP.Port) → $ackHex" -ForegroundColor Yellow
            if ($ack.Length -lt 4) { Write-Host "[!] ACK too short" -ForegroundColor Red; break }
            $opcode = $ack[1]; $ackBlock = ($ack[2] -shl 8) + $ack[3]
            if ($opcode -eq 4) {
                Write-Host "[DEBUG] ACK block $ackBlock" -ForegroundColor Yellow
            } elseif ($opcode -eq 5) {
                $errCode = ($ack[2] -shl 8) + $ack[3]
                $errMsg = [System.Text.Encoding]::ASCII.GetString($ack[4..($ack.Length-2)])
                Write-Host ("[!] TFTP ERROR {0}: {1}" -f $errCode,$errMsg) -ForegroundColor Red; break
            } else { Write-Host "[!] Unknown opcode: $opcode" -ForegroundColor Red; break }
        } catch {
            Write-Host "[!] ACK timeout or error." -ForegroundColor Red; break
        }
    }
    if ($data.Length % $blksize -eq 0) {
        $high = [byte](($block -shr 8) -band 0xFF); $low = [byte]($block -band 0xFF)
        $final = [byte[]](0,3,$high,$low)
        $transferSocket.Send($final, $final.Length, $clientEP)
        Write-Host "[DEBUG] Sent final empty block $block" -ForegroundColor Yellow
        try {
            $ack = $transferSocket.Receive([ref]$clientEP)
            $ackHex = ($ack | ForEach-Object { "{0:X2}" -f $_ }) -join ' '
            Write-Host "[DEBUG] Final ACK → $ackHex" -ForegroundColor Yellow
        } catch {
            Write-Host "[!] Final ACK timeout." -ForegroundColor DarkYellow
        }
    }
    $transferSocket.Close()
    Write-Host "[✓] Done: $filename" -ForegroundColor Green
}
