from typing import Any
from spotify.baseObject import SpotifyObject
from spotify.externalStuff import ExternalURLs
from spotify.image import SpotifyImage
class SimplifiedArtist(SpotifyObject):
    """
    Custom Python subclass object to represent a simplified view of an Artist object.

    Variables specific to this subclass:
    * `external_urls` - custom object, external URLs for the artist.
    * `name` - str, self-explanatory.
    """
    def __init__(self, data: dict[str, Any]):
        """
        Initialise a Simplified Artist object.

        This sets the `external_urls` and `name` variables.
        """
        self.external_urls:ExternalURLs = data['external_urls']
        self.name:str = data['name']
        super().__init__(data)

class Artist(SpotifyObject):
    """
    Custom subclass object to represent an Artist object.

    Subclass-specific variables:
    * custom object `external_urls` - external URLs for the artist.
    * int `followers` - self-explanatory.
    * list `genres` - self-explanatory.
    * list `images` - images of the artist.
    * int `popularity` - popularity of the artist. The value will be between 0 and 100, with 100 being the most popular. The artist's popularity is calculated from the popularity of all the artist's tracks. (Copied from the Spotify documentation)
    * str `name` - self-explanatory.
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
    def __repr__(self):
        return self.name