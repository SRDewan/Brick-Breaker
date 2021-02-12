import colorama as col

from game import *

if __name__ == "__main__":

    col.init(autoreset = False)
    game = Game()
    game.play()
