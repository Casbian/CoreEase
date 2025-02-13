#=========================================================================
    # CONSOLE // SHELL
def CMD_HEIGHT():
    import shutil
    consoleheight = shutil.get_terminal_size().lines
    return consoleheight
def CMD_WIDTH():
    import shutil
    consolewidth = shutil.get_terminal_size().columns
    return consolewidth
def CMD_CLEAR():
    import os
    os.system("cls")
def CMD_COMMAND(command:str):
    import os
    os.system(command)
#=========================================================================
    # TIME
def TIME_WAIT(second:int):
    import time
    time.sleep(second)
def TIME_CURRENT():
    import time
    import datetime
    time = datetime.datetime.now()
    return time
def TIME_DIFFERENCE_WITHIN_24_HOUR(targettime:str):
    import datetime
    currenttime = TIME_CURRENT()
    try:
        targettime = datetime.datetime.combine(currenttime.date(),datetime.datetime.strptime(targettime,"%H:%M").time())
    except (ValueError,TypeError):
        return "Error try Format: str(%H:%M)"
    timedifference = targettime - currenttime
    return timedifference
#=========================================================================
    # ENVIRONMENT VARIABLE
def ENV_CPUCOUNT():
    import os
    cpucount = os.cpu_count()
    return cpucount
def ENV_GET(key:str):
    import os
    value = os.environ.get(key)
    return value
def ENV_GETALL():
    import os
    variablelist = []
    keys = ['USERPROFILE', 'APPDATA', 'LOCALAPPDATA', 'TEMP', 'PATH', 'HOMEDRIVE', 'HOMEPATH','PROGRAMFILES', 'PROGRAMFILES(X86)', 'SYSTEMROOT', 'COMSPEC', 'LOGNAME', 'COMPUTERNAME','PROCESSOR_IDENTIFIER', 'SYSTEMDRIVE', 'WINDIR', 'OS', 'USERDOMAIN', 'USERNAME','PROMPT', 'SESSIONNAME', 'LOGONSERVER']
    for x in keys:
        value = os.environ.get(x)
        variablelist.append(x,value)
    return variablelist
#=========================================================================
    # SYSTEM DIRECT
def SYS_SHUTDOWN(time:int):
    import os
    os.system(f'shutdown /s /f /t {time}')
def SYS_RESTART(time:int):
    import os
    os.system(f'shutdown /r /f /t {time}')
#=========================================================================