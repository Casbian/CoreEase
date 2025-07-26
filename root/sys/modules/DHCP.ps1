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
function NextFreeIP {
    $startBytes = $IPRangeStart.GetAddressBytes()
    $endBytes   = $IPRangeEnd.GetAddressBytes()
    for ($a = $startBytes[0]; $a -le $endBytes[0]; $a++) {
        for ($b = $startBytes[1]; $b -le $endBytes[1]; $b++) {
            for ($c = $startBytes[2]; $c -le $endBytes[2]; $c++) {
                for ($d = $startBytes[3]; $d -le $endBytes[3]; $d++) {
                    $ip = "$a.$b.$c.$d"
                    if (-not ($Leases.Values | Where-Object { $_.IP.ToString() -eq $ip })) {
                        return [IPAddress]$ip
                    }
                }
            }
        }
    }
    return $null
}
function BuildDHCPOffer {
    param (
        [byte[]]$Request,
        [IPAddress]$ClientIP
    )
    $transactionID = [byte[]]$Request[4..7]
    $mac = [byte[]]$Request[28..33]
    $packet = [System.Collections.Generic.List[byte]]::new()
    $packet.AddRange([byte[]](0x02, 0x01, 0x06, 0x00))
    $packet.AddRange($transactionID)                 
    $packet.AddRange([byte[]](0x00, 0x00, 0x00, 0x00)) 
    $packet.AddRange(([IPAddress]"0.0.0.0").GetAddressBytes()) 
    $packet.AddRange($ClientIP.GetAddressBytes())              
    $packet.AddRange(([IPAddress]$ServerIP).GetAddressBytes())  
    $packet.AddRange([byte[]](0x00, 0x00, 0x00, 0x00))          
    $chaddr = New-Object byte[] 16
    [Array]::Copy($mac, 0, $chaddr, 0, 6)
    $packet.AddRange($chaddr)
    $packet.AddRange([byte[]](0..191 | ForEach-Object { 0 }))
    $packet.AddRange([byte[]](99, 130, 83, 99))
    $packet.AddRange([byte[]](53, 1, 2))
    $packet.AddRange([byte[]](1, 4))
    $packet.AddRange($SubnetMask)
    $packet.AddRange([byte[]](3, 4))
    $packet.AddRange(([IPAddress]$ServerIP).GetAddressBytes())
    $packet.AddRange([byte[]](51, 4))
    $leaseBytes = [BitConverter]::GetBytes([System.Net.IPAddress]::HostToNetworkOrder($LeaseTime))
    $packet.AddRange($leaseBytes)
    $packet.AddRange([byte[]](54, 4))
    $packet.AddRange(([IPAddress]$ServerIP).GetAddressBytes())
    $tftpBytes = [System.Text.Encoding]::ASCII.GetBytes($TFTPServerIP)
    $packet.AddRange([byte[]](66, $tftpBytes.Length))
    $packet.AddRange($tftpBytes)
    $bootfileBytes = [System.Text.Encoding]::ASCII.GetBytes($BootFileName)
    $packet.AddRange([byte[]](67, $bootfileBytes.Length))
    $packet.AddRange($bootfileBytes)
    $packet.Add(255)
    return $packet.ToArray()
}
function BuildDHCPAck {
    param (
        [byte[]]$Request,
        [IPAddress]$ClientIP
    )
    $transactionID = [byte[]]$Request[4..7]
    $mac = [byte[]]$Request[28..33]
    $packet = [System.Collections.Generic.List[byte]]::new()
    $packet.AddRange([byte[]](0x02, 0x01, 0x06, 0x00))  
    $packet.AddRange($transactionID)
    $packet.AddRange([byte[]](0x00, 0x00, 0x00, 0x00))
    $packet.AddRange(([IPAddress]"0.0.0.0").GetAddressBytes())
    $packet.AddRange($ClientIP.GetAddressBytes())
    $packet.AddRange(([IPAddress]$ServerIP).GetAddressBytes())
    $packet.AddRange([byte[]](0x00, 0x00, 0x00, 0x00))
    $chaddr = New-Object byte[] 16
    [Array]::Copy($mac, 0, $chaddr, 0, 6)
    $packet.AddRange($chaddr)
    $packet.AddRange([byte[]](0..191 | ForEach-Object { 0 }))
    $packet.AddRange([byte[]](99, 130, 83, 99))
    $packet.AddRange([byte[]](53, 1, 5))
    $packet.AddRange([byte[]](1, 4))
    $packet.AddRange($SubnetMask)
    $packet.AddRange([byte[]](3, 4))
    $packet.AddRange(([IPAddress]$ServerIP).GetAddressBytes())
    $packet.AddRange([byte[]](51, 4))
    $leaseBytes = [BitConverter]::GetBytes([System.Net.IPAddress]::HostToNetworkOrder($LeaseTime))
    $packet.AddRange($leaseBytes)
    $packet.AddRange([byte[]](54, 4))
    $packet.AddRange(([IPAddress]$ServerIP).GetAddressBytes())
    $tftpBytes = [System.Text.Encoding]::ASCII.GetBytes($TFTPServerIP)
    $packet.AddRange([byte[]](66, $tftpBytes.Length))
    $packet.AddRange($tftpBytes)
    $bootfileBytes = [System.Text.Encoding]::ASCII.GetBytes($BootFileName)
    $packet.AddRange([byte[]](67, $bootfileBytes.Length))
    $packet.AddRange($bootfileBytes)
    $packet.Add(255)
    return $packet.ToArray()
}

