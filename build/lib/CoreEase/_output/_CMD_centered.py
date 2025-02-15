#=========================================================================
def C_PRINT(string:str,filler:str):
    import shutil
    console_w = shutil.get_terminal_size().columns
    print(string.center(console_w,filler))
def C_TEMP_PRINT(string:str,filler:str):
    import shutil
    console_w = shutil.get_terminal_size().columns
    print(string.center(console_w,filler),end="\r")
def C_INPUT(string:str):
    import shutil
    console_w = shutil.get_terminal_size().columns
    console_lp = console_w // 2 - (len(string)+2)
    x = input(" " * console_lp + string + " " * 5)
    return x
def C_ENUMERATED_PRINT(list:list):
    import shutil
    console_w = shutil.get_terminal_size().columns
    for x,y in enumerate(list):
        print(x + y.center(console_w," "))
#=========================================================================