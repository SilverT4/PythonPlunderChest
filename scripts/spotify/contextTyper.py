from spotify.album import Album
from spotify.artist import Artist
from spotify.podcast import Show
from spotify.playlist import Playlist
from typing import Literal
from dotenv import load_dotenv
from spotipy import Spotify,SpotifyException,SpotifyClientCredentials
cli = Spotify(client_credentials_manager=SpotifyClientCredentials())
def contextObject(type:Literal['album','artist','show','playlist'],id:str):
    match type:
        case 'album':
            return Album(cli.album(id,market='US'))
        case 'artist':
            return Artist(cli.artist(id,market='US'))
        case 'playlist':
            return Playlist(cli.playlist(id,market='US'))
        case 'show':
            return Show(cli.show(id,market='US'))
        case _:
            raise ValueError("Unrecognized context type: ",type,id)