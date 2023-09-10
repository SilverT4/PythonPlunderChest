from random import randint
import spotipy,PIL # spotipy, pillow
import asyncio # asyncio
from globals.relativeTime import relative_time as rt # in this git.
from time import sleep
from spotipy import SpotifyOauthError
from dotenv import load_dotenv # python-dotenv
from os import getenv
from spotify.album import *
from spotify.artist import *
from spotify.playlist import *
from spotify.podcast import *
from spotify.track import *
from spotify.user import *
from spotify.me import MyTopItems
from spotify.length import milliseconds_to_hms as tlength
from spotify.player import Player
from spotify.contextTyper import contextObject
from spotify.SpotifyClient import *
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk # ttkthemes
from tkscrolledframe import ScrolledFrame # tkScrolledFrame
from requests import get # requests
from async_tkinter_loop import async_handler,async_mainloop
from functools import partial
from urllib.request import urlretrieve
from PIL import Image,ImageTk
load_dotenv()

root = ThemedTk(theme='scidgreen',toplevel=1,themebg=1,background=1,sync=1,fonts=1)
root.title("python spotify thing")
@async_handler
async def check_access_token():
    from json import load
    from datetime import datetime
    from winsound import MessageBeep
    cacheFile = load(open(".cache"))
    try:
        expiry = cacheFile['expires_at']
        if datetime.now().timestamp() >= expiry:
            t=Toplevel()
            t.title("Warning")
            tFrame = Frame(t)
            tFrame.grid()
            Label(tFrame,text="Your access token has expired. Click OK to reauthenticate Spotify.",image="::tk::icons::warning",compound=LEFT).grid()
            def reauth():
                try:
                    cli.current_user()
                    t.destroy()
                except spotipy.SpotifyException as egg:
                    show_NonfatalError(egg)
            Button(tFrame,text="OK",command=reauth).grid()
            t.after(100,lambda:MessageBeep(48))
    except KeyError:
        t = Toplevel()
        t.title("Warning")
        tFrame = Frame(t)
        tFrame.grid()
        def reauth():
            try:
                cli.set_auth(SpotifyOAuth(show_dialog=True,open_browser=True,scope=auth_scope))
                print(cli.current_playback())
            except SpotifyException as egg:
                print(egg)
                show_NonfatalError(egg)
        Label(tFrame,text="No access token found in cache, or \"expires_at\" key does not exist in cache JSON data. Please reauthenticate Spotify.",image="::tk::icons::error",compound=LEFT).grid()
        Button(tFrame,text="Reauthenticate",command=reauth).grid()
        t.after(100,lambda:MessageBeep(16))
@async_handler
async def show_NonfatalError(details:BaseException):
    from traceback import format_exc
    sex = Toplevel()
    sex.title("Error")
    sexFrame = Frame(sex)
    sexFrame.grid()
    Label(sexFrame,text="An error has occurred. This error does not prevent the further use of this application, and can be dismissed.\nDetails:",image="::tk::icons::error",compound="left").grid(row=0,columnspan=2)
    sbX = Scrollbar(sexFrame,orient='horizontal')
    sbY = Scrollbar(sexFrame)
    sbX.grid(row=2,column=0,sticky='we')
    sbY.grid(row=1,column=1,sticky='ns')
    det = Text(sexFrame,yscrollcommand=sbY.set,xscrollcommand=sbX.set,cursor='arrow')
    det.insert('end',format_exc())
    det.configure(state='disabled')
    det.grid(row=1,column=0)
    sbX.configure(command=det.xview)
    sbY.configure(command=det.yview)
    Button(sexFrame,text="OK",command=sex.destroy).grid(row=3,columnspan=2)
