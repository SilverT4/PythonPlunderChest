from typing import Any,Union
from spotify.baseObject import SpotifyObject
from spotify.externalStuff import ExternalURLs
from spotify.user import User
from spotify.track import Track
from spotify.podcast import Episode
from spotify.image import SpotifyImage
from spotify.SpotifyClient import cli as cl
from spotipy import SpotifyException
from json import load

def getDateTime(string):
    from datetime import datetime
    return datetime.fromisoformat(string)
class PlaylistItems(SpotifyObject):
    """idk"""
    def __init__(self, data: dict[str, Any]):
        self.next:str|None = data['next']
        self.limit:int = data['limit']
        self.previous:str|None = data['previous']
        self.total:int = data['total']
        self.items:list[PlaylistItem] = [PlaylistItem(s) for s in data['items']]
        super().__init__(data)
class PlaylistItem(SpotifyObject):
    """
    Custom subclass object to represent an item in a playlist.

    Subclass-specific variables:
    * str `added_at` - A date/time string representing when the item was added.
    * custom object `added_by` - Represents who added the item.
    * bool `is_local` - Whether the item is from a local file.
    * custom object `track` - The item itself.
    * datetime object `added_at_DT` - Custom variable by me.
    """
    def __init__(self, data: dict[str, Any]):
        self.added_at:str = data['added_at']
        self.added_at_DT = getDateTime(self.added_at.removesuffix("Z"))
        if data['added_by']['id'] != '': self.added_by:User = User(cl.user(data['added_by']['id']))
        else: self.added_by:User = User(cl.user("jx93c9uctz2ex5v5mvje1bpa7")) # uses me as a placeholder
        try: self.is_local:bool = data['is_local']
        except KeyError: self.is_local = False
        self.track:Track|Episode = Track(data['track']) if data['track']['track'] else Episode(data['track'])
        super().__init__(data)

class Playlist(SpotifyObject):
    """
    Custom subclass object to represent a Spotify playlist.

    Subclass-specific variables:
    * bool `collaborative` - Represents whether the playlist is collaborative, meaning users other than the owner can modify it.
    * str `description` - self-explanatory. will be None if no description exists.
    * custom object `external_urls` - external urls for the playlist
    * int `followers` - the total number of followers.
    * list `images` - images of the playlist cover. may have up to 3 images, or be empty.
    * str `name` - self-explanatory.
    * custom object `owner` - represents the playlist owner.
    * bool `public` - represents whether the playlist is public or private. set to True if public, False if private, or None if irrelevant.
    * str `snapshot_id` - version identifier for the playlist.
    * list `tracks` - self-explanatory. contains tracks and podcast episodes.
    """
    def __init__(self, data: dict[str, Any]):
        self.collaborative:bool = data['collaborative']
        self.description:str = data['description']
        self.external_urls:ExternalURLs = ExternalURLs(data['external_urls'])
        try:
            self.followers:int = data['followers']['total'] # see artist.py for why i do it like this
        except KeyError:
            self.followers = 0
        try:
            self.images:list[SpotifyImage] = [SpotifyImage(i) for i in data['images']]
        except KeyError:
            self.images = []
        self.name:str = data['name']
        self.owner:User = User(data['owner'])
        self.public:bool = data['public']
        self.snapshot_id:str = data['snapshot_id']
        self.tracks:PlaylistItems = PlaylistItems(data['tracks'])
        super().__init__(data)