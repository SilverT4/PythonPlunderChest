from typing import Any
class ExternalURLs():
    """
    Custom Python class object to represent a list of external URLs for a Spotify object.

    Variables:
    * `spotify` - str, The Spotify URL for the object.
    """
    def __init__(self, data:dict[str,Any]) -> None:
        self.spotify:str = data['spotify']

class ExternalIDs():
    """
    Custom python class object to represent the known external IDs of a Spotify object.

    Variables:
    * str `isrc` - [International Standard Recording Code](http://en.wikipedia.org/wiki/International_Standard_Recording_Code)
    * str `ean` - [International Article Number](http://en.wikipedia.org/wiki/International_Article_Number_%28EAN%29)
    * str `upc` - [Universal Product Code](http://en.wikipedia.org/wiki/Universal_Product_Code)
    """
    def __init__(self,data:dict[str,str]) -> None:
        self.isrc = data['isrc']
        self.ean = data['ean']
        self.upc = data['upc']