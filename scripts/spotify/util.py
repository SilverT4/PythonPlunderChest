from spotify.legalese import CopyrightObject
from spotify.iterator import SpotifyIterable
from spotify.SpotifyClient import cli
from spotify.album import Album
from spotify.artist import Artist
from spotify.audiobook import Chapter,Audiobook
from spotify.playlist import Playlist
from spotify.user import User
from spotify.player import Player,Device
from spotify.track import Track
from spotify.image import SpotifyImage
from spotify.baseObject import SpotifyObject
from typing import Literal,Any,Callable
from urllib.request import urlretrieve
from os.path import exists
def expanded_id(type:Literal['album','artist','audiobook','chapter','episode','playlist','show','track','user'],id:str):
    if f"spotify:{type}:" in id:
        return id.removeprefix(f'spotify:{type}:')
    elif "https://open.spotify.com" in id:
        return id.removeprefix(f'https://open.spotify.com/{type}/').removesuffix(r'?id=.*')
    else:
        return id # if it's just a plain old ID it returns the ID itself
def audiobook(id:str,market:str='US') -> ...: # uses the US market as placeholder
    resp = cli._get("audiobooks/"+expanded_id("audiobook",id))
    return Audiobook(resp)

def audiobooks(ids:list[str],market:str='US'):
    resp = cli._get("audiobooks/?ids="+','.join(ids))
    return [Audiobook(a) for a in resp['audiobooks']]

def audiobook_chapters(id:str,market:str='US'):
    resp = cli._get(f"audiobooks/{id}/chapters")
    return SpotifyIterable(resp,'chapter',Chapter)

def devices():
    resp = cli.devices()
    return [Device(d) for d in resp['devices']]

from spotify.podcast import Show,Episode
def convert(data:dict[str,any],to:str) -> Album|Artist|Audiobook|Chapter|Episode|Playlist|Show|Track|User|Device|Player|SpotifyImage|CopyrightObject | CopyrightObject: # I probably won't use this, but I'm including it anyway.
    objs:dict[str,Album|Artist|Audiobook|Chapter|Episode|Playlist|Show|Track|User|Device|Player|SpotifyImage|CopyrightObject] = {"album": Album, "artist": Artist, "audiobook": Audiobook, "chapter": Chapter, "episode": Episode, "show": Show, "playlist": Playlist, "player": Player, "track": Track, "user": User, "image": SpotifyImage, "copyright": CopyrightObject}
    if to.lower() in objs:
        return objs[to.lower()](data)
    else: return SpotifyObject(data) # Fallback if the type is unrecognised.

def getimg(name:str) -> str|None:
    if exists("IMG_CACHE/{0}.JPG".format(name)):
        return "IMG_CACHE/{0}.JPG".format(name)
    return None
def download_image(from_:str,to:str,callback:Callable):
    urlretrieve(from_,to,callback)

def formatn(n,s):
    if n == 1:
        return '{n} {s}'.format(n,s)
    else:
        return '{n} {s}s'.format(n,s)
    
def formatl(u:dict[str,int]):
    "this formats the length string for podcasts atm"
    finalString = ""
    
def tlen(ms):
    # Convert milliseconds to seconds
    seconds = ms / 1000

    # Use divmod to get hours, minutes, and remaining seconds
    hours, remainder = [round(t) for t in divmod(seconds, 3600)]
    minutes, seconds = [round(t) for t in divmod(remainder, 60)]

    formatted_time = ""

    if hours > 0:
        formatted_time += f"{hours}:"
    
    if minutes < 10:
        formatted_time += f"0{minutes}:"
    else: formatted_time += f"{minutes}:"

    if seconds < 10:
        formatted_time += f"0{seconds}:"
    else: formatted_time += f"{seconds}:"

    return formatted_time

def runtime(ms):
    # Convert milliseconds to seconds
    seconds = ms / 1000

    # Use divmod to get hours, minutes, and remaining seconds
    hours, remainder = [round(t) for t in divmod(seconds, 3600)]
    minutes, seconds = [round(t) for t in divmod(remainder, 60)]

    formatted_time = []

    # Use the formatn function to format hours, minutes, and seconds
    if hours > 0:
        formatted_time.append(formatn(hours, "hour"))
    if minutes > 0:
        formatted_time.append(formatn(minutes, "minute"))
    if seconds > 0:
        formatted_time.append(formatn(seconds, "second"))

    return ', '.join(formatted_time)

import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *

class VerticalScrolledFrame(ttk.Frame):
    def __init__(self, parent, *args, **kw):
        ttk.Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = ttk.Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        self.canvas = tk.Canvas(self, bd=0, highlightthickness=0, 
                                width = 200, height = 300,
                                yscrollcommand=vscrollbar.set)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command = self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = ttk.Frame(self.canvas)
        self.interior.bind('<Configure>', self._configure_interior)
        self.canvas.bind('<Configure>', self._configure_canvas)
        self.master.bind('<MouseWheel>',self._mouse)
        self.interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=NW)

    def _mouse(self,event:tk.Event):
        self.canvas.yview_scroll(int(-1*(event.delta)/120),"units")
    def _configure_interior(self, event):
        # Update the scrollbars to match the size of the inner frame.
        size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
        self.canvas.config(scrollregion=(0, 0, size[0], size[1]))
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the canvas's width to fit the inner frame.
            self.canvas.config(width = self.interior.winfo_reqwidth())
        
    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # Update the inner frame's width to fill the canvas.
            self.canvas.itemconfigure(self.interior_id, width=self.canvas.winfo_width())