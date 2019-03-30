

class GameState:

    def __init__(self):
        self.map = [
            ['#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
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
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
            ['#', ' ', ' ', ' ', ' ', ' ', ' ', '#'],
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

    @property
    def outOfBBX(self):
        return abs(self.distance_to_bbX) > self.BOUNDING_BOX_RADIUS

    @property
    def outOfBBY(self):
        return abs(self.distance_to_bbY) > self.BOUNDING_BOX_RADIUS


