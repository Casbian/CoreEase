#=========================================================================
def DIR_CURRENT():
    import os
    directory = os.getcwd()
    return directory
def DIR_CHANGE(path:str):
    import os
    os.chdir(path)
def DIR_LISTALL(path:str):
    import os
    all = os.listdir(path)
    return all
def DIR_CREATE(directory:str):
    import os
    os.mkdir(directory)
def DIRS_CREATE(directorystructure:str):
    import os
    os.makedirs(directorystructure, exist_ok=True)
def DIR_DELETE(directory:str):
    import os
    os.rmdir(directory)  
def DIRS_DELETE(directorystructure:str):
    import os
    os.removedirs(directorystructure)
def DIR_NAME(directory:str):
    import os
    os.path.dirname(directory)
#=========================================================================