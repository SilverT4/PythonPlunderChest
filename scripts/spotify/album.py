from typing import Any
from spotify.baseObject import SpotifyObject
from spotify.artist import SimplifiedArtist
from spotify.track import SimplifiedTrack
from spotify.image import SpotifyImage
class TracksObject(SpotifyObject):
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
        self.items:list[SimplifiedTrack] = [SimplifiedTrack(js) for js in data['items']]
        super().__init__(self,data)
class Album(SpotifyObject):
    """
    Custom Python object subclass to represent a Spotify Album.

    Variables specific to this subclass:
    * str `album_type` - self-explanatory. Can be "album", "single", or "compilation"
    * list `artists` - self-explanatory.
    * list `genres` - self-explanatory.
    * list `images` - the cover art of the album in various sizes.
    * int `popularity` - self-explanatory. Ranges between 0 to 100, with higher numbers being more popular.
    * int `total_tracks` - self-explanatory.
    * list `tracks` - self-explanatory.
    * str `release_date` - the date the album was first released.
    * str `release_date_precision` - the precision of which the `release_date` value is known. Can be "year", "month", or "day"
    * custom object `restrictions` - Included if a content restriction is applied. None if not.
    """
    def __init__(self, data: dict[str, Any]):
        """
        Initialise the Album class object.

        This sets the `album_type`, `artists`, `genres`, `images`, `popularity`, `total_tracks`, and `tracks` variables.
        """
        self.album_type:str = data['album_type']
        self.artists:list[SimplifiedArtist] = [SimplifiedArtist(js) for js in data['artists']]
        try:
            self.genres:list[str] = data['genres']
        except KeyError:
            self.genres = []
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
        self.name = data['name']
        super().__init__(data)