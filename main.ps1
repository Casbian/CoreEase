##==================================================##
## MAIN SCRIPT
##==================================================##

# Initialize UI
$INSTALLERPATH = "root\\sys\\assets\\InstallerPython.exe"
$UIINITIALIZE = $false
while (-not $UIINITIALIZE) {
    try {
        python.exe "root\\ui\\main.py"
        $UIINITIALIZE = $true
    }
    catch {
        Start-Process -FilePath $INSTALLERPATH -ArgumentList "/quiet InstallAllUsers=1 PrependPath=1 Include_test=0 Include_pip=1" -Wait
    }
}