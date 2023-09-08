from typing import Any
from spotify.SpotifyClient import cli
from spotify.baseObject import SpotifyObject
from spotify.legalese import CopyrightObject
class Chapter(SpotifyObject):
    """
    Custom object subclass to represent a Spotify audiobook chapter.

    Subclass-specific variables:
    * NoneType or str `audio_preview_url` - A URL to a 30-second preview of the chapter. Sets to None if unavailable.
    * list `available_markets` - The markets of which the chapter is available, defined by their respective [ISO 3166-1 alpha 2](http://en.wikipedia.org/wiki/ISO_3166-1_alpha-2) codes.
    * int `chapter_number` - Self-explanatory.
    * str `description` - Self-explanatory.
    * str `html_description` - HTML friendly version of the description.
    * int `duration_ms` - The duration in milliseconds
    * bool `explicit` - Whether the chapter contains explicit content
    * str `release_date` - Chapter release date
    * str `release_date_precision` - Precision of the release date.
    * bool `is_playable` - True if the chapter is playable in the given market. Not included unless [Track Relinking](https://developer.spotify.com/documentation/web-api/concepts/track-relinking) is applied.
    * custom object `audiobook` - The Audiobook this chapter belongs to.
    * int `chapter_number` - Self-explanatory.
    """
    def __init__(self, data: dict[str, Any]):
        self.description:str = data['description'] if 'description' in data else None
        self.chapter_number:int = data['chapter_number'] if 'chapter_number' in data else None
        self.duration_ms:int = data['duration_ms'] if 'duration_ms' in data else None
        self.explicit:bool = data['explicit'] if 'explicit' in data else None
        self.languages:list = data['languages'] if 'languages' in data else None
        self.name:str = data['name'] if 'name' in data else None
        self.audio_preview_url:str|None = data['audio_preview_url'] if 'audio_preview_url' in data else None
        self.release_date:str = data['release_date'] if 'release_date' in data else None
        self.release_date_precision:str = data['release_date_precision'] if 'release_date_precision' in data else None
        self.is_playable:bool = data['is_playable'] if 'is_playable' in data else None
        self.html_description:str = data['html_description'] if 'html_description' in data else None
        self.audiobook:dict = data['audiobook'] if 'audiobook' in data else None

        super().__init__(data)

class Audiobook(SpotifyObject):
    """
    Custom subclass object to represent an Audiobook returned by the Spotify API.
    
    Subclass-specific variables:
    * list `authors` - The authors of the audiobook
    * list `chapters` - A list of custom objects representing each chapter of the audiobook
    * str `description` - Self-explanatory.
    * str `edition` - The edition of the audiobook.
    * list `languages` - Self-explanatory.
    * str `media_type` - The media type of the audiobook.
    * list `narrators` - The narrator(s) of the audiobook.
    """
    def __init__(self, data: dict[str, Any]):
        self.authors:list = data['authors'] if 'authors' in data else None
        self.chapters:list[Chapter] = [Chapter(c) for c in data['chapters']] if 'chapters' in data else None
        self.copyrights:list[CopyrightObject] = [CopyrightObject(c) for c in data['copyrights']] if 'copyrights' in data else None
        self.description:str = data['description'] if 'description' in data else None
        self.edition:str = data['edition'] if 'edition' in data else None
        self.explicit:bool = data['explicit'] if 'explicit' in data else None
        self.external_urls:dict = data['external_urls'] if 'external_urls' in data else None
        self.html_description:str = data['html_description'] if 'html_description' in data else None
        self.languages:list = data['languages'] if 'languages' in data else None
        self.media_type:str = data['media_type'] if 'media_type' in data else None
        self.name:str = data['name'] if 'name' in data else None
        self.narrators:list = [n['name'] for n in data['narrators']] if 'narrators' in data else None
        self.publisher:str = data['publisher'] if 'publisher' in data else None
        self.total_chapters:int = data['total_chapters'] if 'total_chapters' in data else None

        super().__init__(data)