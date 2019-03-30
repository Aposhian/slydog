import sys
import pygame
from pygame.locals import *

from gamestate import GameState
from renderer import render, renderStartScreen, TILEWIDTH, TILEHEIGHT, TILEFLOORHEIGHT
from renderer import HALF_WINHEIGHT, HALF_WINWIDTH

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'
lastImg = "down"

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
    pygame.key.set_repeat(1, 130)

    startScreen(FPSCLOCK) # show the title screen until the user presses a key

    mapNeedsRedraw = True

    mapSurf = None

    # For camera offset logic
    mapWidth = len(game_state.map) * TILEWIDTH
    mapHeight = (len(game_state.map[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT
    MAX_CAM_Y_PAN = abs(HALF_WINHEIGHT - int(mapHeight / 2)) + TILEWIDTH
    MAX_CAM_X_PAN = abs(HALF_WINWIDTH - int(mapWidth / 2)) + TILEHEIGHT

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
                    game_state.currentImg = "left"
                elif event.key == K_RIGHT:
                    playerMoveTo = RIGHT
                    game_state.currentImg = "right"
                elif event.key == K_UP:
                    playerMoveTo = UP
                    game_state.currentImg = "up"
                elif event.key == K_DOWN:
                    playerMoveTo = DOWN
                    game_state.currentImg = "down"
                


                elif event.key == K_ESCAPE:
                    terminate() # Esc key quits.

        if playerMoveTo != None:
            # If the player pushed a key to move, make the move
            # (if possible) and push any stars that are pushable.
            moved = makeMove(game_state, playerMoveTo)

            if game_state.currentImg != lastImg:
                mapNeedsRedraw = True
            if moved:
                if playerMoveTo == RIGHT:
                    game_state.distance_to_bbX += 1
                elif playerMoveTo == LEFT:
                    game_state.distance_to_bbX -= 1
                elif playerMoveTo == UP:
                    game_state.distance_to_bbY += 1
                elif playerMoveTo == DOWN:
                    game_state.distance_to_bbY -= 1
                mapNeedsRedraw = True
            
            # Update camera if player is out of bounding box if possible
            if game_state.outOfBBX and playerMoveTo == RIGHT and game_state.cameraOffsetX > -MAX_CAM_X_PAN:
                game_state.cameraOffsetX -= TILEWIDTH
                game_state.distance_to_bbX -= 1
            elif game_state.outOfBBX and playerMoveTo == LEFT and game_state.cameraOffsetX < MAX_CAM_X_PAN:
                game_state.cameraOffsetX += TILEWIDTH
                game_state.distance_to_bbX += 1
            elif game_state.outOfBBY and playerMoveTo == UP and game_state.cameraOffsetY < MAX_CAM_Y_PAN:
                game_state.cameraOffsetY += TILEFLOORHEIGHT
                game_state.distance_to_bbY -= 1
            elif game_state.outOfBBY and playerMoveTo == DOWN and game_state.cameraOffsetY > -MAX_CAM_Y_PAN:
                game_state.cameraOffsetY -= TILEFLOORHEIGHT
                game_state.distance_to_bbY += 1

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
    elif mapObj[x][y] in ('#', 'x', 'L', 'J'):
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
