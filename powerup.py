import time

from config import *
from obj import *
from util import *

class Powerup(Object):

    def __init__(self, shape, pos, type):

        shape = listify(shape)
        self.__type = type
        self.__time = time.time()
        super().__init__(shape, [font['blue'], bg['black']], pos)

    def getType(self):
        return self.__type

    def fall(self):
        self.setVel([jump, 0])

    def power(self, paddle, ball):
        print("lol")

    def collide(self):
        self.destroy()

class padExpand(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__(shape, pos, 1)

    def power(self, paddle, ball):
        paddle.setShape("       ")

class padShrink(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__(shape, pos, 2)

    def power(self, paddle, ball):
        paddle.setShape("   ")

class ballMul(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__(shape, pos, 3)

class ballFast(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__(shape, pos, 4)

class ballThru(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__(shape, pos, 5)

    def power(self, paddle, ball):
        ball.setThru()

class padGrab(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__(shape, pos, 6)

    def power(self, paddle, ball):
        paddle.setStick(True)
