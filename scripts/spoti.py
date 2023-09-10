# clever name i know
from functools import partial
from spotify.SpotifyClient import cli
from tkinter import *
from tkinter.ttk import *
from ttkthemes import ThemedTk
from spotify.util import *
from PIL import Image,ImageTk
class Spotipie(ThemedTk):
    def __init__(self, screenName: str | None = None, baseName: str | None = "deez", className: str = 'h', useTk: bool = False, sync: bool = False, use: str | None = None, *, theme: str | None = None, toplevel: bool | None = None, themebg: bool | None = None, background: bool | None = None, gif_override: bool = 1) -> None:
        super().__init__(screenName, baseName, className, useTk, sync, use, theme=theme, toplevel=toplevel, themebg=themebg, background=background, gif_override=gif_override)
        self.mainframe = Frame(self)
        self.mainframe.grid()
        self.menubar = Menu(tearoff=0)
        self['menu'] = self.menubar
        self.myMenu = Menu(tearoff=0)
        self.myMenu.add_command(label="View profile",command=self.show_myProfile)
        self.fileMenu = Menu(tearoff=0)
        self.menubar.add_cascade(label="File",menu=self.fileMenu)
        self.menubar.add_cascade(label=self.getMyName(),menu=self.myMenu)
        self.topStuffMenu = Menu(tearoff=0)
        self.themeMenu = Menu(tearoff=0)
        for theme in self.themes:
            self.themeMenu.add_command(label=theme.title(),command=partial(self.set_theme,theme,1,1))
        self.fileMenu.add_cascade(label="Change theme...",menu=self.themeMenu)
        self.myMenu.add_cascade(label="View my...",menu=self.topStuffMenu)
        self.topStuffMenu.add_command(label="Top artists",command=self.show_topArtists)
        self.topStuffMenu.add_command(label="Top tracks",command=self.show_MyTopTracks)
        self.dlWindow = Toplevel(self)
        self.dlFrame = Frame(self.dlWindow)
        self.dlFrame.grid()
        self.dlLabel = Label(self.dlFrame,text="Now downloading image from Spotify, please wait...")
        self.dlLabel.grid()
        self.dlpbar = Progressbar(self.dlWindow)
        self.dlpbar.grid()
        self.dlWindow.title("Download Progress")
        self.dlWindow.withdraw()
        self.toplevels:list[Toplevel] = []
    def show_myProfile(self):
        me = convert(cli.me(),'user')
        t = Toplevel()
        self.toplevels.append(t)
        t.title("Profile for " + me.display_name)
        tFrame = Frame(t)
        tFrame.grid()
        if me.images[0] != None and not getimg(me.id):
            download_image(me.image.url,"IMG_CACHE/{0}.JPG".format(me.id),self.DownloadProgress)
        if getimg(me.id):
            fart = Image.open(getimg(me.id))
            img = ImageTk.PhotoImage(fart)
        else:
            img = '::tk::icons::question'
        pLabel = Label(tFrame,image=img,text=me.widgetText+"\n{0}".format(me.product),compound='left')
        pLabel.image = img
        pLabel.grid(row=0,column=0)

    def show_topArtists(self):
        print("pre-caching images ahead of time!")
        deez = SpotifyIterable(cli.current_user_top_artists(50,0,time_range='long_term'),'artist',Artist)
        imgs = []
        dlCount = 0
        for artist in deez.items:
            if artist.images[0] != None:
                if not getimg(artist.id):
                    urlretrieve(artist.images[0].url,"IMG_CACHE/{0}.JPG".format(artist.id),self.DownloadProgress)
                    dlCount += 1
                d = Image.open(getimg(artist.id))
                j = ImageTk.PhotoImage(d.resize((64,64)))
                imgs.append(j)
            else: imgs.append("::tk::icons::question")
        print("downloaded {} images".format(str(dlCount)))
        tl = Toplevel()
        tl.title(self.getMyName()+"'s Top Artists")
        self.toplevels.append(tl)
        tFrame = VerticalScrolledFrame(tl)
        tFrame.grid()
        colors = ['#d4af37','#bbc2cc','#cd7f32']
        fgcolors = ['white','black','white']
        for i in range(len(deez.items)):
            aa = Label(tFrame.interior,text=i+1)
            if i < 3:
                aa.configure(background=colors[i],foreground=fgcolors[i])
            aa.grid(row=i,column=0)
            leg = Label(tFrame.interior,text=deez.items[i].name,image=imgs[i],compound='left')
            if imgs[i] != "::tk::icons::question": leg.image = imgs[i]
            leg.grid(row=i,column=1,sticky='w')
    def show_MyTopTracks(self):
        print("precaching images if necessary...")
        imgs=[]
        deez = SpotifyIterable(cli.current_user_top_tracks(100,0,time_range='long_term'),'track',Track)
        dlCount = 0
        for track in deez.items:
            alb = track.album
            if alb.images[0] != None:
                if not getimg(alb.id):
                    urlretrieve(alb.images[0].url,"IMG_CACHE/{0}.JPG".format(alb.id),self.DownloadProgress)
                    dlCount += 1
                d = Image.open(getimg(alb.id))
                j = ImageTk.PhotoImage(d.resize((48,48)))
                imgs.append(j)
            else: imgs.append("::tk::icons::question")
        print("downloaded {} images".format(str(dlCount)))
        tl = Toplevel()
        tl.title(self.getMyName()+"'s Top Tracks")
        self.toplevels.append(tl)
        tFrame = VerticalScrolledFrame(tl)
        tFrame.grid()
        colors = ['#d4af37','#bbc2cc','#cd7f32']
        fgcolors = ['white','black','white']
        for i in range(len(deez.items)):
            aa = Label(tFrame.interior,text=i+1)
            if i < 3:
                aa.configure(background=colors[i],foreground=fgcolors[i])
            aa.grid(row=i,column=0)
            leg = Label(tFrame.interior,text=deez.items[i].widgetText,image=imgs[i],compound='left')
            if imgs[i] != "::tk::icons::question": leg.image = imgs[i]
            leg.grid(row=i,column=1,sticky='w')
    def show_artist(self):
        "i need to think of a layout lmao"
        ...
    def getMyName(self):
        try:
            me = User(cli.me())
            return me.display_name or "My stuff"
        except:
            return "My stuff"
    def show_customizer(self):
        ...
    
    def DownloadProgress(self,c:int,b:int,t:int): # 🥁🥁 🐔 AND ⚽⚽ TORTURE. FROM WIKIPEDIA, THE FREE ENCYCLOPEDIA AT E N DOT WIKIPEDIA DOT ORG
        p = c*b
        if p < t:
            self.dlWindow.deiconify()
            self.dlWindow.title('{0} of {1} bytes downloaded'.format(p,t))
            self.dlpbar.configure(value=p,maximum=t)
            self.after(150,self.dlWindow.withdraw)
        else:
            self.dlWindow.withdraw()


spot = Spotipie(theme="winxpblue",toplevel=1,useTk=1,sync=1,themebg=1,background=1)
spot.mainloop()