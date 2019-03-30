import re
import string
from pathlib import Path

path = "testScript.txt"

characters = {'0':,'1':,'2':,'3':,'4':}

def getMatch(match):
    id = match.group(0).translate(str.maketrans('','','{}'))
    return characters[id].name

with open(path) as file:
    content = file.read()
    s = re.sub('\{.+\}', getMatch, content)
    print(s)

