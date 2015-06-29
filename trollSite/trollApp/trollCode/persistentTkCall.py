from os import system, remove
from subprocess import call

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

CREATE_NO_WINDOW = 0x08000000
call("python persistentTk.py", creationflags = CREATE_NO_WINDOW)
call("rm persistentTk.py", creationflags = CREATE_NO_WINDOW)
