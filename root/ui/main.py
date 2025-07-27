##==================================================##
## DISCLAIMER
##==================================================##

##==================================================##
## IMPORTS
##==================================================##
import tkinter
from tkinter import messagebox
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

    #Login Button Assets
    BLI = tkinter.PhotoImage(file="root\\ui\\assets\\buttonlogin.png")
    BLIH = tkinter.PhotoImage(file="root\\ui\\assets\\buttonloginhover.png")
    BLIP = tkinter.PhotoImage(file="root\\ui\\assets\\buttonloginpressed.png")
    #Login Button Placement and Binds
    BL = tkinter.Button(master=BGL,image=BLI,relief="flat",bg="black",activebackground="black",border=0,command=lambda:LOGINUSERTODMC(BGL,ID,PASSWORD))
    BL.image = BLI  #Keeps in Reference
    BL.place(relx=0.336,rely=0.7)
    def BLENTER(event):
        BL.configure(image=BLIH)
    def BLLEAVE(event):
        BL.configure(image=BLI)
    def BLPRESS(event):
        BL.configure(image=BLIP)
    def BLRELEASE(event):
        BL.configure(image=BLIH)
    BL.bind("<Enter>", BLENTER)
    BL.bind("<Leave>", BLLEAVE)
    BL.bind("<ButtonPress-1>", BLPRESS)
    BL.bind("<ButtonRelease-1>", BLRELEASE)

    #Close Button Assets
    BCI = tkinter.PhotoImage(file="root\\ui\\assets\\buttonclose.png")
    BCIH = tkinter.PhotoImage(file="root\\ui\\assets\\buttonclosehover.png")
    BCIP = tkinter.PhotoImage(file="root\\ui\\assets\\buttonclosepressed.png")
    #Close Button Placement and Binds
    BC = tkinter.Button(master=BGL,image=BCI,relief="flat",bg="#000000",activebackground="#000000",border=0,command=lambda:ROOT.quit())
    BC.image = BCI  #Keeps in Reference
    BC.place(relx=0.92,rely=0.03)
    def BLENTER(event):
        BC.configure(image=BCIH)
    def BLLEAVE(event):
        BC.configure(image=BCI)
    def BLPRESS(event):
        BC.configure(image=BCIP)
    def BLRELEASE(event):
        BC.configure(image=BCIH)
    BC.bind("<Enter>", BLENTER)
    BC.bind("<Leave>", BLLEAVE)
    BC.bind("<ButtonPress-1>", BLPRESS)
    BC.bind("<ButtonRelease-1>", BLRELEASE)

    #Entry Fields
    ELU = tkinter.Entry(master=BGL,relief="flat",bg="#FFFFFF",fg="#000000",border=0,width=24,font=("ClashGrotesk",14,"bold"),justify="left")
    ELU.place(relx=0.23,rely=0.39)
    ELU.insert(0, "ID")   #Entry USER Default
    ELP = tkinter.Entry(master=BGL,relief="flat",bg="#FFFFFF",fg="#000000",border=0,width=24,font=("ClashGrotesk",14,"bold"),justify="left",show="*")
    ELP.place(relx=0.23,rely=0.525)
    ELP.insert(0, "PASSWORD")   #Entry PASSWORD Default


    ID = ELU.get()
    PASSWORD = ELP.get()

def LOGINUSERTODMC(BGL,ID,PASSWORD):
    #Clean LOGINWINDOW
    BGL.destroy()
    #ROOT Window Changes
    ROOT.overrideredirect(False)
    ROOT.attributes("-topmost", False)
    ROOT.state('zoomed')
    ROOT.resizable(True,True)

    #Login Logic

    MAINWINDOW()

def MAINWINDOW():
    #Create Menu Bar
    MENUBAR = tkinter.Menu(master=ROOT)
    #Device Menu
    DEVICEMENU = tkinter.Menu(MENUBAR, tearoff=1)
    #AD Menu
    ADMENU = tkinter.Menu(MENUBAR, tearoff=1)
    #SQL Menu
    SQLMENU = tkinter.Menu(MENUBAR, tearoff=1)
    #Toolbox Menu
    TOOLBOXMENU = tkinter.Menu(MENUBAR, tearoff=1)
    TOOLBOXMENU.add_command(label="🔧 DHCP [local]", command=lambda:STARTDHCP())
    def STARTDHCP():
        ANSWER = tkinter.messagebox.askokcancel("🔧 DHCP [local]","ℹ️INFORMATION\nThis will start a crude local Powershell DHCP Server.\nDHCP Servers provide IP's and Network Information.\n\nYou can change DHCP Settings in:\nroot\\sys\\modules\\DHCP.ps1\n\n⚠️WARNING\nDo not change DHCP Handshake Structure:\n📢 Discover\n📬 Offer\n📦 Request\n✅ ACK\n\n⚠️WARNING\nThis will change your Ethernet Adapter IP and DNS Settings.\nInternet Connection can get cut.")
        if ANSWER:
            subprocess.run(["powershell.exe", "-File", "root\\sys\\modules\\DHCP.ps1"])
    TOOLBOXMENU.add_command(label="🔧 TFTP [local]", command=lambda:STARTTFTP())
    def STARTTFTP():
        ANSWER = tkinter.messagebox.askokcancel("🔧 TFTP [local]","ℹ️INFORMATION\nThis will start a crude local Powershell TFTP Server.\nTFTP Servers provide FileTransfer\n\nYou can change TFTP Settings in:\nroot\\sys\\modules\\TFTP.ps1\n\n⚠️WARNING\nTFTP Message Codes:\n🗂️ 1- RRQ\n🗂️ 2- WRQ\n📁 3- DATA\n✅ 4- ACK\n❌ 5- ERROR\n🔒 6- RFC 2347+ OPTIONS\n\n⚠️WARNING\nThis will permanently listen on Port 69 until stopped.")
        if ANSWER:
            subprocess.run(["powershell.exe", "-File", "root\\sys\\modules\\TFTP.ps1"])
    #Add Menus to Bar
    MENUBAR.add_cascade(label="🖥️ Device", menu=DEVICEMENU)
    MENUBAR.add_cascade(label="🗃️ Active Directory", menu=ADMENU)
    MENUBAR.add_cascade(label="🧰 Toolbox", menu=TOOLBOXMENU)
    ROOT.configure(menu=MENUBAR)
    #Background Asset
    BG = tkinter.PhotoImage(file="root\\ui\\assets\\uibgmain.png")
    #Background Holder Label
    BGL = tkinter.Label(master=ROOT,image=BG)
    BGL.image = BG  #Keeps in Reference
    BGL.place(relx=0,rely=0,relheight=1,relwidth=1)
    















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