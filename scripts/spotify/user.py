from typing import Any,Annotated
from spotify.baseObject import SpotifyObject
from spotify.image import SpotifyImage
import humanize
class User(SpotifyObject):
    """
    Custom subclass object representing a Spotify user.

    Subclass-specific variables:
    * str `display_name` - The user's display name. Sets to None if unavailable.
    * custom object `external_urls` - External URLs for the user.
    * int `followers` - The number of followers of this user.
    * list `images` - The user's profile picture in various sizes.
    * str `product` - The user's subscription type. (If applicable.)
    """

    subscriptionTypes = {"premium": "Spotify Premium User", "free": "Spotify Free User", "open": "Spotify Free User"}
    
    def __init__(self, data: dict[str, Any]):
        self.display_name:str = data['display_name']
        try:
            self.product:str = self.subscriptionTypes[data['product']]
        except KeyError:
            self.product:str = "Subscription data unavailable."
        try:
            self.images:list[SpotifyImage] = [SpotifyImage(s) for s in data['images']]
        except KeyError:
            self.images = []
        try:
            self.followers:int = data['followers']['total'] # see artist.py for why i do it like this
        except KeyError:
            self.followers = 0
        self.widgetText = f'{self.display_name}\n{humanize.intcomma(self.followers)} followers'
        super().__init__(data)