from enum import Enum, auto


class GameState(Enum):
    QUIT = auto()
    PLAY = auto()
    PAUSE = auto()

class Game:
    def __init__(self):
        self.state = GameState.PLAY

    def run(self):
        pass

    def quit(self):
        pass

    def init(self):
        pass

    def update(self):
        pass

    def paint(self):
        pass



