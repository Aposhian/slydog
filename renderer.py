import time

import pygame
from pygame.locals import *


WINWIDTH = 800 # width of the program's window, in pixels
WINHEIGHT = 600 # height in pixels
HALF_WINWIDTH = int(WINWIDTH / 2)
HALF_WINHEIGHT = int(WINHEIGHT / 2)

# The total width and height of each tile in pixels.
TILEWIDTH = 50
TILEHEIGHT = 85
TILEFLOORHEIGHT = 40

# Because the Surface object stored in DISPLAYSURF was returned
# from the pygame.display.set_mode() function, this is the
# Surface object that is drawn to the actual computer screen
# when pygame.display.update() is called.
DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))

pygame.display.set_caption('Sly Dog')

# A global dict value that will contain all the Pygame
# Surface objects returned by pygame.image.load().
IMAGESDICT = {'bkgd': pygame.image.load('assets/stars background.png').convert(),
              'covered goal': pygame.image.load('assets/Selector.png'),
              'corner': pygame.image.load('assets/Wall_Block_Tall.png'),
              'wall': pygame.image.load('assets/doorsketch.png'),
              'inside floor': pygame.image.load('assets/Plain_Block.png'),
              'outside floor': pygame.image.load('assets/floor tile.png'),
              'title': pygame.image.load('assets/star_title.png'),
              'princess': pygame.image.load('assets/dogspritefront.png'),
              'princessL': pygame.image.load('assets/dogspriteleft.png'),
              'princessR': pygame.image.load('assets/dogspriteright.png'),
              'princessBack': pygame.image.load('assets/dogspriteback.png'),
              'monster': pygame.image.load('assets/monster_sprite.png'),
              'girl': pygame.image.load('assets/girl_sprite.png'),
              'nervous': pygame.image.load('assets/nervous_sprite.png'),
              'trenchcoat': pygame.image.load('assets/trenchcoat_sprite.png'),
              'robot': pygame.image.load('assets/robot_sprite.png'),
              'boy': pygame.image.load('assets/boy.png'),
              'rock': pygame.image.load('assets/Rock.png'),
              'short tree': pygame.image.load('assets/Tree_Short.png'),
              'tall tree': pygame.image.load('assets/Tree_Tall.png'),
              'ugly tree': pygame.image.load('assets/Tree_Ugly.png'),
              'chair': pygame.image.load('assets/chair sprite.png'),
              'middle_wall': pygame.image.load('assets/newwall.png'),       
              'chairFlip': pygame.transform.flip(pygame.image.load('assets/nervous_sprite.png'), True, False)}

# These dict values are global, and map the character that appears
# in the level file to the Surface object it represents.
TILEMAPPING = {'x': IMAGESDICT['corner'],
               '#': IMAGESDICT['wall'],
               'o': IMAGESDICT['inside floor'],
               ' ': IMAGESDICT['outside floor'],
               'L': IMAGESDICT['chair'],
               'W': IMAGESDICT['middle_wall'],
               'n': IMAGESDICT['nervous'],
               'g': IMAGESDICT['girl'],
               'm': IMAGESDICT['monster'],
               'r': IMAGESDICT['robot'],
               't': IMAGESDICT['trenchcoat'],
               'J': IMAGESDICT['chairFlip']}
OUTSIDEDECOMAPPING = {'1': IMAGESDICT['rock'],
                      '2': IMAGESDICT['short tree'],
                      '3': IMAGESDICT['tall tree'],
                      '4': IMAGESDICT['ugly tree']}

PLAYERIMAGES = [IMAGESDICT['princess'],
                IMAGESDICT['princessL'],
                IMAGESDICT['princessR'],
                IMAGESDICT['princessBack'],
                IMAGESDICT['boy']]

# The percentage of outdoor tiles that have additional
# decoration on them, such as a tree or rock.
OUTSIDE_DECORATION_PCT = 20

BRIGHTBLUE = (  0, 170, 255)
WHITE      = (255, 255, 255)
BGCOLOR = (0,0,0)
TEXTCOLOR = (200,200,200)

def overlay(game_state, characterIndex):
    #fade in to black
    for i in range(1, 100):
        s=pygame.Surface((WINWIDTH, WINHEIGHT), pygame.SRCALPHA)
        s.fill((0,0,0,i/20))
        DISPLAYSURF.blit(s, (0,0))
        pygame.display.update()
        time.sleep(.00001)
    # Blit character avatar
    # DISPLAYSURF.blit(IMAGESDICT[game_state.characters[characterIndex].avatar], (0, 0))

