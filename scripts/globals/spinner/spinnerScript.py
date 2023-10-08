from tkinter import Misc
from PIL import Image
from PIL.Image import Image as Dick
from PIL.ImageTk import PhotoImage
import os
SPINNERPATH=os.path.abspath(__file__).removesuffix("spinnerScript.py")
class spinner:
    def __init__(self):
        self.sprites:list[Dick] = []
        for i in range(43):
            shit = Image.open("{1}/spinner go brr00{0}.png".format("0" + str(i) if i < 10 else str(i),SPINNERPATH))
            self.sprites.append(shit)
        self.curSprite = 0
    def doSpin(self,image:PhotoImage,size:tuple[int,int]):
        spr = self.sprites[self.curSprite % 43]
        image.paste(spr.resize(size))
        self.curSprite += 1
    def reset(self): self.curSprite = 0