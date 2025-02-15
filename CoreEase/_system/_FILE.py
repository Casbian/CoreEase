#=========================================================================
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