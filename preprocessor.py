import re
import string

class Preprocessor:
    def __init__(self, characters):
        self.characters = characters
        self.id_to_index = {}

    def getMatch(match):
        id = match.group(0).translate(str.maketrans('','','{}'))
        return characters[id_to_index[id]].name

    def replace(self, path, id_to_index_dictionary):
        id_to_index = id_to_index_dictionary
        with open(path) as file:
            content = file.read()
            s = re.sub('\{.+\}', getMatch, content)
            id_to_index = {}
            return s

