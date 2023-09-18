link = "https://is.gd/WVZvnI" # let the script surprise you idk
import random,subprocess

chamber = [None,None,link,None,None,None]
random.shuffle(chamber)

if random.choice(chamber) == link:
    executable = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    subprocess.Popen(executable + " --app=" + link)
    print("lmao bad luck")
else:
    print("you're safe... for now. run again to play again.")