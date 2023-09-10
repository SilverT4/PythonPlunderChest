from typing import Any,Literal
from spotify.baseObject import SpotifyObject
from spotify.image import SpotifyImage
class SpotifyIterable(SpotifyObject):
    """
    Custom subclass object to represent any Spotify API response in a format similar to the following:

    ```json
    {
        "href": "string",
        "limit": 0,
        "next": "string",
        "offset": 0,
        "previous": null,
        "limit": 69,
        "items": [...]
    }
    ```

    Subclass-specific variables:
    * int `limit` - The limit of objects.
    * str `next` - API endpoint URL for the next page of objects.
    * str `previous` - Ditto, but for the previous page.
    * int `offset` - Current page offset.
    * int `total` - Total objects on this page of objects.
    * list `items` - The list of objects. This can be any SpotifyObject. **This is non-subtype specific.**
    """
    def __init__(self,data:dict[str,Any],objType:Literal['album','artist','audiobook','chapter','episode','show','track'],create:SpotifyObject=SpotifyObject):
        self.limit:int = data['limit'] if 'limit' in data else None
        self.next:str = data['next'] if 'next' in data else None
        self.previous:str = data['previous'] if 'previous' in data else None
        self.offset:int = data['offset'] if 'offset' in data else None
        self.total:int = data['total'] if 'total' in data else None
        self.items:list[create] = [create(so) for so in data['items']] if 'items' in data else []
        self.itemType = objType
        super().__init__(data)

    def __str__(self):
        return f'Iterable object for {self.itemType}s\nItem count: {self.total}\nOffset: {self.offset}\nNext page: {self.next}\nPrevious page: {self.previous}'