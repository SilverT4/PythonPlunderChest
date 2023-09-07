from datetime import datetime
from tkinter import *
from tkinter.ttk import *
from traceback import format_exc, print_exc
from urllib.request import urlretrieve
from winsound import MessageBeep
from sys import argv
from globals.relativeTime import relative_time as rt
from PIL import Image, ImageTk
from spotify.album import Album
from spotify.artist import Artist
from spotify.contextTyper import contextObject
from spotify.length import milliseconds_to_hms as tlength
from spotify.player import Player
from spotify.playlist import Playlist
from spotify.podcast import Episode, Show
from spotify.SpotifyClient import cli
from spotify.track import Track
from spotify.user import User
from spotipy.exceptions import SpotifyException
from globals.helpDocs import HelpDocumentation
from ttkthemes import ThemedTk
acceptedArguments = [{"name": "--clean", "description": "Utility with which to clean up the IMG_CACHE folder of the script's directory."}, {"name": "--force-redownloads", "description": "Force the script to redownload album/show cover images every time, instead of using the cache."}, {"name": "--use-context","description": "When updating the now playing widget, set the title to use the name of the current context object, instead of the current track or episode title."}, {"name": "<no arguments>", "description": "Run with no parameters to use the widget itself."}]
helpDoc = HelpDocumentation("Spotify Playback Widget", "Silly little Python script that displays your currently playing song/podcast in a little window at the bottom right of your screen.\nThe window resizes automatically when the song/podcast data changes, and also updates the elapsed time automatically.",acceptedArguments)
lookFor = [t['name'] for t in acceptedArguments if t['name'] not in ['--help','<no arguments>']]
def mainCode():
    print(argv)
    curFile = ""
    useContext = False
    def viewArgs():
        # shows arguments
        t = Toplevel()
        t.title("Program Arguments")
        tFrame = Frame(t)
        tFrame.grid()
        Label(tFrame,text="Here's a list of arguments provided when running this script:",image='::tk::icons::information',compound='left').grid(columnspan=2)
        sb = Scrollbar(tFrame)
        lb=Listbox(tFrame,yscrollcommand=sb.set,width=max((len(s) for s in argv),default=0))
        lb.insert(END,*argv)
        lb.grid(row=1,column=0)
        sb.configure(command=lb.yview)
        sb.grid(row=1,column=1,sticky='nsw')
        Button(tFrame,text='OK',command=t.destroy).grid(columnspan=2)
    def simp(a:Event):
        stx=root.winfo_screenwidth()-26
        y=root.winfo_screenheight()-126
        dum,ass = root.winfo_width(),root.winfo_height()
        stx -= dum
        y -= ass
        if [a.x,a.y] != [stx,y]:
            try:
                root.wm_geometry(f"+{stx}+{y}")
            except:
                pass
        else:
            print("deez",datetime.now())
    def ball(a:Event):
        stx=tl.winfo_screenwidth()-26
        y=tl.winfo_screenheight()-126
        dum,ass = tl.winfo_width(),tl.winfo_height()
        stx -= dum
        y -= ass
        if [a.x,a.y] != [stx,y]:
            try:
                tl(f"+{stx}+{y}")
            except:
                pass
        else:
            print("deez",datetime.now())
    def show_error(oops:BaseException):
        if type(oops) is not KeyboardInterrupt:
            print_exc()
            items = []
            for thing in root.children:
                items.append(thing)
            for thing in items:
                root.children[thing].destroy()
            t = Toplevel()
            t.title("Error")
            t.lift()
            tFrame = Frame(t)
            tFrame.grid()
            Label(tFrame,text="An error has occurred and this application needs to quit.\nYou can view error details below:",image="::tk::icons::error",compound="left").grid(row=0,columnspan=2)
            sb_x = Scrollbar(tFrame,orient='horizontal')
            sb_y = Scrollbar(tFrame,orient='vertical')
            txt = Text(tFrame,width=50,height=25,wrap="none",cursor='arrow',xscrollcommand=sb_x.set,yscrollcommand=sb_y.set)
            txt.insert(END,format_exc())
            txt.configure(state='disabled')
            txt.grid(row=1,column=0,sticky='news')
            sb_x.configure(command=txt.xview)
            sb_y.configure(command=txt.yview)
            sb_x.grid(row=2,column=0,sticky='we')
            sb_y.grid(row=1,column=1,sticky='nsw')
            Button(tFrame,text="Quit",command=quit).grid(columnspan=2)
            t.after(100,lambda: MessageBeep(16))
        else:
            quit()
    def updateButLessLaggy():
        nonlocal curFile
        try:
            nut = Player(cli.current_playback())
            if nut:
                playerItem = nut.item
                sillyString = ""
                if playerItem:
                    if not useContext: root.title(playerItem.name)
                    if nut.currently_playing_type == "episode":
                        sillyString = f"{playerItem.name}\n{playerItem.show.name}"
                    elif nut.currently_playing_type == "track":
                        sillyString = f"{playerItem.name}\n{', '.join(artist.name for artist in playerItem.artists)}\n{playerItem.album.name}"
                    curFile = playerItem.id
                    hasMedia = len(playerItem.album.images) > 0 if type(playerItem) == Track else len(playerItem.show.images) >0
                    if hasMedia:
                        sillyUrl = playerItem.album.images[0].url if type(playerItem) == Track else playerItem.show.images[0].url
                        sillyName = "IMG_CACHE/{0}.JPG".format(playerItem.id)
                        try:
                            open(sillyName)
                        except FileNotFoundError:
                            urlretrieve(sillyUrl,sillyName,imgDL) # download if not cached
                        fard = Image.open(sillyName)
                        profImg.paste(fard.resize((64,64)))
                        root.wm_iconphoto(True,profImg)
                    else: 
                        profImg.paste(ImageTk.PhotoImage(Image.open("../gagababy.png").resize((64,64))))
                        root.wm_iconphoto(True,"::tk::icons::question")
                    root.update()
                else:
                    root.title("???")
                    sillyString = "Unable to get current track information.\nPlease try again later."
                if nut.progress_ms:
                    if playerItem:
                        sillyString += f"\n{tlength(nut.progress_ms)} / {tlength(playerItem.duration_ms)}"
                        pbar.configure(value=nut.progress_ms,maximum=playerItem.duration_ms)
                    else:
                        sillyString += f"\n{tlength(nut.progress_ms)} elapsed"
                        pbar.configure(value=nut.progress_ms,maximum=nut.progress_ms*2) # Double the length. This just sets the bar to 50% lmao
                else: pass
                labelText.set(sillyString)
                l.configure(image=profImg)
                l.image = profImg
                if playerItem:
                    if playerItem.name in sillyString: # check if the current item's name is in the silly string
                        root.after(1000,updateButLessLaggy)
                elif nut.currently_playing_type == 'episode' and not playerItem:
                    root.after(1000,updateButLessLaggy) # fallback cause it keeps freezing
                elif playerItem and curFile != playerItem.id: update()
        except BaseException as egg:
            show_error(egg)
    newLine = "\n"
    def update():
        try:
            nut = Player(cli.current_playback())
        except BaseException as egg:
            show_error(egg)
        try:
            nonlocal useContext
            useContext = nut.context and '--use-context' in argv
            if nut:
                playerItem = nut.item
                if useContext:
                    print(nut.context.__dict__)
                    ctx = contextObject(nut.context.type,nut.context.id or nut.context.uri)
                    root.title(ctx.name)
                if playerItem:
                    if not useContext: root.title(playerItem.name)
                    nonlocal profImg,curFile
                    sillyUrl = playerItem.album.images[0].url if type(playerItem) == Track else playerItem.show.images[0].url
                    sillyName = "IMG_CACHE/{0}.JPG".format(playerItem.id)
                    curFile = playerItem.id
                    if not '--force-redownload' in argv:
                        try:
                            open(sillyName)
                        except FileNotFoundError:
                            urlretrieve(sillyUrl,sillyName,imgDL) # download if not cached
                    else:
                        urlretrieve(sillyUrl,sillyName,imgDL) # download regardless if forcing
                    fard = Image.open(sillyName)
                    profImg.paste(fard.resize((64,64)))
                    root.update()
                    if type(playerItem) == Episode:
                        labelText.set(f'{playerItem.name}\n{playerItem.show.name}\n')
                        l.configure(wraplength=len(playerItem.show))
                    elif type(playerItem) == Track:
                        labelText.set(f'{playerItem.name}\n{",".join([artist.name for artist in playerItem.artists])}\n{playerItem.album.name}')
                else:
                    labelText.set("Could not retrieve item information.\nPlease try again later.")
                    root.title("???")
                if nut.progress_ms:
                    if playerItem: 
                        labelText.set(labelText.get()+f'\n{tlength(nut.progress_ms)} / {tlength(nut.item.duration_ms)}')
                        pbar.configure(value=nut.progress_ms,maximum=playerItem.duration_ms)
                    else: 
                        labelText.set(labelText.get()+f'\n{tlength(nut.progress_ms)} elapsed')
                        pbar.configure(value=nut.progress_ms,maximum=nut.progress_ms*2) # Double the length. This just sets the bar to 50% lmao
        except TclError:
            pass
        root.after(1000,updateButLessLaggy)
    
        try:
            root.wm_iconphoto(True,profImg)
        except UnboundLocalError:
            root.wm_iconphoto(True,"::tk::icons::question")
        #root.wm_attributes("-disabled",1)
        try:
            menubar.delete(0,1)
            root.forget(menubar)
        except TclError:
            pass
        

    def switch_theme():
        root.set_theme(theme.get())

    root = ThemedTk(toplevel=1,themebg=1,background=1)
    root.title("Spotify Playback Widget")
    themeList = root.themes
    root.resizable(0,0)
    rootFrame = Frame(root)
    rootFrame.grid()
    labelText = StringVar(value="You haven't signed in yet.\nClick 'Update' in the menu bar to get started!")
    tl = Toplevel(name="img_download")
    tl.title("Image Download")
    tFrame = Frame(tl,name='tframe')
    tFrame.grid()
    pbar2 = Progressbar(tFrame,name='balls',value=0)
    pbar2.grid(row=1)
    sus=Label(tFrame,name='sex',text=f"Downloading cover art for {labelText.get().split(newLine)[0]}",image="::tk::icons::information",compound='left')
    sus.grid(row=0)
    tl.update()
    tl.withdraw()
    pFrame = Frame(rootFrame)
    pFrame.grid()
    j=Image.open("..\\gagababy.png")
    profImg = ImageTk.PhotoImage(j.resize((64,64)),master=root)
    l = Label(pFrame,textvariable=labelText,image=profImg,compound='left')
    l.image = profImg
    l.grid()
    pbar = Progressbar(rootFrame,value=0,maximum=100)
    pbar.grid(row=1,sticky='ew')
    menubar = Menu(tearoff=0)
    root.configure(menu=menubar)
    qMenu = Menu(tearoff=0)
    qMenu.add_command(label="View arguments",command=viewArgs)
    qMenu.add_separator()
    qMenu.add_command(label="Quit",command=quit)
    menubar.add_cascade(label="🍎",menu=qMenu)
    menubar.add_command(label="Update",command=update)
    root.wm_attributes("-topmost",1)
    root.bind("<FocusIn>",lambda a: root.wm_attributes("-alpha",1))
    root.bind("<FocusOut>",lambda a: root.wm_attributes("-alpha",0.7))
    theme = StringVar()
    rcMenu = Menu(l,tearoff=0,selectcolor="green")
    for t in themeList:
        rcMenu.add_radiobutton(value=t,label=t,variable=theme,command=switch_theme)
    def doPopup(e:Event):
        rcMenu.tk_popup(e.x_root,e.y_root)
    root.bind("<Button-3>",doPopup)
    root.bind("<Configure>",simp)
    tl.bind("<Configure>",ball)
    def imgDL(c:int,b:int,t:int): # LMAO CBT
        print(c,b,t)
        try:
            tl.deiconify()
            tl.lift()
            sus.configure(text=f"Downloading cover art for {labelText.get().split(newLine)[0]}")
            pbar2.configure(value=c*b,maximum=t)
            root.update()
            if c*b >= t:
                tl.withdraw()
        except AttributeError as e:
            show_error(e)
    print("exiting lol")
    root.mainloop()
