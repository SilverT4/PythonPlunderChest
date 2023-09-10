# Script to try and work out problems in shit. This will be updated frequently.
from spotify.SpotifyClient import cli
from spotify.util import get_audiobook,get_audiobook_chapters,get_audiobooks
cli.retries = 3
cli.requests_timeout = 5
from json import load
from globals.cleanType import cleanType
a:dict[str,any]=load(open("placeholder.json"))
keys = list(a.keys())
files = [open("s/"+x+".txt","w") for x in a.keys()]
for i in range(11):
    thingy = a[keys[i]]
    keys2 = thingy.keys()
    file = files[i]
    for t in keys2:
        sex = "self.{1}:{0} = data['{1}'] if '{1}' in data else None\n".format(cleanType(type(thingy[t])),t)
        file.write(sex)
    file.close()
