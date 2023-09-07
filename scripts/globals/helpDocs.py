from os import PathLike,sep
from typing import Any
from sys import argv
from tkinter import *
from tkinter.ttk import *

class Parameter():
    """
    Python class to represent a parameter.

    Variables:
    * str `name` - Self-explanatory.
    * dict `description` - Self-explanatory.
    """
    def __init__(self,name:str,description:Any):
        """
        Initializes the Parameter object.

        Arguments:
        * str `name` - Self-explanatory. (Required: Yes)
        * str `description` - Self-explanatory. (Required: Yes)
        """
        self.name = name
        self.description = description
    def __repr__(self):
        return f'{self.name} - {self.description}'
    def __str__(self)->str:
        return f"{self.name} - {self.description}"
class HelpDocumentation():
    """
    Python class which represents help documentation for a class. This is meant to make it easier for me to show help documentation in a script.

    Variables:
    * str `title` - This is set automatically by the calling script. It shows up in the Tk window if `-g` is specified in `sys.argv`.
    * str `description` - This is set automatically by the calling script. It's just the script description and help.
    * list `params` - This is set automatically by the calling script. It's a list of accepted parameters that can be added when running the script via command line.

    Methods:
    * `printHelp()` - Called if `-g` is not specified in `sys.argv` when calling the script. Prints the help text to the current terminal.
    * `showHelp()` - Called if `-g` is specified in `sys.argv`. Shows the help text in a Tkinter window. (Hence why I import tkinter stuff in the file for the documentation.)
    * `outFile(file)` - Called if `-o` is specified in `sys.argv` along with a file path. Raises a `ValueError` if no file path is specified.
    """
    def __init__(self,title:str,desc:str,params:list[dict[str,str]]):
        self.title = title
        self.description = desc
        self.params = [Parameter(**p) for p in params]

    def do(self,args:list):
        if args[0] == '-g':
            self.showHelp()
        elif args[0] == '-o':
            if len(args[1:]) >0:
                self.outFile(" ".join(args[1:]))
            else:
                raise ValueError("No file name provided.")
    def printHelp(self):
        print(self.description,*self.params)
    
    def showHelp(self):
        hroot = Tk()
        hroot.title(self.title)
        Label(text=f'Help for {self.title}',image="::tk::icons::information",compound='left').grid(columnspan=2)
        sb_x = Scrollbar(orient='horizontal')
        sb_y = Scrollbar(orient='vertical')
        txt = Text(height=15,width=100,xscrollcommand=sb_x.set,yscrollcommand=sb_y.set)
        txt.insert(END,self.description+"\n\n")
        for parm in self.params:
            txt.insert(END,str(parm)+'\n')
        txt['state'] = 'disabled'
        txt.grid(row=1,column=0)
        sb_x.configure(command=txt.xview)
        sb_y.configure(command=txt.yview)
        sb_x.grid(row=2,column=0,sticky='new')
        sb_y.grid(row=1,column=1,sticky='nsw')
        Button(text='OK',command=quit).grid(row=3,columnspan=2)
        hroot.mainloop()
    
    def outFile(self,file:int|str|bytes|PathLike[str]|PathLike[bytes]=None):
        print(file)
        if file.startswith("-o"):
            file = file.removeprefix("-o")
        if file:
            f=open(file.removeprefix(" "),"w") # the removeprefix is to remove any extra spaces in front of it
            f.write(self.description+'\n\n')
            for parm in self.params:
                f.write(str(parm)+'\n')
            f.flush() # idk if close does flush and im too lazy to google it
            f.close()
        else:
            raise ValueError("File parameter is None, cannot save file.")

hd = HelpDocumentation("Python Plunder Chest Help","Holds a Python class which represents help documentation for a class. This is meant to make it easier for me to show help documentation in a script.",[{"name": "-g","description": "Tells the script calling the class to show a Tkinter window."},{"name":"-o <filepath>","description":"Tells the script calling the class to output the help contents to a file. Raises an exception if filepath is not specified."}])
if '-g' in argv:
    hd.showHelp()
elif '-o' in argv:
    assert argv != ['helpDocs.py','-o'], "No file path was specified."
    hd.outFile(" ".join(argv[2:])) # uses 2: as index to get all remaining shit