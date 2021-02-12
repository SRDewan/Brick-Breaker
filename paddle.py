from config import *
from obj import *
from util import *

class Paddle(Object):

    def __init__(self, pos):

        self.__shape = listify("     ")
        super().__init__(self.__shape, [font['black'], bg['white']], pos)
