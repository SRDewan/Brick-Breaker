import colorama as col

from game import *

if __name__ == "__main__":

    col.init(autoreset = True)
    game = Game()
    game.play()
