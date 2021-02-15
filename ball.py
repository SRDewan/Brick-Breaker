from config import *
from obj import *
from util import *

class Ball(Object):

    def __init__(self, pos):

        shape = listify("o")
        super().__init__(shape, [font['black'], bg['black']], pos)
