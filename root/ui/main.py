
import tkinter
import modules

ROOT = tkinter.Tk()
ROOT.title("Device Management Console")
ROOT.geometry("500x500")
ROOT.resizable(False,False)
ROOT.iconbitmap(default="root\\ui\\assets\\uiicon.ico")
THREADPOOL = modules.ThreadPool.INIT()


















ROOT.mainloop()
modules.ThreadPool.SHUTDOWN(THREADPOOL)
exit()