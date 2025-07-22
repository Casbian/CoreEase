
import tkinter
import modules

ROOT = tkinter.Tk()
ROOT.title("Device Management Console")
ROOT.geometry("500x500")
ROOT.resizable(False,False)
ROOT.iconbitmap(default="root\\ui\\assets\\uiicon.ico")
THREADPOOL = modules.ThreadPool.INIT()



import sqlite3

conn = sqlite3.connect('mydatabase.db')
cursor = conn.cursor()

#cursor.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)')
#cursor.execute('INSERT INTO users (name) VALUES (?)', ('Alice',))
#conn.commit()

cursor.execute('SELECT * FROM users')
print(cursor.fetchall())

conn.close()
















ROOT.mainloop()
modules.ThreadPool.SHUTDOWN(THREADPOOL)
exit()