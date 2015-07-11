from os import system, remove
from subprocess import call

target = open("massiveFileWrite.py", 'w')
target.write("""
from os import chdir, mkdir
from Tkinter import Label, Tk
from webbrowser import open_new_tab

troll_song = "https://www.youtube.com/watch?v=o1eHKf-dMwo"

root = Tk()
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()

label = Label(root,
              text = 'LOL! Trolled You!',
              font = "Verdana 100 bold",
              height = screen_height,
              width = screen_width)

open_new_tab(troll_song)

folder_name = "Important Files"

try:
    mkdir(folder_name)
except: #directory has already been made
    pass

try:
    chdir(folder_name)
except:
    pass

file_count = 500
num_times = 500

filename = 'Important File {}.txt'
message = 'You have been troll' + 'ol' * num_times + 'ed'

for index in xrange(1, file_count + 1):
    target = open(filename.format(index), 'w')
    target.write(message)
    target.close()
    
label.pack()
root.mainloop()
""")
target.close()

CREATE_NO_WINDOW = 0x08000000
call("python massiveFileWrite.py", creationflags = CREATE_NO_WINDOW)
call("rm massiveFileWrite.py", creationflags = CREATE_NO_WINDOW)
