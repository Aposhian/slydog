import pygame
from pygame.locals import *

from gamestate import GameState
from renderer import startScreen

def main():
    startScreen() # show the title screen until the user presses a key

    game_state = GameState()

    pygame.init()
    FPSCLOCK = pygame.time.Clock()

