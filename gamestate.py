from character import Character
from pathlib import Path
import random
from preprocessor import Preprocessor

class GameState:

    def __init__(self):
        self.map = [
            ['#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', '#', '#', ' ', ' ', '#', '#', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', '#', '#', ' ', ' ', '#', '#', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', '#', '#', ' ', ' ', '#', '#', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', 'J', 'J', ' ', ' ', 'J', 'J', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', 'L', 'L', ' ', ' ', 'L', 'L', '#'],
            ['#', '#', '#', '#', '#', '#', '#', '#']
        ]

        self.player_pos = (len(self.map) // 2, len(self.map[0]) // 2)
        self.cameraOffsetX = 0
        self.cameraOffsetY = 0
        self.currentImg = "down"

        self.distance_to_bbX = 0
        self.distance_to_bbY = 0
        self.BOUNDING_BOX_RADIUS = 4
        self.background_scroll_x = 0

        self.characters = [
            Character("Robby", "assets/robot.png", "assets/robot_sprite.png", "robot.txt"),
            Character("Alicia", "assets/girl.png", "assets/girl_sprite.png", "girl.txt"),
            Character("George", "assets/monster.png", "assets/monster_sprite.png", "monster.txt"),
            Character("Alfred", "assets/nervous.png", "assets/nervous_sprite.png", "nervous.txt"),
            Character("Mark", "assets/trenchcoat.png", "assets/trenchcoat_sprite.png", "trenchcoat.txt")
        ]
        self.initCharacters()

    @property
    def outOfBBX(self):
        return abs(self.distance_to_bbX) > self.BOUNDING_BOX_RADIUS

    @property
    def outOfBBY(self):
        return abs(self.distance_to_bbY) > self.BOUNDING_BOX_RADIUS

    def initCharacters(self):
        # Randomly assign leadins and clues

        # leadins
        availableCharacters = list(range(len(characters)))
        for filename in Path("scripts/leadins").glob("**/*.txt"):
            characterIndex = int((random.random() * len(availableCharacters)) // 1)
            with open(filename) as leadin_script:
                content = leadin_script.read()
                characters[characterIndex].eliza.combined_script.append(content)
            availableCharacters.remove(characterIndex)
            if len(availableCharacters) == 0:
                break
        
        # clues
        def randomIndex():
            return int((random.random() * len(characters)) // 1)

        pre = Preprocessor(characters)

        # Assign killer
        killerIndex = randomIndex()

        # bags
        helped = randomIndex()
        helpwitness = randomIndex()
        characters[helped].eliza.combined_script.append(pre.replace('scripts/clues/bags1.txt',{'helped':helped,'killer':killerIndex}))
        characters[helpwitness].eliza.combined_script.append(pre.replace('scripts/clues/bags2.txt',{'helped':helped,'helpwitness':helpwitness}))

        # scared
        scared = randomIndex()
        scared_witness = randomIndex()
        characters[scared].eliza.combined_script.append(pre.replace('scripts/clues/scared1.txt',{'scared':scared,'killer':killerIndex}))
        characters[scared_witness].eliza.combined_script.append(pre.replace('scripts/clues/scared2.txt',{'scared':scared,'scared_witness':scared_witness}))

        # lunch
        lunch = randomIndex()
        characters[lunch].eliza.combined_script.append(pre.replace('scripts/clues/lunch.txt',{'lunch':lunch}))

        # bathroom
        bathroom = randomIndex()
        bathroom_witness = randomIndex()
        sick_witness = randomIndex()
        characters[bathroom_witness].eliza.combined_script.append(pre.replace('scripts/clues/bathroom1.txt',{'bathroom':bathroom,'bathroom_witness':bathroom_witness}))
        characters[sick_witness].eliza.combined_script.append(pre.replace('scripts/clues/bathroom2.txt',{'bathroom':bathroom,'sick_witness':sick_witness}))

        # untrustworthy
        suspicious = randomIndex()
        suspect = randomIndex()
        characters[suspicious].eliza.combined_script.append(pre.replace('scripts/clues/untrustworthy.txt',{'suspicious':suspicious,'suspect':suspect}))

        for character in characters:
            character.load()