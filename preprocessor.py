import re
import string

class Preprocessor:
    def __init__(self, characters):
        self.characters = characters
        self.id_to_index = {}

    def replace(self, path, id_to_index_dictionary):
        def getMatch(match):
            id = match.group(0).translate(str.maketrans('','','{}'))
            return self.characters[id_to_index[id]].name

        id_to_index = id_to_index_dictionary
        with open(path) as file:
            content = file.read()
            s = None
            while True:
                scopy = s
                s = re.sub('\{.+\}', getMatch, content)
                if s == scopy:
                    break
            id_to_index = {}
            return s

