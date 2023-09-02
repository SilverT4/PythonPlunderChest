# inspired by those dumb tiktoks. made graphical because i felt like it.
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk # ttkthemes
from time import sleep
from functools import partial
from pathlib import Path
from playsound import playsound # playsound
from winsound import PlaySound,SND_ASYNC,SND_FILENAME
from threading import Thread
clickSound = "..\\random-sounds\\clickfast.wav" # if running in VS Code or another editor like it, ensure you're running from the scripts directory, not the base git directory
root = ThemedTk(theme="kroc",themebg=1,toplevel=1,background=1) # yes i know kroc is terrible. this isn't a professional script
root.title("Jet Roulette")
incVar = IntVar()
pvar = IntVar()
results = ["You stay dry this time. Nice job!","You got a shower! ...Hope you weren't wearing any expensive clothes!","You got the cone. Enjoy it.","OH NO! YOU GOT THE JET!!","You got a nice mist. Not bad.","All from the centre of that nozzle. At least it wasn't the jet.","Damn, you got SOAKED.","You got a spray that's flatter than I am. Nice."]
settings = ["Off","Shower","Cone","Jet","Mist","Centre","Soaker","Flat"]
cursor = 0

def show_result():
    resTitle = settings[cursor]
    resText = results[cursor]
    root.children['load'].destroy() # remove the previous toplevel
    tl = Toplevel()
    tl.title(f"You landed on {resTitle}!")
    tlFrame = Frame(tl)
    tlFrame.grid()
    Label(tlFrame,text=resText).grid()
    def reset():
        print("resetting")
        pvar.set(0)
        tl.destroy()
    controlFrame = Frame(tlFrame)
    controlFrame.grid()
    Label(controlFrame,text="What would you like to do?").grid(column=0)
    Button(controlFrame,text="Play again",command=reset).grid(row=0,column=1)
    Button(controlFrame,text="Quit",command=quit).grid(row=0,column=2)
def roulette(inc:int):
    global cursor
    def piss():
        PlaySound(clickSound,SND_FILENAME)
    tiddy = Thread(target=piss)
    for _ in range(inc):
        cursor += 1
        if cursor == 8:
            cursor = 0
        root.update()
        playsound(clickSound)
        pvar.set(pvar.get()+1)

    show_result()

def pass_the_cheese():
    tl = Toplevel(name="load")
    tl.title("Setting the shit...")
    tlFrame = Frame(tl)
    tlFrame.grid()
    inc = incVar.get()
    Label(tlFrame,text=f"You chose to rotate {inc} {'times' if inc != 1 else 'time'}. Let's see what you get...").grid(row=0)
    Progressbar(tlFrame,variable=pvar,maximum=inc).grid(row=1)
    tl.after(100,partial(roulette,inc))


jrFrame = Frame()
jrFrame.grid()
Label(jrFrame,text="Jet Roulette",underline=12).grid(row=0,columnspan=2)
Label(jrFrame,text="Rotate count:").grid(row=1,column=0)
Spinbox(jrFrame,textvariable=incVar,from_=0,to=99,increment=1).grid(row=1,column=1)
Button(jrFrame,text="Spin!",command=pass_the_cheese).grid(row=2,columnspan=2,sticky='we')

root.mainloop()
