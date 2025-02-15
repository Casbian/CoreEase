#=========================================================================
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