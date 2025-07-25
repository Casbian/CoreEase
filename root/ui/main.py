##==================================================##
## DISCLAIMER
##==================================================##

##==================================================##
## IMPORTS
##==================================================##
import tkinter
import modules

##==================================================##
## FUNCTIONS
##==================================================##
def LOGINWINDOW():
    BGW = 550
    BGH = 550
    BG = tkinter.PhotoImage(file="root\\ui\\assets\\uibglogin.png")
    BGL = tkinter.Label(master=ROOT,image=BG)
    BGL.image = BG
    BGL.place(relx=0,rely=0,relheight=1,relwidth=1)
    ROOT.geometry(f"{BGW}x{BGH}+{int((WIDTH/2)-BGW/2)}+{int((HEIGHT/2)-BGH/2)}")
    ROOT.overrideredirect(True)
    ROOT.attributes("-topmost", True)
    BLI = tkinter.PhotoImage(file="root\\ui\\assets\\buttonlogin.png")
    BL = tkinter.Button(master=BGL,image=BLI,relief="flat",bg="black",activebackground="black",border=0,command=lambda:LOGINUSERTODMC(BGL,USERNAME,PASSWORD))
    BL.image = BLI
    BL.place(relx=0.25,rely=0.65)
    ELU = tkinter.Entry(master=BGL,relief="flat",bg="white",fg="black",border=0,width=18,font=("Verdana",14,"bold"),justify="center")
    ELU.place(relx=0.26,rely=0.4)
    ELU.insert(0, "USER")
    ELP = tkinter.Entry(master=BGL,relief="flat",bg="white",fg="black",border=0,width=18,font=("Verdana",14,"bold"),justify="center")
    ELP.place(relx=0.26,rely=0.51)
    ELP.insert(0, "PASSWORD")
    USERNAME = ELU.get()
    PASSWORD = ELP.get()
def LOGINUSERTODMC(BGL,USERNAME,PASSWORD):
    BGL.destroy()
    ROOT.overrideredirect(False)
    ROOT.attributes("-topmost", False)
    ROOT.state('zoomed')
    print(USERNAME,PASSWORD)


##==================================================##
## MAIN BODY
##==================================================##
ROOT = tkinter.Tk()
WIDTH = ROOT.winfo_screenwidth()
HEIGHT = ROOT.winfo_screenheight()
ROOT.title("Device Management Console")
ROOT.resizable(False,False)
ROOT.iconbitmap(default="root\\ui\\assets\\uiicon.ico")

THREADPOOL = modules.ThreadPool.INIT()


LOGINWINDOW()



ROOT.mainloop()
modules.ThreadPool.SHUTDOWN(THREADPOOL)
exit()