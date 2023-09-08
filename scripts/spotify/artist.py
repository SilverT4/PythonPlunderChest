from typing import Any
from spotify.baseObject import SpotifyObject
from spotify.externalStuff import ExternalURLs
from spotify.image import SpotifyImage
class Artist(SpotifyObject):
    """
    Custom subclass object to represent an Artist returned by the Spotify API

    This sets the following variables, if included in the `data` argument:
    - str `name` - The name of the artist
    - int `followers` - The number of Spotify followers the artist has
    - list `genres` - List of genres associated with the artist
    - int `popularity` - The popularity score of the artist
    """
    def __init__(self, data: dict[str, Any]):
        self.external_urls:ExternalURLs = data['external_urls']
        try:
            self.followers:int = data['followers']['total'] # The API lists 'followers' as an object with an extra 'href' string, but this is always null at this time.
        except KeyError:
            self.followers = None
        try:
            self.genres:list[str] = data['genres']
        except KeyError:
            self.genres = []
        try:
            self.images:list[SpotifyImage] = [SpotifyImage(s) for s in data['images']]
            self.image:SpotifyImage = self.images[0]
        except KeyError:
            self.images = []
        try:
            self.popularity:int = data['popularity']
        except KeyError:
            self.popularity = None
        self.name:str = data['name']
        super().__init__(data)
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name