rootFrame = Frame()
rootFrame.grid()
menubar = Menu(tearoff=0)
root.configure(menu=menubar)
@async_handler
async def show_MyProfile():
    print("attempting to show user profile")
    try:
        me = User(cli.me())
    except spotipy.SpotifyOauthError as egg:
        show_NonfatalError(egg)

    pWindow = Toplevel()
    pWindow.title(me.display_name)
    pWindow.grid_rowconfigure(0,weight=1)
    pWindow.grid_columnconfigure(0,weight=1)
    pf = Frame(pWindow)
    pf.grid()
    pFrame = pf
    print(me.images)
    if len(me.images) > 0:
        # grabs the largest image
        img = me.images[0]
        from urllib.request import urlretrieve as deez
        dum = deez(img.url,"TMP_PFP.JPG")
        from PIL import ImageTk
        mud = ImageTk.PhotoImage(file="TMP_PFP.JPG")
        profLabel = Label(pFrame,image=mud,text=f"{me.display_name}\n{me.product}",compound='left')
        profLabel.image = mud
        profLabel.grid(row=0,columnspan=2)
    else:
        print("no pfp")
        Label(pFrame,text=f"{me.display_name}\n{me.product}").grid(row=0,columnspan=2)
    
    Label(pFrame,text=f"Followers: {me.followers}").grid(row=1,column=0)
@async_handler
async def show_Playlist(plist:Playlist):
    print("showing playlist")
    pWindow = Toplevel()
    pWindow.title(plist.name)
    pWindow.grid_rowconfigure(0,weight=1)
    pWindow.grid_columnconfigure(0,weight=1)
    pf = Frame(pWindow)
    pf.grid()
    aFrame = Frame(pf)
    aFrame.grid()
    sb_x = Scrollbar(pf,orient='horizontal')
    sb_x.grid(row=2,column=0,sticky='we')
    sb_y = Scrollbar(pf)
    sb_y.grid(row=1,column=1,sticky='ns')
    pFrame = Treeview(pf,cursor='arrow',columns=('Title','Album or Podcast','Date added','Release date','🕒'),height=10,selectmode='none',yscrollcommand=sb_y.set,xscrollcommand=sb_x.set)
    pFrame.grid(row=1,column=0)
    sb_x.configure(command=pFrame.xview)
    sb_y.configure(command=pFrame.yview)
    tlengths = [item.track.duration_ms for item in plist.tracks.items]
    plistLength = tlength(sum(tlengths))
    try:
        if len(plist.images) == 1:
            img = plist.images[0]
        elif len(plist.images) > 1:
            img = plist.images[1] # usually the second-smallest image, or the smallest
        from urllib.request import urlretrieve as deez
        dum = deez(img.url,"TMP_PFP.JPG")
        from PIL import ImageTk,Image
        mum = Image.open("TMP_PFP.JPG")
        mud = ImageTk.PhotoImage(mum.resize((128,128)) if mum.size != (128,128) else mum)
        pLabel = Label(aFrame,image=mud,text=f"{plist.name}\nMade by {plist.owner.display_name}\nTotal length: {plistLength}",compound="top")
        pLabel.image = mud
        pLabel.grid()
    except IndexError:
        Label(aFrame,image="::tk::icons::question",text=f"{plist.name}\nMade by {plist.owner.display_name}\nTotal length: {plistLength}",compound="top").grid(row=0,column=0)
    Label(aFrame,text="Track list:").grid()
    headers = ["Title","Album or podcast","Date added","Added by","🕒"]
    for i in range(5):
        pFrame.heading(i,text=headers[i])
    crow = 3
    from humanize import naturaldate
    from PIL import Image,ImageTk
    from urllib.request import urlretrieve as piss
    for i in range(len(plist.tracks.items)):
        leItem = plist.tracks.items[i]
        leTrack = leItem.track
        length = tlength(leTrack.duration_ms)
        album_show = ""
        if type(leTrack) is Episode:
            album_show = leTrack.show.name
        else:
            album_show = leTrack.album.name
        added_natural = rt(leItem.added_at_DT)
        release = leItem.added_by.display_name
        piss(leItem.added_by.images[0].url,"TMP_ADDBY.JPG")
        image = Image.open("TMP_ADDBY.JPG")
        img = ImageTk.PhotoImage(image.resize((32,32)))
        pFrame.insert('','end',text=i,values=(leTrack.name,album_show,added_natural,release,length),image=img)
        crow+=1

