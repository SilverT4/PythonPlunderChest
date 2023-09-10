from typing import Any
from spotify.baseObject import SpotifyObject
class Episode(SpotifyObject):
    """
    Custom subclass object to represent a podcast episode object.
    
    Subclass-specific variables:
    * str `audio_preview_url` - URL to a 30-second preview in MP3 format. sets to None if unavailable.
    * str `description` - self-explanatory.
    * str `html_description` - HTML-friendly version of `description`
    * int `duration_ms` - duration of the episode in milliseconds.
    * bool `explicit` - self-explanatory.
    * bool `is_externally_hosted` - represents whether the show is hosted on the Spotify CDN or not.
    * bool `is_playable` - True if the episode is playable in the given market.
    * **deprecated** str `language` - language used in the episode, specified by its [ISO-639](https://en.wikipedia.org/wiki/ISO_639) code. **Deprecated: This field is deprecated and might be removed in the future. Instead, use the `languages` field.**
    * list `languages` - languages used in the episode, identified by their respective [ISO-639](https://en.wikipedia.org/wiki/ISO_639) codes.
    * str `release_date` - the episode's release date
    * str `release_date_precision` - precision of which the `release_date` is known. can be `day`, `month`, or `year`
    * custom object `show` - represents the episode's show. if this class is being called *from* the `Show` class, this is None.
    """
    def __init__(self, data: dict[str, Any]):
        self.audio_preview_url:str|None = data['audio_preview_url']
        self.name = data['name']
        self.description:str = data['description']
        self.html_description:str = data['html_description']
        self.duration_ms:int = data['duration_ms']
        self.explicit:bool = data['explicit']
        self.is_externally_hosted:bool = data['is_externally_hosted']
        self.is_playable:bool = data['is_playable']
        self.language:str = data['language']
        self.languages:list[str] = data['languages']
        self.release_date:str = data['release_date']
        self.release_date_precision:str = data['release_date_precision']
        try:
            self.show:Show = Show(data['show'])
            self.widgetText = self.show.widgetText
        except KeyError:
            self.show = None
            self.widgetText = self.name+'\n\n'
        super().__init__(data)
class EpisodeList():
    """
    Custom class object to represent the list of episodes in a Spotify podcast.

    Variables:
    * str `href` - Link to the Web API returning full details.
    * int `limit` - maximum number of items in the response.
    * str `next` - URL to the next page of items, or None if not provided.
    * str `previous` - ditto with `next`
    * int `offset` - offset of the items returned.
    * int `total` - self-explanatory.
    * list `items` - the episodes of the podcast.
    """
    def __init__(self,data:dict[str,str|int|None]) -> None:
        self.href:str = data['href']
        self.limit:int = data['limit']
        self.next:str|None = data['next']
        self.previous:str|None = data['previous']
        self.offset:int = data['offset']
        self.total:int = data['total']
        self.items:list[Episode] = [Episode(e) for e in data['items']]
class Show(SpotifyObject):
    """
    Custom subclass object to represent a podcast on Spotify.

    Subclass-specific variables:
    * list `copyrights` - the show's copyright statements.
    * str `description` - self-explanatory.
    * str `html_description` - an HTML-friendly version of the description. (I wonder if I can format HTML stuff in Tkinter?)
    * bool `explicit` - whether the show is explicit or not.
    * bool `is_externally_hosted` - represents whether the show is hosted on the Spotify CDN or not.
    * list `languages` - lists the languages in the show, identified by their respective [ISO-639](https://en.wikipedia.org/wiki/ISO_639) codes.
    * str `media_type` - the media type of the show.
    * str `name` - self-explanatory.
    * str `publisher` - the show's publisher.
    * int `total_episodes` - self-explanatory
    * list `episodes` - self-explanatory.
    """
    def __init__(self, data: dict[str, Any]):
        self.copyrights:list[Any] = data['copyrights']
        self.description:str = data['description']
        self.html_description:str = data['html_description']
        self.explicit:bool = data['explicit']
        self.is_externally_hosted:bool = data['is_externally_hosted']
        self.languages:list[str] = data['languages']
        self.media_type:str = data['media_type']
        self.name:str = data['name']
        self.publisher:str = data['publisher']
        self.total_episodes:int = data['total_episodes']
        self.episodes = EpisodeList(data['episodes'])
        self.widgetText = f'{self.name}\n{self.publisher}\n'
        super().__init__(data)