def render(game_state, mapSurf, mapNeedsRedraw):

    # Render scrolling background
    bkgd_width = IMAGESDICT['bkgd'].get_rect().width
    rel_x = game_state.background_scroll_x % bkgd_width
    DISPLAYSURF.blit(IMAGESDICT['bkgd'], (rel_x - bkgd_width, 0))
    if rel_x < WINWIDTH:
        DISPLAYSURF.blit(IMAGESDICT['bkgd'], (rel_x, 0))
    game_state.background_scroll_x -= 4

    if mapNeedsRedraw or mapSurf is None:
        mapSurf = drawMap(game_state)

    # Adjust mapSurf's Rect object based on the camera offset.
    mapSurfRect = mapSurf.get_rect()
    mapSurfRect.center = (HALF_WINWIDTH + game_state.cameraOffsetX,
                    HALF_WINHEIGHT + game_state.cameraOffsetY)

    # Draw mapSurf to the DISPLAYSURF Surface object.
    DISPLAYSURF.blit(mapSurf, mapSurfRect)
    return mapSurf

def drawMap(game_state):
    """Draws the map to a Surface object, including the player and
    stars. This function does not call pygame.display.update(), nor
    does it draw the "Level" and "Steps" text in the corner."""

    # mapSurf will be the single Surface object that the tiles are drawn
    # on, so that it is easy to position the entire map on the DISPLAYSURF
    # Surface object. First, the width and height must be calculated.
    mapSurfWidth = len(game_state.map) * TILEWIDTH
    mapSurfHeight = (len(game_state.map[0]) - 1) * TILEFLOORHEIGHT + TILEHEIGHT
    mapSurf = pygame.Surface((mapSurfWidth, mapSurfHeight + 100), pygame.SRCALPHA, 32)

    # Draw the tile sprites onto this surface.
    character_codes = {'m':2,'n':3,'r':0,'t':4,'g':1}
    for x in range(len(game_state.map)):
        for y in range(len(game_state.map[x])):
            map_entry = game_state.map[x][y]
            if map_entry in character_codes.keys():
                game_state.characters[character_codes[map_entry]].coordinates = (x,y)

            spaceRect = pygame.Rect((x * TILEWIDTH, y * TILEFLOORHEIGHT, TILEWIDTH, TILEHEIGHT))
            if game_state.map[x][y] in TILEMAPPING:
                baseTile = TILEMAPPING[game_state.map[x][y]]
            elif game_state.map[x][y] in OUTSIDEDECOMAPPING:
                baseTile = TILEMAPPING[' ']

            if baseTile.get_size()[1] > TILEHEIGHT:
                spaceRect.y -= baseTile.get_size()[1] - TILEHEIGHT -1
            # First draw the base ground/wall tile.
            mapSurf.blit(baseTile, spaceRect)

            if game_state.map[x][y] in OUTSIDEDECOMAPPING:
                # Draw any tree/rock decorations that are on this tile.
                mapSurf.blit(OUTSIDEDECOMAPPING[game_state.map[x][y]], spaceRect)

            # Last draw the player on the board.
            if (x, y) == game_state.player_pos:
                # Note: The value "currentImage" refers
                # to a key in "PLAYERIMAGES" which has the
                # specific player image we want to show.
                if game_state.currentImg == "down":
                    mapSurf.blit(PLAYERIMAGES[0], spaceRect)
                elif game_state.currentImg == "left":
                    mapSurf.blit(PLAYERIMAGES[1], spaceRect)
                elif game_state.currentImg == "right":
                    mapSurf.blit(PLAYERIMAGES[2], spaceRect)
                elif game_state.currentImg == "up":
                    mapSurf.blit(PLAYERIMAGES[3], spaceRect)
    return mapSurf

def renderStartScreen():
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

    # Position the title image.
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 200 # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    # Unfortunately, Pygame's font & text system only shows one line at
    # a time, so we can't use strings with \n newline characters in them.
    # So we will use a list with each line in it.
    instructionText = ['You are a crime solving dog, whose mission is to solve a crime ',
                       'on the train you are riding.',
                       'Arrow keys or WASD to move, E to talk with people through chatbox.']

    # Start with drawing a blank color to the entire window:
    #DISPLAYSURF.fill(BGCOLOR)

    # Draw the title image to the window:

    DISPLAYSURF.blit(pygame.image.load('assets/Sly Dog Title Screen.png'), (0,0))
    #DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10 # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)