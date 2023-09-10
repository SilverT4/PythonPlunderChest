from spotify.SpotifyClient import cli
from spotify.iterator import SpotifyIterable
def get_newReleases(country:str='US',offset:int=0):
    return SpotifyIterable(cli.new_releases(country,offset)['albums'])