from platform import uname
from subprocess import call


def getPlatform():
    return uname()[0]

target = open("displaySuccess.py", 'w')
target.write("""
from Tkinter import Label, Tk

root = Tk()
label = Label(root, text = "Success!")

label.pack()
root.mainloop()
""")
target.close()

if getPlatform() == "Windows":
    CREATE_NO_WINDOW = 0x08000000
    call(["python", "displaySuccess.py"], creationflags=CREATE_NO_WINDOW)
    call(["rm", "displaySuccess.py"], creationflags=CREATE_NO_WINDOW)

else:
    call(["python", "displaySuccess.py"])
    call(["rm", "displaySuccess.py"])
