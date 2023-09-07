from datetime import datetime
from functools import partial
from random import randint
from sys import argv
from os import path
from time import sleep
from tkinter import *
from tkinter.ttk import *
from traceback import format_exc, print_exc
from urllib.request import urlretrieve
from winsound import MessageBeep
from threading import Thread,ThreadError
from globals.helpDocs import HelpDocumentation
from globals.relativeTime import relative2 as rt
from PIL import Image, ImageTk
from spotify.album import Album
from spotify.artist import Artist
from spotify.contextTyper import contextObject
from spotify.length import milliseconds_to_hms as tlength
from spotify.player import Context, Player
from spotify.playlist import Playlist
from spotify.podcast import Episode, Show
from spotify.SpotifyClient import cli
from spotify.track import Track
from spotify.user import User
from spotipy.exceptions import SpotifyException
from ttkthemes import ThemedTk

acceptedArguments = [{"name": "--clean", "description": "Utility with which to clean up the IMG_CACHE folder of the script's directory.\n\nAdd --continue as an argument to open the widget after cleanup."}, {"name": "--force-redownloads", "description": "Force the script to redownload album/show cover images every time, instead of using the cache."}, {"name": "--use-context","description": "When updating the now playing widget, set the title to use the name of the current context object, instead of the current track or episode title."}, {"name": "<no arguments>", "description": "Run with no parameters to use the widget itself."}]
helpDoc = HelpDocumentation("Spotify Playback Widget", "Silly little Python script that displays your currently playing song/podcast in a little window at the bottom right of your screen.\nThe window resizes automatically when the song/podcast data changes, and also updates the elapsed time automatically.\nYou can also change its appearance to any theme supported by `ThemedTk` by right clicking anywhere in the main window.",acceptedArguments)
class SpotiWidget(ThemedTk):
    """
    Custom subclass of `ThemedTk` to represent the Spotify Playback Widget. Additional arguments come from `sys.argv`, meaning you'd have to run this through the command line to use them.

    Use the `--help` argument to display help.
    """
    def __init__(self, theme:str|None = ..., *extraArgs, **extraKeys) -> None:
        """```markdown
        Initialize the Spotify Display Widget
        
        Command-line arguments are listed in `acceptedArguments`, and here:
        
        * `--force-redownload` - **Not recommended with the way this widget is coded at the moment.** Forces the widget to redownload album/show images on *every* update.
        * `--use-context` - Sets the widget's titlebar to the current context's object name if applicable.
        ```
        """
        super().__init__(screenName=None, baseName=None, className="deez nuts", useTk=1, sync=1, use=None, theme=theme, toplevel=1, themebg=1, background=1, gif_override=1)

        self.title("Spotify Display Widget")
        self.resizable(0,0)
        self.bind("<Configure>",self.adjust_self) # Makes it move to the bottom right automatically
        self.wm_attributes('-topmost',1)

        self.mainframe = Frame(self)
        self.mainframe.grid()

        self.svar = StringVar(self)

        self.mainimage = ImageTk.PhotoImage(Image.open("../gagababy.png").resize((64,64)))
        self.mainlabel = Label(self.mainframe,textvariable=self.svar,image=self.mainimage,compound='left')
        self.mainlabel.image = self.mainimage
        self.mainlabel.grid()

        self.pbar = Progressbar(self.mainframe)
        self.pbar.grid(sticky='we')

        self.spot:Player = None
        self.now_playing:Track|Episode = None
        self.context:Context = None
        self.ctxObject:Artist|Album|Show|Playlist = None
        self.CURRENT_TRACKID:str = None

        self.download_mode = "cache" if "--force-redownload" not in extraArgs else "forced"
        self.cur_file = ""

        self.DownloadWindow = Toplevel(self)
        self.DownloadWindow.title("Download progress")
        self.DL_FRAME = Frame(self.DownloadWindow)
        self.DL_PBAR = Progressbar(self.DownloadWindow)
        self.DL_LBL = Label(self.DownloadWindow,text="Downloading track image, please wait...",image="::tk::icons::information",compound='left')
        self.DL_FRAME.grid()
        self.DL_PBAR.grid(row=1)
        self.DL_LBL.grid(row=0)
        self.DownloadWindow.withdraw()

        # These threads were a suggestion when I was using ChatGPT to try and figure out how to stop the application from freezing so much
        self.updateThread = Thread(target=self.refresh_spot)
        self.updateThread.daemon = True
        self.updateThread.start()

        self.updThr2 = Thread(target=self.imgtest)
        self.updThr2.daemon = True
        self.updThr2.start()

        self.bell()

        self.extraArgs = extraArgs

        self.updThr3 = Thread(target=self.contextUpdate)
        self.updThr3.daemon = True
        self.updThr3.start()
        self.after(1000,self.refresh_view)

        self.rcMenu = Menu(tearoff=0)
        for theme in self.themes:
            self.rcMenu.add_radiobutton(label=theme,value=theme,variable=self.current_theme,command=partial(self.set_theme,theme,1,1))
        self.bind("<Button-3>",lambda a: self.rcMenu.tk_popup(a.x_root,a.y_root))

    def contextUpdate(self):
        if self.context and '--use-context' in self.extraArgs:
            ctx = contextObject(self.context.type,self.context.id or self.context.uri)
            self.title(ctx.name)
    def refresh_spot(self):
        while True:
            try:
                starttime=datetime.now()
                self.spot = Player(cli.current_playback())
                if self.spot.item:
                    self.now_playing = self.spot.item
                    self.CURRENT_TRACKID = self.now_playing.id
                else:
                    self.now_playing = None # Discard the previous item if nothing is available.
                if self.spot.context:
                    self.context = self.spot.context
                else:
                    self.context = None # Discard previous context.
                stoptime=datetime.now()
            except Exception:
                raise
            sleep(1)
            

    def refresh_view(self):
        try:
            if self.now_playing:
                NP = self.now_playing # for easy access lmao
                SP = self.spot
                PB = self.pbar
                #if self.CURRENT_TRACKID != NP.id or self.cur_file != NP.imgID: self.refresh_image()
                formatMe = NP.widgetText
                if SP.progress_ms:
                    formatMe += "\n{0} / {1}".format(tlength(SP.progress_ms), tlength(NP.duration_ms))
                    PB.configure(value=SP.progress_ms,maximum=NP.duration_ms)
                else:
                    PB.configure(value=randint(0,PB.cget('maximum')))
                self.svar.set(formatMe)
            else:
                self.svar.set("No playback information")
            self.update()
            self.after(1000,self.refresh_view)
        except BaseException:
            raise

    def DownloadProgress(self,c,b,t):
        print(c,b,t) # lmao
        prog = c*b
        self.DownloadWindow.wm_deiconify()
        if prog < t:
            self.DL_PBAR.configure(value=prog,maximum=t)
        else:
            self.after(250,self.DownloadWindow.withdraw) # Withdraw the window once download is complete.
    def imgtest(self):
        try:
            nut = Player(cli.current_playback())
        except:
            raise
        try:
            useContext = nut.context and '--use-context' in argv
            if nut:
                playerItem = nut.item
                if playerItem:
                    if not useContext: self.title(playerItem.name)
                    hasMedia = len(playerItem.album.images) > 0 if type(playerItem) == Track else len(playerItem.show.images) >0
                    if hasMedia:
                        sillyUrl = playerItem.album.images[0].url if type(playerItem) == Track else playerItem.show.images[0].url
                        sillyName = "IMG_CACHE/{0}.JPG".format(playerItem.id)
                        if not path.exists(sillyName) or self.download_mode == 'forced':
                            try:
                                urlretrieve(sillyUrl,sillyName,self.DownloadProgress)
                            except AttributeError or TypeError:
                                sillyName = "../gagababy.png"
                        fard = Image.open(sillyName)
                        self.mainimage.paste(fard.resize((64,64)))
                        self.wm_iconphoto(True,fard)
                else:
                    pass
        except TclError:
            pass
        self.after(1000,self.imgtest)
    
        try:
            self.wm_iconphoto(True,self.mainimage)
        except UnboundLocalError:
            self.wm_iconphoto(True,"::tk::icons::question")
    def refresh_image(self): # Focus on this one pls, gpt
        print('attempting to refresh image')
        if self.now_playing:
            if self.cur_file != self.now_playing.imgID:
                sillyPath = "IMG_CACHE/{0}.JPG".format(self.now_playing.imgID)
                if not path.exists(sillyPath) or self.download_mode == 'forced':
                    try:
                        urlretrieve(self.now_playing.image.url, sillyPath, self.DownloadProgress)
                    except AttributeError or TypeError:
                        sillyPath = "../gagababy.png"
                    
                tmpImage = Image.open(sillyPath)
                self.mainimage.paste(tmpImage.resize((64, 64)))
                self.cur_file = self.now_playing.imgID
        else:
            self.mainimage.paste(Image.open("../gagababy.png").resize((64, 64)))


                
    def adjust_self(self,a:Event):
        stx=self.winfo_screenwidth()-26
        y=self.winfo_screenheight()-126
        dum,ass = self.winfo_width(),self.winfo_height()
        stx -= dum
        y -= ass
        if [a.x,a.y] != [stx,y]:
            try:
                self.wm_geometry(f"+{stx}+{y}")
            except:
                pass
        else:
            print("deez",datetime.now())

