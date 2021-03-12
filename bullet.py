from config import *
from obj import *
from util import *

class Bullet(Object):

    def __init__(self, pos):

        shape = listify("|")
        super().__init__(shape, [font['black'], bg['black']], pos, True, [-1, 0])
        self.setFrame(bullFps)
