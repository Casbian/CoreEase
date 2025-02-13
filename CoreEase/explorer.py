#=========================================================================
    # FILE
def FILE_RENAME(oldname:str,newname:str):
    import os
    os.rename(oldname,newname)
def FILE_EXIST(file:str):
    import os
    if os.path.exists(file):
        return True
    else:
        return False
def FILE_CREATE(file:str):
    explorer = open(file, "w")
    explorer.write("")
    explorer.close()
def FILE_DELETE(file:str):
    import os
    os.remove(file)
def FILE_READ(file:str):
    explorer = open(file, "r")
    content = explorer.read()
    explorer.close()
    return content
def FILE_APPEND(file:str,content:str):
    explorer = open(file, "a")
    explorer.write(content + "\n")
    explorer.close()
def FILE_WRITE(file:str,content:str):
    explorer = open(file, "w")
    explorer.write(content + "\n")
    explorer.close()
#=========================================================================
    # DIRECTORY
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
    # PATH
def PATH_JOIN(path:str,path2:str):
    import os
    r = os.path.join(path,path2)
    return r
#=========================================================================