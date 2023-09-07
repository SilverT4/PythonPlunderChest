from dotenv import load_dotenv
from spotipy import Spotify,SpotifyException,SpotifyOAuth,SpotifyClientCredentials
from os import getenv
load_dotenv()
# Set SPOTIPY_AUTH_SCOPE in your .env file to use it as your auth scope. Also, the .env file should be in the same directory as the script *calling* this module, NOT the directory of this module.
auth_scope = getenv("SPOTIPY_AUTH_SCOPE","user-read-currently-playing user-read-playback-state playlist-read-private playlist-read-collaborative user-top-read user-read-recently-played user-read-private")
authWarns = {"user-read-currently-playing": "WARNING: Your auth scope environment variable is missing the \"user-read-currently-playing\" scope. You will be unable to get the currently playing track for your profile.",
"user-read-playback-state": "WARNING: Your auth scope environment variable is missing the \"user-read-playback-state\" scope. You will be unable to get the current playback state from Spotify.",
"user-modify-playback-state": "WARNING: Your auth scope environment variable is missing the \"user-modify-playback-state\" scope. If you include playback controls in your application, they will not work!",
"playlist-read-private": "INFO: Your auth scope environment variable is missing the \"playlist-read-private\" scope. This will not cause any code-breaking issues, but private playlists will not be returned by Spotify.",
"playlist-read-collaborative": "INFO: Your auth scope environment variable is missing the \"playlist-read-collaborative\" scope. This will not cause any code-breaking issues, but collaborative playlists will not be returned by Spotify.",
"user-top-read": "WARNING: Your auth scope environment variable is missing the \"user-top-read\" scope. If your code relies on this scope, it will not work.",
"user-read-recently-played": "INFO: Your auth scope environment variable is missing the \"user-read-recently-played\" scope. This will not cause many code-breaking issues unless this scope is needed for your application.",
"user-read-private": "INFO: Your auth scope environment variable is missing the \"user-read-private\" scope. This will not cause any code-breaking issues unless this scope is needed for your application."}

for key,value in authWarns.items():
    if not key in auth_scope:
        print(value)

canModifyPlaybackState = "user-modify-playback-state" in auth_scope
auth = SpotifyOAuth(show_dialog=True,open_browser=True,scope=auth_scope)

cli = Spotify(auth_manager=auth)
