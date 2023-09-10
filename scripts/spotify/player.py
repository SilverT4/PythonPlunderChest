from typing import Any
from spotify.SpotifyClient import cli
from dotenv import load_dotenv
from spotify.baseObject import SpotifyObject
from spotify.track import Track
from spotify.podcast import Episode
from spotify.contextTyper import contextObject

def playerItem(data:dict[str,Any],curtype:str):
    try:
        if curtype == 'track':
            return Track(cli.track(data['uri']))
        elif curtype == 'episode':
            return Episode(cli.episode(data['uri']))
    except:
        return None
class Device(SpotifyObject):
    """
    Custom subclass object to represent the device on which the authenticated user is currently listening on.

    Subclass-specific variables:
    * bool `is_active` - True if the device is the currently active device.
    * bool `is_private_session` - True if the device is in a private playback session.
    * bool `is_restricted` - If this is True, no Web API commands will be accepted by the device.
    * str `name` - self-explanatory.
    * int `volume_percent` - self-explanatory
    * bool `supports_volume` - Whether the device can be used to set the volume of the audio playback.
    """
    def __init__(self, data: dict[str, Any]):
        """
        Initialise the Device object.

        Special notes: `id` and `volume_percent` can be None.
        """
        self.is_active:bool = data['is_active']
        self.is_private_session:bool = data['is_private_session']
        self.is_restricted:bool = data['is_restricted']
        self.name:str = data['name']
        self.volume_percent:int = data['volume_percent'] if 'volume_percent' in data else 69
        self.supports_volume:bool = data['supports_volume']
        super().__init__(data)
class Context(SpotifyObject):
    """
    Custom subclass object to represent the authenticated user's current player context.

    Subclass-specific variables:

    None.
    """
    def __init__(self, data: dict[str, Any]):
        super().__init__(data)
class Actions():
    """
    Custom object to represent the actions allowed to update the UI based on which playback actions are available in the current context.
    
    Variables:
    * bool `interrupting_playback` - Interrupting playback.
    * bool `pausing` - Pausing.
    * bool `resuming` - Resuming.
    * bool `seeking` - Seeking.
    * bool `skipping_next` - Skipping to the next context.
    * bool `skipping_prev` - Ditto with `skipping_next`, just the previous context.
    * bool `toggling_repeat_context` - Toggling repeat context flag.
    * bool `toggling_shuffle` - Toggling shuffle flag.
    * bool `toggling_repeat_track` - Toggling repeat track flag.
    * bool `transferring_playback` - Transferring playback between devices.
    """
    def __init__(self,deez:dict[str,bool]):
        data = deez['disallows']
        self.interrupting_playback = False if 'interrupting_playback' in data else True
        self.pausing = False if 'playback' in data else True
        self.resuming = False if 'resuming' in data else True
        self.seeking = False if 'seeking' in data else True
        self.skipping_next = False if 'skipping_next' in data else True
        self.skipping_prev = False if 'skipping_prev' in data else True
        self.toggling_repeat_context = False if 'toggling_repeat_context' in data else True
        self.toggling_shuffle = False if 'toggling_shuffle' in data else True
        self.toggling_repeat_track = False if 'toggling_repeat_track' in data else True
        self.transferring_playback = False if 'transferring_playback' in data else True
class Player(SpotifyObject):
    """
    Custom subclass object to represent the authenticated user's player.

    Subclass-specific variables:
    * custom object `device` - The device with which the user is listening on.
    * str `repeat_state` - Repeat mode. Can be `off`, `track`, or `context`.
    * bool `shuffle_state` - Whether shuffle is enabled.
    * custom object `context` - Context object. Can be None.
    * int `timestamp` - Unix Millisecond Timestamp when data was fetched.
    * int `progress_ms` - Current progress into the track or episode. Can be None.
    * bool `is_playing` - self-explanatory.
    * Track or Episode object `item` - the currently playing item.
    * str `currently_playing_type` - The type of the currently playing media. Can be `track`, `episode`, `ad`, or `unknown`.
    * custom object `actions` - Allowed actions based on the current context.
    """
    def __init__(self, data: dict[str, Any]):
        if data:
            self.device:Device = Device(data['device']) if 'device' in data else None
            self.repeat_state:str = data['repeat_state']
            self.shuffle_state:bool = data['shuffle_state']
            self.context = Context(data['context']) if data['context'] else None
            self.timestamp:int = data['timestamp']
            self.progress_ms:int = data['progress_ms']
            self.is_playing:bool = data['is_playing']
            self.currently_playing_type:str = data['currently_playing_type']
            self.item:Track|Episode = playerItem(data['item'],self.currently_playing_type)
            self.actions:Actions = Actions(data['actions'])
        else:
            self.device:Device = None
            self.repeat_state:str = ""
            self.shuffle_state:bool = False
            self.context:Context = None
            self.timestamp:int = 0
            self.progress_ms:int = 0
            self.is_playing:bool = False
            self.currently_playing_type:str = "unknown"
            self.item:Track|Episode = None
            self.actions:Actions = None
        super().__init__(data)