import time

# from config import *
import config
from obj import *
from util import *

class Powerup(Object):

    def __init__(self, shape, pos, type):

        shape = listify(shape)
        self.__type = type
        self.__time = -1
        super().__init__(shape, [font['blue'], bg['black']], pos)
        self.setFrame(powFps)

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
    
    def __init__(self, pos):
        super().__init__("<=>", pos, 1)

    def power(self, paddle, ball):
        if(cols - paddle.getPos()[1] - paddle.getDim()[1] >= change):
            paddle.setShape(listify(" " * (paddle.getDim()[1] + change)))

class padShrink(Powerup):
    
    def __init__(self, pos):
        super().__init__(">=<", pos, 2)

    def power(self, paddle, ball):
        if(paddle.getDim()[1] > change):
            paddle.setShape(listify(" " * (paddle.getDim()[1] - change)))

class ballMul(Powerup):
    
    def __init__(self, pos):
        super().__init__("2xO", pos, 3)

    def power(self, obj1, ball):
        tempo = obj1.getVel()[:]

        if(not tempo[1]):
            tempo[1] += 1
        else:
            tempo[1] *= -1

        ball.activate(obj1.getPos()[:])
        ball.setVel(tempo)

        self.setTime(time.time())

    def normal(self, obj1, ball):
        ball.setVel([0, 0])
        ball.destroy()
        self.setTime(-1)

class ballFast(Powerup):
    
    def __init__(self, pos):
        super().__init__(">>>", pos, 4)

    def power(self, obj1, ball):
        if(obj1.getFrame() > 1):
            obj1.setFrame(ball.getFrame() - 1)
            ball.setFrame(ball.getFrame() - 1)

class ballThru(Powerup):
    
    def __init__(self, pos):
        super().__init__("XXX", pos, 5)

    def power(self, obj1, ball):
        obj1.setThru(True)
        ball.setThru(True)

class padGrab(Powerup):
    
    def __init__(self, pos):
        super().__init__("|_|", pos, 6)

    def power(self, paddle, ball):
        paddle.setStick(True)