@async_handler
async def show_MyPlaylists():
    print('attempting to show user playlists')
    try:
        myLists = cli.current_user_playlists()
        myself = User(cli.current_user())
    except spotipy.SpotifyOauthError as egg:
        show_NonfatalError(egg)
    print(myLists)
    fff = [cli.playlist(f['id']) for f in myLists['items']]
    lazyLists = [Playlist(s) for s in fff]

    pWindow = Toplevel()
    pWindow.title(f"{myself.display_name}'s Playlists")
    pWindow.grid_columnconfigure(0,weight=1)
    pWindow.grid_rowconfigure(0,weight=1)
    pf = Frame(pWindow)
    pf.grid()
    pFrame = pf
    Label(pFrame,text="Your playlists").grid()
    crow = 1
    for i in range(len(lazyLists)):
        root.update()
        playlist = lazyLists[i]
        crow+=1
        try:
            if len(playlist.images) == 1:
                img = playlist.images[0]
            elif len(playlist.images) > 1:
                img = playlist.images[1] # usually the second-smallest image, or the smallest
            from urllib.request import urlretrieve as deez
            dum = deez(img.url,"TMP_PFP.JPG")
            from PIL import ImageTk,Image
            mum = Image.open("TMP_PFP.JPG")
            mud = ImageTk.PhotoImage(mum.resize((64,64)) if mum.size != (64,64) else mum)
            ptype = "Public playlist" if playlist.public and not playlist.collaborative else "Public collaborative playlist" if playlist.public and playlist.collaborative else "Private playlist"
            labelText = f"{playlist.name}\n{ptype}\nCreated by {playlist.owner.display_name}\nTrack count: {playlist.tracks.total}"
            pLabel = Button(pFrame,image=mud,text=labelText,compound="left",command=partial(show_Playlist,playlist))
            pLabel.image = mud
            pLabel.grid(row=crow,column=0,sticky='we')
            crow+=1
        except IndexError:
            labelText = f"{playlist.name}\n{ptype}\nCreated by {playlist.owner.display_name}\nTrack count: {playlist.tracks.total}"
            Label(pFrame,image="::tk::icons::question",text=labelText,compound="top").grid(row=0,column=0)
            crow+=1
@async_handler
async def show_TrackDetails(id:str):
    print("getting details for track")
    leTrack = Track(cli.track(id))
    pWindow = Toplevel()
    pWindow.title(leTrack.name)
    pFrame = Frame(pWindow)
    pFrame.grid()
    labelText = StringVar()
    menubar = Menu(tearoff=0)
    pWindow.configure(menu=menubar)
    extraView = Menu(tearoff=0)
    extraView.add_command(label="View album")
    extraView.add_separator()
    lstring = ','.join([artist.name for artist in leTrack.artists]) if len(leTrack.artists) > 1 else leTrack.artists[0].name
    labelText.set(leTrack.name + "\nBy " + lstring + "\nLength: " + tlength(leTrack.duration_ms))
    refreshing = False
    if len(leTrack.album.images) > 0:
        url = leTrack.album.images[0].url
        urlretrieve(url,"TMP_TRK.PNG")
        mf = Image.open("TMP_TRK.PNG")
        img = ImageTk.PhotoImage(mf.resize((300,300)))
        l = Label(pFrame,image=img,text=leTrack.name + "\nBy " + lstring + "\nLength: " + tlength(leTrack.duration_ms),compound='top')
        l.image = img
        l.grid()
    else:
        Label(pFrame,image='::tk::icons::question',text=leTrack.name + "\nBy " + lstring + "\nLength: " + tlength(leTrack.duration_ms),compound='top').grid()
    for artist in leTrack.artists:
        extraView.add_command(label="View artist: " + artist.name)
    