try:
    match argv[1]:
        case '--clean':
            root = ThemedTk(theme='scidblue',themebg=1)
            root.title("Cache cleanup")
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
                quit(69)
            lbl = Label(rootFrame,text="By cleaning the image cache, image downloads may take longer to complete.\nDo you wish to continue?",image="::tk::icons::question",compound="top")
            lbl.grid(columnspan=2)
            btYes = Button(rootFrame,text='Yes',underline=1,command=cleanup)
            btYes.grid(row=1,column=0)
            btNo = Button(rootFrame,text='No',underline=1,command=quit)
            btNo.grid(row=1,column=1)
            btYes.bind("y",cleanup)
            btNo.bind("n",quit)
            root.mainloop()
        case '--help':
            match argv[2]:
                case '-g':
                    helpDoc.showHelp()
                case '-o':
                    try:
                        if len(argv) < 4:
                            raise ValueError("No file path was provided.")
                        helpDoc.outFile(argv[3])
                    except (IndexError, ValueError) as wawa:
                        raise ValueError("Error: " + str(wawa))
                    except BaseException:
                        raise
                case '':
                    helpDoc.printHelp()
                case _:
                    raise NotImplementedError("Unrecognised argument(s): ",argv[2:])
        case '' | _:
            if argv[1]: print("unrecognised option!")
            mainCode()
except IndexError:
    mainCode()