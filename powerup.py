from config import *
from obj import *
from util import *

class Powerup(Object):

    def __init__(self, shape, pos):

        shape = listify(shape)
        super().__init__(shape, [font['blue'], bg['black']], pos)

    def fall(self):
        self.setVel([jump, 0])
