##==================================================##
## DISCLAIMER
##==================================================##

##==================================================##
## IMPORTS
##==================================================##
import tkinter
import modules
import subprocess
##==================================================##
## FUNCTIONS
##==================================================##
def LOGINWINDOW():
    #Background Width and Height
    BGW = 550
    BGH = 550
    #Background Asset
    BG = tkinter.PhotoImage(file="root\\ui\\assets\\uibglogin.png")
    #Background Holder Label
    BGL = tkinter.Label(master=ROOT,image=BG)
    BGL.image = BG  #Keeps in Reference
    BGL.place(relx=0,rely=0,relheight=1,relwidth=1)
    #ROOT Window Changes
    ROOT.geometry(f"{BGW}x{BGH}+{int((WIDTH/2)-BGW/2)}+{int((HEIGHT/2)-BGH/2)}")
    ROOT.overrideredirect(True)
    ROOT.attributes("-topmost", True)
    #Login Button Asset
    BLI = tkinter.PhotoImage(file="root\\ui\\assets\\buttonlogin.png")
    #Button and Entry Placement
    BL = tkinter.Button(master=BGL,image=BLI,relief="flat",bg="black",activebackground="black",border=0,command=lambda:LOGINUSERTODMC(BGL,USERNAME,PASSWORD))
    BL.image = BLI  #Keeps in Reference
    BL.place(relx=0.25,rely=0.65)
    ELU = tkinter.Entry(master=BGL,relief="flat",bg="white",fg="black",border=0,width=18,font=("Verdana",14,"bold"),justify="center")
    ELU.place(relx=0.26,rely=0.4)
    ELU.insert(0, "USER")   #Entry USER Default
    ELP = tkinter.Entry(master=BGL,relief="flat",bg="white",fg="black",border=0,width=18,font=("Verdana",14,"bold"),justify="center")
    ELP.place(relx=0.26,rely=0.51)
    ELP.insert(0, "PASSWORD")   #Entry PASSWORD Default
    USERNAME = ELU.get()
    PASSWORD = ELP.get()
def LOGINUSERTODMC(BGL,USERNAME,PASSWORD):
    #Clean LOGINWINDOW
    BGL.destroy()
    #ROOT Window Changes
    ROOT.overrideredirect(False)
    ROOT.attributes("-topmost", False)
    ROOT.state('zoomed')

    #Login Logic

    MAINWINDOW()

def MAINWINDOW():
    #Create Menu Bar
    MENUBAR = tkinter.Menu(master=ROOT)
    #Main Menu
    MAINMENU = tkinter.Menu(MENUBAR, tearoff=1)
    MAINMENU.add_command(label="Connect | New AD", command=lambda:ROOT.quit())
    MAINMENU.add_command(label="Connect | New SQL DB", command=lambda:ROOT.quit())
    MAINMENU.add_separator()
    MAINMENU.add_command(label="Exit", command=lambda:ROOT.quit())
    #Device Menu
    DEVICEMENU = tkinter.Menu(MENUBAR, tearoff=1)
    #AD Menu
    ADMENU = tkinter.Menu(MENUBAR, tearoff=1)
    #SQL Menu
    SQLMENU = tkinter.Menu(MENUBAR, tearoff=1)
    #DHCP Menu
    DHCPMENU = tkinter.Menu(MENUBAR, tearoff=1)
    DHCPMENU.add_command(label="Local | Start Powershell DHCP", command=lambda:subprocess.Popen(["start", "powershell.exe", "-File", "root\\sys\\modules\\DHCP.ps1"], shell=True))
    #TFTP Menu
    TFTPMENU = tkinter.Menu(MENUBAR, tearoff=1)
    TFTPMENU.add_command(label="Local | Start Powershell TFTP", command=lambda:subprocess.run(["powershell.exe", "-File", "root\\sys\\modules\\TFTP.ps1"]))
    #Add Menus to Bar
    MENUBAR.add_cascade(label="Main", menu=MAINMENU)
    MENUBAR.add_cascade(label="Device", menu=DEVICEMENU)
    MENUBAR.add_cascade(label="Active Directory", menu=ADMENU)
    MENUBAR.add_cascade(label="SQL Database", menu=SQLMENU)
    MENUBAR.add_cascade(label="PXE | DHCP", menu=DHCPMENU)
    MENUBAR.add_cascade(label="PXE | TFTP", menu=TFTPMENU)
    ROOT.configure(menu=MENUBAR)
















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