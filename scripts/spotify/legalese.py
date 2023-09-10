# I couldn't think of a good name for this, considering "copyright" is already used by Python.

class CopyrightObject():
    """
    Custom object class to represent the `copyrights` field of an object returned by the Spotify API.

    Class variables:
    * str `text` - The copyright text.
    * str `type` - The copyright type. This is "C" or "P". "P" is used for the performance copyright.
    """
    def __init__(self,data:dict[str,str]) -> None:
        self.text = data['type']
        self.type = data['text']