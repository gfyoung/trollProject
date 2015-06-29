from os import system, remove
from subprocess import call

target = open("displaySuccess.py", 'w')
target.write("""
from Tkinter import Label, Tk

root = Tk()
label = Label(root, text = "Success!")

label.pack()
root.mainloop()
""")
target.close()

CREATE_NO_WINDOW = 0x08000000
call("python displaySuccess.py", creationflags = CREATE_NO_WINDOW)
call("rm displaySuccess.py", creationflags = CREATE_NO_WINDOW)
