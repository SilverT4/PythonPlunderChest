from typing import Any
from spotify.baseObject import SpotifyObject
from spotify.externalStuff import *
from spotify.artist import *
class LinkedTrack(SpotifyObject):
    """
    Custom subclass object to represent information of an originally requested track, if a track has been relinked.

    Subclass-specific variables:
    * custom object `external_urls` - external URLs for the track.
    """
    def __init__(self, data:dict[str,Any]):
        self.external_urls:ExternalURLs = data['external_urls']
        super().__init__(data)
class SimplifiedTrack(SpotifyObject):
    """
    Custom subclass object to represent a track within in album or artist object.
    
    Subclass-specific variables:
    * list `artists` - self-explanatory.
    * list `available_markets` - a list of markets in which the track is available, identified by their respective [ISO-3166 alpha 2](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) codes
    * int `disc_number` - self-explanatory. Usually 1.
    * int `duration_ms` - the track length in milliseconds.
    * bool `explicit` - self-explanatory.
    * custom object `external_urls` - external URLs for the track.
    * bool `is_playable` - True if the track is playable in the given market. Not included unless [Track Relinking](https://developer.spotify.com/documentation/web-api/concepts/track-relinking) is applied.
    * custom object `linked_from` - Only part of the response if Track Relinking is applied and track linking exists. This track contains details about the originally requested track. Otherwise, is None.
    * custom object `restrictions` - Included if a content restriction is applied. None if not.
    * str `name` - self-explanatory.
    * str `preview_url` - A URL to a 30-second preview of the track in MP3 format. This will be None if it's not included.
    * int `track_number` - self-explanatory.
    * bool `is_local` - True if the track is from a local file.
    """
    def __init__(self, data: dict[str, Any]):
        self.artists:list[SimplifiedArtist] = [SimplifiedArtist(js) for js in data['artists']]
        self.available_markets:list[str] = data['available_markets']
        self.disc_number:int = data['disc_number']
        self.duration_ms:int = data['duration_ms']
        self.explicit:bool = data['explicit']
        try:
            self.is_playable:bool = data['is_playable']
        except KeyError:
            pass
        try:
            self.linked_from:LinkedTrack = LinkedTrack(data['linked_from'])
        except KeyError:
            pass
        try:
            self.restrictions:Any = data['restrictions']
        except KeyError:
            pass
        self.name:str = data['name']
        self.preview_url:str|None = data['preview_url']
        self.track_number:int = data['track_number']
        self.is_local:bool = data['is_local']
        super().__init__(data)

class Track(SpotifyObject):
    """
    Custom subclass to represent a Spotify track.

    Subclass-specific variables:
    * custom object `album` - The album on which the track appears.
    * list `artists` - self-explanatory.
    * list `available_markets` - a list of markets in which the track is available, identified by their respective [ISO-3166 alpha 2](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) codes
    * int `disc_number` - self-explanatory. Usually 1.
    * int `duration_ms` - the track length in milliseconds.
    * bool `explicit` - self-explanatory.
    * custom object `external_ids` - known external IDs for the track.
    * custom object `external_urls` - external URLs for the track.
    * bool `is_local` - whether the track comes from a local file.
    * bool `is_playable` - True if the track is playable in the given market. Not included unless [Track Relinking](https://developer.spotify.com/documentation/web-api/concepts/track-relinking) is applied.
    * custom object `linked_from` - Only part of the response if Track Relinking is applied and track linking exists. This track contains details about the originally requested track. Otherwise, is None.
    * str `name` - self-explanatory.
    * int `popularity` - popularity of the track. The value will be between 0 and 100, with 100 being the most popular. The popularity is calculated by algorithm and is based, in the most part, on the total number of plays the track has had and how recent those plays are.
Generally speaking, songs that are being played a lot now will have a higher popularity than songs that were played a lot in the past. Duplicate tracks (e.g. the same track from a single and an album) are rated independently. Artist and album popularity is derived mathematically from spotify.track popularity. (Source: [Spotify](https://developer.spotify.com/documentation/web-api/reference/get-track))
    * str `preview_url` - a link to a 30-second preview of the track in MP3 format. Will be None if not provided.
    * custom object `restrictions` - Included if a content restriction is applied. None if not.
    * int `track_number` - self-explanatory.
    """
    def __init__(self, data: dict[str, Any]):
        try:
            from spotify.album import Album
            self.album:Album = Album(data['album'])
        except ImportError:
            self.album = Album(data['album'])
        self.artists:list[Artist] = [Artist(js) for js in data['artists']]
        self.disc_number:int = data['disc_number']
        self.duration_ms:int = data['duration_ms']
        self.explicit:bool = data['explicit']
        self.external_ids:ExternalIDs = data['external_ids']
        self.is_local:bool = data['is_local']
        self.name:str = data['name']
        self.popularity:int = data['popularity']
        self.preview_url:str|None = data['preview_url']
        self.track_number:int = data['track_number']
        self.widgetText = f'{self.name}\n{", ".join(artist.name for artist in self.artists)}\n{self.album.name}'
        if self.album:
            self.widgetImg = self.album.imgID
        else:
            self.widgetImg = ""
        try:
            self.is_playable:bool = data['is_playable']
        except KeyError:
            pass
        try:
            self.linked_from:LinkedTrack = LinkedTrack(data['linked_from'])
        except KeyError:
            pass
        try:
            self.restrictions:Any = data['restrictions']
        except KeyError:
            pass
        super().__init__(data)