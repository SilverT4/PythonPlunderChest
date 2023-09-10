from typing import Any
from spotify.externalStuff import ExternalURLs
from spotify.image import SpotifyImage
class SpotifyObject():
    """
    Base class for Spotify objects. Preferrably should not be directly called, as subclasses of this class will have more suited variables.

    Variables shared by all subclasses:
    * str `id` - the Spotify ID of the object.
    * str `href` - link to the Web API providing full details for the object.
    * str `type` - the object type.
    * str `uri` - the Spotify URI of the object.
    * list `available_markets` - a list of markets in which the track is available, identified by their respective [ISO-3166 alpha 2](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) codes
    * custom object `external_urls` - the external URLs for the object. if unspecified by the subclass in init, this is None.
    * list `images` - a list of images for the object. can be empty.
    """
    def __init__(self,data:dict[str,Any]):
        """
        Initialise the base Spotify object class.

        This sets the following variables:
        `id`, `href`, `type`, `uri`, `available_markets`, `external_urls`, `images`

        If any of following variables are not included when calling a subclass object, they will instead be set to None.

        If the `images` variable is not included, it will be set to an empty `list` object.
        """
        try:
            self.id:str = data['id']
            self.imgID = self.id
        except KeyError:
            self.id = None
            self.imgID = None
        try:
            self.type:str = data['type']
        except KeyError:
            self.type = None
        try:
            self.uri:str = data['uri']
        except KeyError:
            self.uri = None
        try:
            self.href:str = data['href']
        except KeyError:
            self.href = None
        try:
            self.available_markets:list[str] = data['available_markets']
        except KeyError:
            self.available_markets = None # may not always exist
        try:
            self.external_urls:ExternalURLs = ExternalURLs(data['external_urls'])
        except KeyError:
            self.external_urls = None
        try:
            self.images:list[SpotifyImage] = [SpotifyImage(js) for js in data['images']]
            self.image = self.images[0] if len(self.images) > 0 else None
        except KeyError:
            self.images = []
            self.image = None
        self.rawData:dict[str,Any] = data

    def __init_subclass__(cls) -> None:
        pass