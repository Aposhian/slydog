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

pygame.display.set_caption('Star Pusher')
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

# A global dict value that will contain all the Pygame
# Surface objects returned by pygame.image.load().
IMAGESDICT = {'uncovered goal': pygame.image.load('assets/RedSelector.png'),
              'covered goal': pygame.image.load('assets/Selector.png'),
              'star': pygame.image.load('assets/Star.png'),
              'corner': pygame.image.load('assets/Wall_Block_Tall.png'),
              'wall': pygame.image.load('assets/Wood_Block_Tall.png'),
              'inside floor': pygame.image.load('assets/Plain_Block.png'),
              'outside floor': pygame.image.load('assets/Grass_Block.png'),
              'title': pygame.image.load('assets/star_title.png'),
              'solved': pygame.image.load('assets/star_solved.png'),
              'princess': pygame.image.load('assets/princess.png'),
              'boy': pygame.image.load('assets/boy.png'),
              'catgirl': pygame.image.load('assets/catgirl.png'),
              'horngirl': pygame.image.load('assets/horngirl.png'),
              'pinkgirl': pygame.image.load('assets/pinkgirl.png'),
              'rock': pygame.image.load('assets/Rock.png'),
              'short tree': pygame.image.load('assets/Tree_Short.png'),
              'tall tree': pygame.image.load('assets/Tree_Tall.png'),
              'ugly tree': pygame.image.load('assets/Tree_Ugly.png')}


def startScreen():
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""

    # Position the title image.
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50 # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    # Unfortunately, Pygame's font & text system only shows one line at
    # a time, so we can't use strings with \n newline characters in them.
    # So we will use a list with each line in it.
    instructionText = ['Push the stars over the marks.',
                       'Arrow keys to move, WASD for camera control, P to change character.',
                       'Backspace to reset level, Esc to quit.',
                       'N for next level, B to go back a level.']

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BGCOLOR)

    # Draw the title image to the window:
    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)

    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10 # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

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