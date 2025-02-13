#=========================================================================
 # NORMAL
def N_PRINT(string:str):
    print(string)
def N_INPUT(string:str):
    input(string)
def N_ENUMERATED_PRINT(list:list):
    for x,y in enumerate(list):
        print(x + y)
#=========================================================================
 # CENTERED
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
# MESSAGEBOX
def MB_INFO(title:str,message:str):
    import tkinter.messagebox
    tkinter.messagebox.showinfo(title,message)
def MB_WARNING(title:str,message:str):
    import tkinter.messagebox
    tkinter.messagebox.showwarning(title,message)
def MB_ERROR(title:str,message:str):
    import tkinter.messagebox
    tkinter.messagebox.showerror(title,message)
#=========================================================================