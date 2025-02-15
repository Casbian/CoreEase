#=========================================================================
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