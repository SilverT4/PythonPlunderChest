from typing import Any
from spotify.baseObject import SpotifyObject
from spotify.artist import Artist
from spotify.track import Track
from spotify.image import SpotifyImage
from spotify.legalese import CopyrightObject
from spotify.iterator import SpotifyIterable
class TracksObject(SpotifyIterable):
    """
    Custom object class to represent the "tracks" variable in an Album object.

    Variables:
    * `limit` - int, The max. number of items in the response (set by the query or by default)
    * `next` - str/None, URL to the next page of items. Will be None if nothing is provided by the API.
    * `offset` - int, The offset of the items.
    * `previous` - str/None, pretty much the same as `next`.
    * `total` - int, the total number of items available to return.
    * `items` - list, the tracks in the album.
    """
    def __init__(self, data:dict[str,Any]):
        self.limit:int = data['limit']
        self.next:str|None = data['next']
        self.offset:int = data['offset']
        self.previous:str|None = data['previous']
        self.total:int = data['total']
        #self.items:list[SimplifiedTrack] = [SimplifiedTrack(js) for js in data['items']]
        super().__init__(self,data,'track',Track)
class Album(SpotifyObject):
    """
    Custom subclass object to represent an Album returned by the Spotify API

    Subclass-specific variables:
    - str `name` - The name of the album
    - str `release_date` - The release date of the album
    - str `release_date_precision` - The precision of the release date. Usually "day", "month", or "year".
    - int `total_tracks` - The total number of tracks in the album
    - list `artists` - List of Artist objects representing the album's artists
    - list `genres` - List of genres associated with the album
    - str `label` - The record label of the album
    - int `popularity` - The popularity score of the album
    - list `tracks` - List of Track objects representing the album's tracks
    - str `album_type` - The type of album (e.g., 'album', 'single')
    - list `copyrights` - If included by the API, this lists the copyrights of the album.
    """
    def __init__(self, data: dict[str, Any]):
        """
        Initialise the Album class object.

        This sets the `album_type`, `artists`, `genres`, `images`, `popularity`, `total_tracks`, and `tracks` variables.
        """
        self.album_type:str = data['album_type']
        self.artists:list[Artist] = [Artist(js) for js in data['artists']]
        try:
            self.genres:list[str] = data['genres']
        except KeyError:
            self.genres = ['N/A']
        self.images:list[SpotifyImage] = [SpotifyImage(s) for s in data['images']]
        try:
            self.popularity:int = data['popularity']
        except:
            self.popularity = None
        self.total_tracks:int = data['total_tracks']
        try:
            self.tracks:TracksObject = TracksObject(data['tracks'])
        except:
            self.tracks = None
        try:
            self.release_date:str = data['release_date']
            self.release_date_precision:str = data['release_date_precision']
        except KeyError:
            self.release_date:str = "N/A"
            self.release_date_precision = None
        try:
            self.copyrights:list[CopyrightObject] = [CopyrightObject(c) for c in data['copyrights']]
        except KeyError:
            self.copyrights = []
        self.name = data['name']
        super().__init__(data)

    def __str__(self):
        return f'{self.name}\n{", ".join([artist.name for artist in self.artists])}\nReleased {self.release_date}\nGenres: {", ".join(self.genres)}\nTrack count: {self.total_tracks}'
    def __repr__(self):
        return f'{self.name} by {", ".join([artist.name for artist in self.artists])}'