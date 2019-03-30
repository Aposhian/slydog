

class GameState:

    def __init__(self):
        pass

    FPS = 30 # frames per second to update the screen
    CAM_MOVE_SPEED = 5 # how many pixels per frame the camera moves

    # The percentage of outdoor tiles that have additional
    # decoration on them, such as a tree or rock.
    OUTSIDE_DECORATION_PCT = 20

    BRIGHTBLUE = (  0, 170, 255)
    WHITE      = (255, 255, 255)
    BGCOLOR = BRIGHTBLUE
    TEXTCOLOR = WHITE

    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'
