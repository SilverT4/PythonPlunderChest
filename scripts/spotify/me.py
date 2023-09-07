from typing import Any,Literal
from spotify.baseObject import SpotifyObject
from spotify.artist import Artist
from spotify.track import Track

class MyTopItems(SpotifyObject):
    """
    Custom subclass object to represent the signed-in user's top artists or tracks.
    
    Subclass-specific variables:
    * str `next` and `previous` - these are URLs to the next/previous pages of items. will be None if unavailable.
    * int `offset` - offset of the items
    * int `total` - total number of items.
    * list `items` - will contain either the artists or tracks.
    """
    def __init__(self, data: dict[str, Any], listType:Literal['artists','tracks']):
        data['type'] = listType # so it doesnt error
        data['id'] = None
        data['uri'] = None
        match listType:
            case 'artists':
                self.items:list[Artist] = [Artist(js) for js in data['items']]
            case 'tracks':
                self.items:list[Track] = [Track(js) for js in data['items']]
        self.next:str|None = data['next']
        self.previous:str|None = data['previous']
        self.offset:int = data['offset']
        self.total:int = data['total']
        super().__init__(data)