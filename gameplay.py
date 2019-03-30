import sys
import pygame
from pygame.locals import *

from gamestate import GameState
from renderer import render, renderStartScreen

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def startScreen(FPSCLOCK):
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""

    renderStartScreen()

    while True: # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()

def main(game_state):
    FPSCLOCK = pygame.time.Clock()

    pygame.init()

    startScreen(FPSCLOCK) # show the title screen until the user presses a key

    mapNeedsRedraw = True

    mapSurf = None

    # initialize_render(game_state)

    while True: # main game loop
        # Reset these variables:
        playerMoveTo = None

        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                # Player clicked the "X" at the corner of the window.
                terminate()

            elif event.type == KEYDOWN:
                # Handle key presses
                if event.key == K_LEFT:
                    playerMoveTo = LEFT
                elif event.key == K_RIGHT:
                    playerMoveTo = RIGHT
                elif event.key == K_UP:
                    playerMoveTo = UP
                elif event.key == K_DOWN:
                    playerMoveTo = DOWN

                elif event.key == K_ESCAPE:
                    terminate() # Esc key quits.

        if playerMoveTo != None:
            # If the player pushed a key to move, make the move
            # (if possible) and push any stars that are pushable.
            moved = makeMove(game_state, playerMoveTo)

            if moved:
                mapNeedsRedraw = True
            
            # TODO: Add bounding box condition (and counters to track it in gamestate)
            # if playerMoveTo == RIGHT:
            # elif layerMoveTo == LEFT:
            # elif layerMoveTo == UP:
            # elif layerMoveTo == DOWN:

        # Render
        mapSurf = render(game_state, mapSurf, mapNeedsRedraw)
        mapNeedsRedraw = False
        pygame.display.update() # draw DISPLAYSURF to the screen.
        FPSCLOCK.tick()

def terminate():
    pygame.quit()
    sys.exit()

def isWall(mapObj, x, y):
    """Returns True if the (x, y) position on
    the map is a wall, otherwise return False."""

    if x < 0 or x >= len(mapObj) or y < 0 or y >= len(mapObj[x]):
        return False # x and y aren't actually on the map.
    elif mapObj[x][y] in ('#', 'x'):
        return True # wall is blocking
    return False

def isBlocked(game_state, x, y):
    """Returns True if the (x, y) position on the map is
    blocked by a wall or star, otherwise return False."""

    if isWall(game_state.map, x, y):
        return True

    elif x < 0 or x >= len(game_state.map) or y < 0 or y >= len(game_state.map[x]):
        return True # x and y aren't actually on the map.

    return False


def makeMove(game_state, playerMoveTo):
    """Given a map and game state object, see if it is possible for the
    player to make the given move. If it is, then change the player's
    position (and the position of any pushed star). If not, do nothing.

    Returns True if the player moved, otherwise False."""

    # Make sure the player can move in the direction they want.
    playerx, playery = game_state.player_pos

    # The code for handling each of the directions is so similar aside
    # from adding or subtracting 1 to the x/y coordinates. We can
    # simplify it by using the xOffset and yOffset variables.
    if playerMoveTo == UP:
        xOffset = 0
        yOffset = -1
    elif playerMoveTo == RIGHT:
        xOffset = 1
        yOffset = 0
    elif playerMoveTo == DOWN:
        xOffset = 0
        yOffset = 1
    elif playerMoveTo == LEFT:
        xOffset = -1
        yOffset = 0

    # See if the player can move in that direction.
    if isWall(game_state.map, playerx + xOffset, playery + yOffset):
        return False
    else:
        # Move the player upwards.
        game_state.player_pos = (playerx + xOffset, playery + yOffset)
        return True

if __name__ == '__main__':
    game_state = GameState()
    main(game_state)
