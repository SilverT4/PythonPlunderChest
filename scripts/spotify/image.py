class SpotifyImage():
    '''
    Custom object class to represent an image from the Spotify API.

    Variables:
    * str `url` - The source URL of the image.
    * int `height` - self-explanatory.
    * int `width` - self-explanatory.
    '''
    def __init__(self,data:dict[str,str|int]) -> None:
        self.url:str = data['url']
        self.height:int = data['height']
        self.width:int = data['width']