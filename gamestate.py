from character import Character
from pathlib import Path
import random
from preprocessor import Preprocessor
import sys
import time
from threading import Timer

import pygame
from pygame.locals import *

from renderer import DISPLAYSURF
from renderer import WINHEIGHT, WINWIDTH

# For textboxes
COLOR_INACTIVE = pygame.Color('lightskyblue3')
COLOR_ACTIVE = pygame.Color('dodgerblue2')
TEXT_SIZE = 25
textEdgeBufferW = 40
textEdgeBufferH = 20
backspacePressed = False
backspaceStart = time.time()

class OutputBox:
    def __init__(self, x, y, w, h, text=''):
        self.FONT = pygame.font.Font(None, TEXT_SIZE)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def scrolling(self, args):
        #myself = args.self
        dialogue = args.dialogue
        letter_i = args.letter_i

        print(self.text)
        self.text = dialogue[:letter_i]
        # Re-render the text.
        self.txt_surface = self.FONT.render(self.text, True, self.color)

        if len(self.text) < len(dialogue):
            #time.sleep(.5)
            #self.scrolling(dialogue, letter_i+1)
            
            t = Timer(0.5, self.scrolling(), args=(self, dialogue, letter_i+1)).start()

    def handle_event(self, game_state, event):
        #load the next dialogue text if available
        if event.type == pygame.KEYDOWN:   
  
            if event.key == pygame.K_q:
                self.text = ""
                # erase the text
                pygame.draw.rect(DISPLAYSURF, (50,50,50), self.rect)
                if game_state.currentDialogue <= len(game_state.script):
                    for letter in game_state.script[game_state.currentDialogue]:
                        self.text = self.text + letter
                    
                    # Re-render the text.
                    self.txt_surface = self.FONT.render(self.text, True, self.color)
                    #    time.sleep(.1)

                    game_state.currentDialogue += 1
                else:
                    bob = True
                    #what to do when they are done talking?

    def update(self):
        global backspaceStart
        # Resize the box if the text is too long.
        #if self.txt_surface.get_width() < screenWidth - textEdgeBufferW/2:
        #    width = max(200, self.txt_surface.get_width()+10)
        #    self.rect.w = width
                
    def draw(self, screen):
        pygame.draw.rect(screen, (50,50,50), self.rect)
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.FONT = pygame.font.Font(None, TEXT_SIZE)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, game_state, event):
        global backspacePressed, backspaceStart
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text) #<<<<<<<<<<<<<<<<<<<<<<< here is where a character's eliza responds
                    #handleAI(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                    backspacePressed = True
                    backspaceStart = time.time()
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.color)
        if event.type == pygame.KEYUP:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    backspacePressed = False

    def update(self):
        global backspacePressed, backspaceStart
        # Resize the box if the text is too long.
        #if self.txt_surface.get_width() < screenWidth - textEdgeBufferW/2:
        #    width = max(200, self.txt_surface.get_width()+10)
        #    self.rect.w = width

        #for debugging backspace
        #print(str(backspacePressed)+" "+str(backspaceStart))

        #delete characters when holding backspace down
        if time.time() - backspaceStart > 0.35:
            if backspacePressed:
                backspaceStart += .05
                self.text = self.text[:-1]
                self.txt_surface = self.FONT.render(self.text, True, self.color)

    def draw(self, screen):

        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)

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
        self.currentDialogue = 1
        self.script = {1:"i want to talk to you",2:"its important",3:"i think you are pregnant"}

        output_box = OutputBox(textEdgeBufferW/2, WINHEIGHT - textEdgeBufferH - TEXT_SIZE*3, WINWIDTH - textEdgeBufferW, TEXT_SIZE*2)
        input_box2 = InputBox(textEdgeBufferW/2, WINHEIGHT - textEdgeBufferH - TEXT_SIZE, WINWIDTH - textEdgeBufferW, TEXT_SIZE)
        self.text_boxes = [output_box, input_box2]

        self.characters = [
            Character("Robby", "assets/robot.png", "assets/robot_sprite.png", "scripts/characters/robot.txt"),
            Character("Alicia", "assets/girl.png", "assets/girl_sprite.png", "scripts/characters/girl.txt"),
            Character("George", "assets/monster.png", "assets/monster_sprite.png", "scripts/characters/monster.txt"),
            Character("Alfred", "assets/nervous.png", "assets/nervous_sprite.png", "scripts/characters/nervous.txt"),
            Character("Mark", "assets/trenchcoat.png", "assets/trenchcoat_sprite.png", "scripts/characters/trenchcoat.txt")
        ]
        #self.initCharacters()

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
                characters[characterIndex].eliza.combined_script += content
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
        characters[helped].eliza.combined_script += pre.replace('scripts/clues/bags1.txt',{'helped':helped,'killer':killerIndex})
        characters[helpwitness].eliza.combined_script += pre.replace('scripts/clues/bags2.txt',{'helped':helped,'helpwitness':helpwitness})

        # scared
        scared = randomIndex()
        scared_witness = randomIndex()
        characters[scared].eliza.combined_script += pre.replace('scripts/clues/scared1.txt',{'scared':scared,'killer':killerIndex})
        characters[scared_witness].eliza.combined_script += pre.replace('scripts/clues/scared2.txt',{'scared':scared,'scared_witness':scared_witness})

        # lunch
        lunch = randomIndex()
        characters[lunch].eliza.combined_script += pre.replace('scripts/clues/lunch.txt',{'lunch':lunch})

        # bathroom
        bathroom = randomIndex()
        bathroom_witness = randomIndex()
        sick_witness = randomIndex()
        characters[bathroom_witness].eliza.combined_script += pre.replace('scripts/clues/bathroom1.txt',{'bathroom':bathroom,'bathroom_witness':bathroom_witness})
        characters[sick_witness].eliza.combined_script += pre.replace('scripts/clues/bathroom2.txt',{'bathroom':bathroom,'sick_witness':sick_witness})

        # untrustworthy
        suspicious = randomIndex()
        suspect = randomIndex()
        characters[suspicious].eliza.combined_script += pre.replace('scripts/clues/untrustworthy.txt',{'suspicious':suspicious,'suspect':suspect})

        for character in characters:
            character.load()