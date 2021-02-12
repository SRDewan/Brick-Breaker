from config import *
from obj import *
from util import *

class Ball(Object):

    def __init__(self, pos):

        self.__shape = listify("o")
        super().__init__(self.__shape, [font['black'], bg['black']], pos)
