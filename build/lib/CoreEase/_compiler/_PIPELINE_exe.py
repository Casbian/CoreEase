#=========================================================================
 # COMPILER NUITKA
def COMPILER_NUITKA(compiler:str,filepath:str,modulepath:str|None,console:bool,tkinter:bool):
    import subprocess
    import sys
    import os
    compiler=compiler.strip().lower()
    if compiler not in ['msvc','mingw64']:
        print('✘Possible Compilers\n -MSVC\n -MINGW64')
    version=sys.version_info
    if version.major==3 and version.minor==13:
        if compiler=='mingw64':
            print('\n★Python 3.13 detected!\n - MinGW64 does NOT work with Python 3.13.\n - If you need MinGW64,downgrade to Python 3.12.\n✘Wrong Version')
    try:
        subprocess.run([sys.executable,'-m','nuitka','--version'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,check=True)
    except subprocess.CalledProcessError:
        subprocess.run([sys.executable,'-m','pip','install','--upgrade','nuitka'],check=True)
    if compiler=='msvc':
        MSVCInstalled=False
        possible_paths=[r'C:\Program Files (x86)\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC',r'C:\Program Files (x86)\Microsoft Visual Studio\2022\Professional\VC\Tools\MSVC',r'C:\Program Files (x86)\Microsoft Visual Studio\2022\Enterprise\VC\Tools\MSVC',r'C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC']
        for x in possible_paths:
            if os.path.exists(x) and os.listdir(x):
                MSVCInstalled=True
        if MSVCInstalled!=True:
            subprocess.run(['powershell','-Command',f'Invoke-WebRequest -Uri "https://aka.ms/vs/17/release/vs_BuildTools.exe" -OutFile "{os.path.join(os.environ.get("TEMP"),"vs_BuildTools.exe")}"'],shell=True)
            subprocess.run([os.path.join(os.environ.get('TEMP'),'vs_BuildTools.exe')],shell=True)
            COMPILER_NUITKA(compiler,filepath,modulepath,console,tkinter)
    if not os.path.isfile(filepath) or not filepath.endswith('.py'):
        print('✘File not found')
    options=['--standalone','--onefile','--lto=yes']
    if modulepath!=None:
        modulepath=modulepath.strip()
        options.append(f'--include-data-dir={modulepath}')
    if console==False:
        options.append('--no-console')
    if tkinter:
        options.append('--enable-plugin=tk-inter')
    compiler_flag='--msvc=latest' if compiler=='msvc' else ''
    script_dir=os.path.dirname(filepath)
    command="powershell","-Command",f'Start-Process PowerShell -Verb RunAs -Wait -ArgumentList \'-NoProfile -ExecutionPolicy Bypass -Command "cd {script_dir}; {sys.executable} -m nuitka {" ".join(options)} {compiler_flag} \"{filepath}\""\''
    subprocess.run(command,shell=True)
    print(f'✔Success\n - ✔{filepath} ->>> {script_dir}')
#=========================================================================