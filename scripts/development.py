# Script to try and work out problems in shit. This will be updated frequently.
from pathlib import Path
from winsound import PlaySound,SND_FILENAME
from tkinter import *
from tkinter import ttk

t=Tk()
t.title("sound player thingy")
soundDir = Path("../random-sounds")
slist = [p for p in soundDir.iterdir()]
sounds = []
for item in slist:
    if item.is_file(): sounds.append(item.name) # ignore directories
    elif item.is_dir(): 
        slist.extend([p for p in item.iterdir()])
        sounds.extend(["{0}/{1}".format(p.parent.name,p.name) for p in item.iterdir()])
def getfile():
    ret = None
    for i in slist:
        if not "/" in svar.get():
            if i.name == svar.get():
                ret = i
                break
        else:
            if "{0}/{1}".format(i.parent.name,i.name) == svar.get():
                ret = i
                break
    return ret
def playfile():
    f=getfile()
    if not f:
        print("it returned none noooooo",svar.get())
    else:
        PlaySound(f.resolve().as_posix(),SND_FILENAME)
svar = StringVar(value="scroll pls lmao")
pp = ttk.OptionMenu(t,svar,"scroll pls",*sounds)
pp.grid()
b = ttk.Button(text="play",command=playfile)
b.grid(row=0,column=1)
t.mainloop()