refreshing = False
def show_CurrentlyPlaying():
    global refreshing
    try:
        myInfo:Player = Player(cli.current_playback('us','episode'))
    except SpotifyException as egg:
        show_NonfatalError(egg)
    if myInfo:
        context = myInfo.context
        from datetime import datetime
        repeat_mode = StringVar(value=myInfo.repeat_state)
        shuffleState = Variable(value=myInfo.shuffle_state)
        pWindow = Toplevel()
        ts = str(myInfo.timestamp)
        ts = ts[:-3]
        p=datetime.fromtimestamp(float(ts))
        print(p)
        pWindow.title(f"Now Playing - Last updated: {rt(p)}")
        pPane = Panedwindow(pWindow,orient='horizontal')
        pFrame = Frame(pPane)
        cFrame = Frame(pPane)
        playerItem = myInfo.item
        labelText = StringVar()
        labelText2 = StringVar(value="No context information\nSpotify did not provide context\n\n:thinking:")
        pbar = Progressbar(cFrame,value=0,maximum=100)
        pbar.grid(row=1,sticky='we')
        if playerItem:
            if playerItem.type == 'episode':
                labelText.set(f'{playerItem.name}\n{playerItem.show.name}\n')
            elif playerItem.type == 'track':
                labelText.set(f'{playerItem.name}\n{",".join([artist.name for artist in playerItem.artists])}\n{playerItem.album.name}')
        else:
            labelText.set("Could not retrieve item information.\nPlease try again later.")
        if myInfo.progress_ms:
            if playerItem: 
                labelText.set(labelText.get()+f'\n{tlength(myInfo.progress_ms)} / {tlength(myInfo.item.duration_ms)}')
                pbar.configure(value=myInfo.progress_ms,maximum=myInfo.item.duration_ms)
            else: 
                labelText.set(labelText.get()+f'\n{tlength(myInfo.progress_ms)} elapsed')
                pbar.configure(value=myInfo.progress_ms,maximum=myInfo.progress_ms*2) # Double the length. This just sets the bar to 50% lmao
        from PIL import Image,ImageTk
        from urllib.request import urlretrieve
        try:
            sillyUrl = playerItem.album.images[0].url if playerItem.type == 'track' else playerItem.show.images[0].url
            urlretrieve(sillyUrl,"TMP_PLAY.JPG")
            fard = Image.open("TMP_PLAY.JPG")
            img = ImageTk.PhotoImage(fard.resize((64,64)))
            l = Label(cFrame,textvariable=labelText,image=img,compound="left")
            l.image = img
            l.grid(row=0)
        except IndexError:
            l = Label(cFrame,textvariable=labelText,image="::tk::icons::question",compound="left")
            l.grid(row=0)
        ctxMenu = Menu(l,tearoff=0)
        if type(playerItem) == Track:
            ctxMenu.add_command(label=f"View album: {playerItem.album.name}")
            for artist in playerItem.artists:
                ctxMenu.add_command(label=f"View artist: {artist.name}")
            ctxMenu.add_command(label="View track details",command=lambda: show_TrackDetails(playerItem.id))
        elif type(playerItem) == Episode:
            ctxMenu.add_command(label=f"View show: {playerItem.show.name}")
            ctxMenu.add_command(label="View episode description")
        l.bind("<Button-3>",lambda event: ctxMenu.tk_popup(event.x_root,event.y_root))
        l1 = Label(pFrame,textvariable=labelText2,image="::tk::icons::question",compound='right',justify='right')
        l1.grid(row=0,column=1)
        pPane.add(cFrame,weight=1)
        pPane.add(pFrame,weight=1)
        pPane.grid()
        if context:
            print("oh hey we got context nice")
            ctxThing = contextObject(context.type,context.uri) # uses the URI as i'm too lazy to figure out ID another way.
            imageVar = ctxThing.images
            if len(imageVar) > 0:
                sillyUrl = imageVar[0].url
                urlretrieve(sillyUrl,"TMP_CTX.JPG")
                fart = Image.open("TMP_CTX.JPG")
                img = ImageTk.PhotoImage(fart.resize((64,64)))
                ctx_str = f"{ctxThing.name}\n"
                if type(ctxThing) == Album:
                    ctx_str += f"{','.join([artist.name for artist in ctxThing.artists])}\n{ctxThing.genres}\n{ctxThing.release_date}"
                elif type(ctxThing) == Artist:
                    ctx_str += f"{ctxThing.followers} followers\n{ctxThing.genres}\n"
                elif type(ctxThing) == Playlist:
                    ptype = "Public playlist" if ctxThing.public and not ctxThing.collaborative else "Public collaborative playlist" if ctxThing.public and ctxThing.collaborative else "Private playlist"
                    ctx_str += f"Made by {ctxThing.owner.display_name}\n{ptype}\n{ctxThing.tracks.total} items"
                elif type(ctxThing) == Show:
                    ctx_str += f"Published by {ctxThing.publisher}\n{ctxThing.total_episodes} episodes\n{ctxThing.media_type}"
                labelText2.set(ctx_str)
                l1.configure(image=img)
                l1.image = img
            else:
                ctx_str = f"{ctxThing.name}\n"
                if type(ctxThing) == Album:
                    ctx_str += f"{','.join([artist.name for artist in ctxThing.artists])}\n{ctxThing.genres}\n{ctxThing.release_date}"
                elif type(ctxThing) == Artist:
                    ctx_str += f"{ctxThing.followers} followers\n{ctxThing.genres}\n"
                elif type(ctxThing) == Playlist:
                    ptype = "Public playlist" if ctxThing.public and not ctxThing.collaborative else "Public collaborative playlist" if ctxThing.public and ctxThing.collaborative else "Private playlist"
                    ctx_str += f"Made by {ctxThing.owner.display_name}\n{ptype}\n{ctxThing.tracks.total} items"
                elif type(ctxThing) == Show:
                    ctx_str += f"Published by {ctxThing.publisher}\n{ctxThing.total_episodes} episodes\n{ctxThing.media_type}"
                labelText2.set(ctx_str)
                l1.configure(image="::tk::icons::question")
        from winsound import MessageBeep
        @async_handler
        async def refresh():
            global refreshing
            refreshing = True
            myInfo = Player(cli.current_playback('us','episode'))
            context = myInfo.context
            playerItem = myInfo.item
            ts = str(myInfo.timestamp)
            ts = ts[:-3]
            p=datetime.fromtimestamp(float(ts))
            pWindow.title(f"Now Playing - Last updated: {rt(p)}")
            playback_menu.entryconfigure(1,{"label": "Pause" if myInfo.is_playing else "Resume","command":pause if myInfo.is_playing else resume})
            playback_menu.entryconfigure(4,{"label": context.type.title() if context else "Repeat current context"})
            ctxMenu.delete(0,END) # remove everything there
            if type(playerItem) == Track:
                ctxMenu.add_command(label=f"View artist: {playerItem.album.name}")
                for artist in playerItem.artists:
                    ctxMenu.add_command(label=f"View artist: {artist.name}")
                ctxMenu.add_command(label="View track details",command=lambda: show_TrackDetails(playerItem.id))
            elif type(playerItem) == Episode:
                ctxMenu.add_command(label=f"View show: {playerItem.show.name}")
                ctxMenu.add_command(label="View episode description")
            if playerItem:
                if playerItem.type == 'episode':
                    labelText.set(f'{playerItem.name}\n{playerItem.show.name}\n')
                elif playerItem.type == 'track':
                    labelText.set(f'{playerItem.name}\n{",".join([artist.name for artist in playerItem.artists])}\n{playerItem.album.name}')
            else:
                labelText.set("Could not retrieve item information.\nPlease try again later.")
            if myInfo.progress_ms:
                if playerItem: 
                    labelText.set(labelText.get()+f'\n{tlength(myInfo.progress_ms)} / {tlength(myInfo.item.duration_ms)}')
                    pbar.configure(value=myInfo.progress_ms,maximum=myInfo.item.duration_ms)
                else: 
                    labelText.set(labelText.get()+f'\n{tlength(myInfo.progress_ms)} elapsed')
                    pbar.configure(value=myInfo.progress_ms,maximum=myInfo.progress_ms*2) # Double the length. This just sets the bar to 50% lmao
            try:
                sillyUrl = playerItem.album.images[0].url if playerItem.type == 'track' else playerItem.show.images[0].url
                urlretrieve(sillyUrl,"TMP_PLAY.JPG")
                fard = Image.open("TMP_PLAY.JPG")
                img = ImageTk.PhotoImage(fard.resize((64,64)))
                l.configure(image=img)
                l.image = img
            except IndexError:
                l.configure(image='::tk::icons::question')
            if context:
                print("oh hey we got context nice")
                ctxThing = contextObject(context.type,context.uri) # uses the URI as i'm too lazy to figure out ID another way.
                imageVar = ctxThing.images
                if len(imageVar) > 0:
                    sillyUrl = imageVar[0].url
                    urlretrieve(sillyUrl,"TMP_CTX.JPG")
                    fart = Image.open("TMP_CTX.JPG")
                    img = ImageTk.PhotoImage(fart.resize((64,64)))
                    ctx_str = f"{ctxThing.name}\n"
                    if type(ctxThing) == Album:
                        ctx_str += f"{','.join([artist.name for artist in ctxThing.artists])}\n{ctxThing.genres}\n{ctxThing.release_date}"
                    elif type(ctxThing) == Artist:
                        ctx_str += f"{ctxThing.followers} followers\n{ctxThing.genres}\n"
                    elif type(ctxThing) == Playlist:
                        ptype = "Public playlist" if ctxThing.public and not ctxThing.collaborative else "Public collaborative playlist" if ctxThing.public and ctxThing.collaborative else "Private playlist"
                        ctx_str += f"Made by {ctxThing.owner.display_name}\n{ptype}\n{ctxThing.tracks.total} items"
                    elif type(ctxThing) == Show:
                        ctx_str += f"Published by {ctxThing.publisher}\n{ctxThing.total_episodes} episodes\n{ctxThing.media_type}"
                    labelText2.set(ctx_str)
                    l1.configure(image=img)
                    l1.image = img
                else:
                    ctx_str = f"{ctxThing.name}\n"
                    if type(ctxThing) == Album:
                        ctx_str += f"{','.join([artist.name for artist in ctxThing.artists])}\n{ctxThing.genres}\n{ctxThing.release_date}"
                    elif type(ctxThing) == Artist:
                        ctx_str += f"{ctxThing.followers} followers\n{ctxThing.genres}\n"
                    elif type(ctxThing) == Playlist:
                        ptype = "Public playlist" if ctxThing.public and not ctxThing.collaborative else "Public collaborative playlist" if ctxThing.public and ctxThing.collaborative else "Private playlist"
                        ctx_str += f"Made by {ctxThing.owner.display_name}\n{ptype}\n{ctxThing.tracks.total} items"
                    elif type(ctxThing) == Show:
                        ctx_str += f"Published by {ctxThing.publisher}\n{ctxThing.total_episodes} episodes\n{ctxThing.media_type}"
                    labelText2.set(ctx_str)
                    l1.configure(image="::tk::icons::question")
            else:
                l1.configure(image="::tk::icons::question")
                labelText2.set("No context information\nSpotify did not provide context\n\n:thinking:")
            refreshing = False
        async def skip_forward():
            if canModifyPlaybackState and myInfo.actions.skipping_next:
                print('skipping to next item!')
                cli.next_track()
                pWindow.after(500,refresh)
            else:
                show_NonfatalError(BaseException("You do not have permission to perform this action" if not canModifyPlaybackState else "Skipping to the next item is not allowed at this time."))
        
        @async_handler
        async def skip_back():
            if "user-modify-playback-state" in auth_scope and myInfo.actions.skipping_prev:
                print('skipping to last item!')
                cli.previous_track()
                pWindow.after(500,refresh)
            else:
                show_NonfatalError(BaseException("You do not have permission to perform this action" if not canModifyPlaybackState else "Skipping to the previous item is not allowed at this time."))
        @async_handler
        async def pause():
            if canModifyPlaybackState and myInfo.actions.pausing:
                print('pausing track')
                try: cli.pause_playback()
                except SpotifyException as egg:
                    show_NonfatalError(egg)
                pWindow.after(500,refresh)
            else:
                show_NonfatalError(BaseException("You do not have permission to perform this action" if not canModifyPlaybackState else "Pausing is not supported at this time."))
        @async_handler
        async def resume():
            if canModifyPlaybackState and myInfo.actions.resuming:
                print('resuming track')
                try:
                    cli.start_playback()
                except SpotifyException as egg:
                    show_NonfatalError(egg)
                pWindow.after(500,refresh)
            else:
                show_NonfatalError(BaseException("You do not have permission to perform this action" if not canModifyPlaybackState else "Resuming playback is not supported at this time."))
        @async_handler
        async def show_VolumeSlider():
            from tkinter import Scale as TkScale # Using this for better control.
            v = IntVar(value=myInfo.device.volume_percent)
            vWindow = Toplevel(pWindow)
            vWindow.wm_attributes("-toolwindow",1)
            vFrame = Frame(vWindow)
            vFrame.grid()
            Label(vFrame,text="Drag the slider below to change the volume.",image="::tk::icons::information",compound='left').grid(row=0,columnspan=2)
            TkScale(vFrame,variable=v,from_=100,to=0,tickinterval=25,label="Volume").grid(row=1,columnspan=2)
            def set_Volume():
                if canModifyPlaybackState:
                    print(f"setting volume to {v.get()}%")
                    cli.volume(v.get())
                    vWindow.after(475,refresh)
                    vWindow.after(500,vWindow.destroy)
                else:
                    show_NonfatalError(BaseException("You do not have permission to modify the playback state."))
            Button(vFrame,text="OK",command=set_Volume).grid(row=2,column=0)
            Button(vFrame,text="Cancel",command=vWindow.destroy).grid(row=2,column=1)
        @async_handler
        async def switch_RepeatState():
            if canModifyPlaybackState:
                try:
                    cli.repeat(repeat_mode.get())
                except BaseException as egg:
                    show_NonfatalError(egg)
            else:
                show_NonfatalError(BaseException("You do not have permission to modify the playback state"))
        @async_handler
        async def toggle_Shuffle():
            if canModifyPlaybackState:
                try:
                    cli.shuffle(shuffleState.get())
                except BaseException as egg:
                    show_NonfatalError(egg)
            else:
                show_NonfatalError(BaseException("You do not have permission to modify the playback state"))
        countUp = BooleanVar(value=True)
        def playbackTime():
            myInfo = Player(cli.current_playback())
            dum = myInfo.progress_ms
            if playerItem:
                if playerItem.type == 'episode':
                    newString = f'{playerItem.name}\n{playerItem.show.name}\n\n{tlength(dum)} / {tlength(playerItem.duration_ms)}'
                elif playerItem.type == 'track':
                    newString = f'{playerItem.name}\n{",".join([artist.name for artist in playerItem.artists])}\n{playerItem.album.name}\n{tlength(dum)} / {tlength(playerItem.duration_ms)}'
                labelText.set(newString)
                pbar.configure(value=dum,maximum=myInfo.item.duration_ms)
            else: 
                newString = f"Could not retrieve item information.\nPlease try again later\n\n{tlength(dum)} elapsed"
                labelText.set(newString)
                pbar.configure(value=dum,maximum=dum*3) # Triple the length. This just sets the bar to 33% lmao
            if countUp.get() is True: pWindow.after(1000,partial(playbackTime))
        def updateCounter():
            countUp.set(not countUp.get())
            if countUp.get() is True:
                playbackTime(myInfo.progress_ms or 0)
        menubar = Menu(tearoff=0)
        pWindow.configure(menu=menubar)
        menubar.add_command(label="Refresh",command=refresh)
        playback_menu = Menu(tearoff=0)
        playback_menu.add_command(label="Skip previous",command=skip_back)
        playback_menu.add_command(label="Pause" if myInfo.is_playing else "Resume",command=pause if myInfo.is_playing else resume)
        playback_menu.add_command(label="Skip next",command=skip_forward)
        playback_menu.add_separator()
        try:playback_menu.add_radiobutton(label=myInfo.context.type.title(),command=switch_RepeatState,value="context",variable=repeat_mode)
        except AttributeError: playback_menu.add_radiobutton(label="Repeat current context",command=switch_RepeatState,value="context",variable=repeat_mode)
        playback_menu.add_radiobutton(label="Item",command=switch_RepeatState,value='track')
        playback_menu.add_radiobutton(label="Disable Repeat",command=switch_RepeatState,value="off")
        playback_menu.add_checkbutton(label="Shuffle",offvalue=False,onvalue=True,variable=shuffleState,command=toggle_Shuffle)
        playback_menu.add_separator()
        playback_menu.add_command(label="Set volume...",command=show_VolumeSlider)
        menubar.add_cascade(label="Controls",menu=playback_menu)
        optmenu = Menu(tearoff=0)
        menubar.add_cascade(label="Options",menu=optmenu)
        optmenu.add_checkbutton(label="Update time elapsed",command=updateCounter,variable=countUp,onvalue=True)
        global PREP_FINISHED
        PREP_FINISHED = True
        playbackTime()
menubar.add_command(label="View profile",command=show_MyProfile)
Label(rootFrame,text="What do you want to do?").grid(columnspan=2)
Button(rootFrame,text="Show my playlists",command=show_MyPlaylists).grid(row=1,column=0)
Button(rootFrame,text="View my currently playing",command=show_CurrentlyPlaying).grid(row=1,column=1)
root.after(100,check_access_token)
async_mainloop(root)