# ===================================
# CONFIGURATION Variables Network_OWN
# ===================================
$interface = "Ethernet"
$ip = "10.10.10.1"
$prefix = 24
$gateway = "10.10.10.1"
$dns = "192.168.178.1"
# ===================================
# ===================================
try {
    New-NetIPAddress -InterfaceAlias $interface -IPAddress $ip -PrefixLength $prefix -DefaultGateway $gateway -AddressFamily IPv4 -ErrorAction Stop
    Write-Host "[✓] IP Setup Success" -ForegroundColor Green
} catch {
    Write-Host "[!] IP Setup WARNING - IP already set" -ForegroundColor Yellow
}
Set-DnsClientServerAddress -InterfaceAlias $interface -ServerAddresses $dns
Write-Host "[✓] DNS Setup Success" -ForegroundColor Green
# ====================================
# CONFIGURATION Variables Network_DHCP
# ====================================
$ServerIP      = $ip
$SubnetMask    = [byte[]](255,255,255,0)
$LeaseTime     = 3600
$IPRangeStart  = [IPAddress]"10.10.10.10"
$IPRangeEnd    = [IPAddress]"10.10.10.40"
$BootFileName  = "bootx64.efi"
$TFTPServerIP  = $ServerIP
$Leases        = @{}
# ====================================
# ====================================
$udpClient = New-Object System.Net.Sockets.UdpClient 67
$udpClient.Client.SetSocketOption([System.Net.Sockets.SocketOptionLevel]::Socket, [System.Net.Sockets.SocketOptionName]::ReuseAddress, $true)
$udpClient.Client.SetSocketOption([System.Net.Sockets.SocketOptionLevel]::Socket, [System.Net.Sockets.SocketOptionName]::Broadcast, $true)
$endpoint = New-Object System.Net.IPEndPoint ([IPAddress]::Any, 0)
Write-Host "[*] DHCP Server started on $ServerIP (port 67)" -ForegroundColor Cyan
while ($true) {
    $received = $udpClient.Receive([ref]$endpoint)
    $mac = -join ($received[28..33] | ForEach-Object { "{0:X2}" -f $_ })
    $msgType = $received[242]
    if ($msgType -eq 1) {
        Write-Host "[>] DHCPDISCOVER from $mac" -ForegroundColor Yellow
        $ipToAssign = NextFreeIP
        if ($ipToAssign) {
            $offer = BuildDHCPOffer -Request $received -ClientIP $ipToAssign
            $remoteEP = New-Object System.Net.IPEndPoint ([IPAddress]"255.255.255.255", 68)
            $udpClient.Send($offer, $offer.Length, $remoteEP)
            $Leases[$mac] = @{ IP = $ipToAssign; Time = (Get-Date) }
            Write-Host "[+] DHCPOFFER $ipToAssign to $mac" -ForegroundColor Cyan
        } else {
            Write-Host "IP not available" -ForegroundColor Yellow
        }
    }
    if ($msgType -eq 3) {
        Write-Host "[>] DHCPREQUEST from $mac" -ForegroundColor Yellow
        if ($Leases.ContainsKey($mac)) {
            $ack = BuildDHCPAck -Request $received -ClientIP $Leases[$mac].IP
            $remoteEP = New-Object System.Net.IPEndPoint ([IPAddress]"255.255.255.255", 68)
            $udpClient.Send($ack, $ack.Length, $remoteEP)
            Write-Host "[✓] DHCPACK sent to $mac for $($Leases[$mac].IP)" -ForegroundColor Green
        }
    }
}