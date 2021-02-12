from config import *
from obj import *
from util import *

class Brick(Object):

    def __init__(self, type, pos):

        self.__shape = listify("   ")
        self.__type = type  ## 0 => Normal, 1 => Unbreakable, 2 => Exploding
        self.__status = 3   ## Decreasing life/strength of brick from 3(max) to 0(disappear)
        super().__init__(self.__shape, [font['black'], bg[brickCol[self.__type][self.__status]]], pos)
