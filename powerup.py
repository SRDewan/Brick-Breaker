import time

from config import *
from obj import *
from util import *

class Powerup(Object):

    def __init__(self, shape, pos, type):

        shape = listify(shape)
        self.__type = type
        self.__time = -1
        super().__init__(shape, [font['blue'], bg['black']], pos)

    def getType(self):
        return self.__type

    def fall(self):
        self.setVel([jump, 0])

    def power(self, paddle, ball):
        self.setTime(time.time())

    def normal(self, paddle, ball):
        self.setTime(-1)

    def collide(self):
        self.destroy()

    def getTime(self):
        return self.__time

    def setTime(self, ttime):
        self.__time = ttime

class padExpand(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__("<=>", pos, 1)

    def power(self, paddle, ball):
        paddle.setShape(listify(" " * (paddle.getDim()[1] + change)))
        self.setTime(time.time())

    def normal(self, paddle, ball):
        paddle.setShape(listify(" " * (paddle.getDim()[1] - change)))
        self.setTime(-1)

class padShrink(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__(">=<", pos, 2)

    def power(self, paddle, ball):
        paddle.setShape(listify(" " * (paddle.getDim()[1] - change)))
        self.setTime(time.time())

    def normal(self, paddle, ball):
        paddle.setShape(listify(" " * (paddle.getDim()[1] + change)))
        self.setTime(-1)

class ballMul(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__("2xO", pos, 3)

class ballFast(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__("...", pos, 4)

class ballThru(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__("XoX", pos, 5)

    def power(self, paddle, ball):
        ball.setThru(True)
        self.setTime(time.time())

    def normal(self, paddle, ball):
        ball.setThru(False)
        self.setTime(-1)

class padGrab(Powerup):
    
    def __init__(self, shape, pos):
        super().__init__("|_|", pos, 6)

    def power(self, paddle, ball):
        paddle.setStick(True)
        self.setTime(time.time())

    def normal(self, paddle, ball):
        paddle.release(ball)
        paddle.setStick(False)
        self.setTime(-1)