dick = {}
for thing in ["screenName","baseName","className","useTk","sync","use"]:
    dick.__setitem__(thing,None)
if "--clean" in argv:
    root = Tk()
    root.title("SDW Image Cache")
    rootFrame = Frame(root)
    rootFrame.grid()
    def cleanup(s:Event=None):
        from os import chdir,remove,listdir
        from time import sleep
        from winsound import PlaySound,SND_FILENAME as sfn
        chdir("IMG_CACHE")
        files = listdir()
        lbl.configure(text="Now cleaning up the image cache folder...",image="::tk::icons::information")
        btYes.destroy()
        btNo.destroy()
        pbar = Progressbar(rootFrame,value=0,maximum=len(files))
        pbar.grid(row=1,columnspan=2)
        lmao = StringVar()
        Label(rootFrame,textvariable=lmao).grid(columnspan=2)
        lb = Listbox(rootFrame)
        for file in files:
            sleep(0.25)
            lmao.set(file)
            pbar.step()
            root.update()
            try:
                remove(file)
            except FileNotFoundError:
                print(f"COULD NOT FIND {file.upper()}, WAS IT DELETED MANUALLY??")
                PlaySound("../../random-sounds/mparty8_ballyhoo_09.wav",sfn)
            except PermissionError as egg:
                lb.insert(END,f"{egg.filename} could not be deleted.")
            finally:
                print(file)
        if not "--continue" in argv: quit() # Specify "--continue" in the CLI to open the widget proper after cleanup
    lbl = Label(rootFrame,text="By cleaning the image cache, image downloads may take longer to complete.\nDo you wish to continue?",image="::tk::icons::question",compound="top")
    lbl.grid(columnspan=2)
    btYes = Button(rootFrame,text='Yes',underline=1,command=cleanup)
    btYes.grid(row=1,column=0)
    btNo = Button(rootFrame,text='No',underline=1,command=quit)
    btNo.grid(row=1,column=1)
    root.bind("y",cleanup)
    root.bind("n",quit)
    root.mainloop()
    if not "--continue" in argv: quit() # Specify "--continue" in the CLI to open the widget proper after cleanup
    
if not "--help" in argv:
    spot = SpotiWidget(*argv,**dick,theme="scidmint",toplevel=1,themebg=1,background=1)
    spot.mainloop()
else:
    helpDoc.do(argv[2:])