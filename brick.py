from config import *
from obj import *
from util import *

class Brick(Object):

    def __init__(self, type, pos):

        shape = listify("[ ]")
        self.__type = type  ## 0 => Normal, 1 => Unbreakable, 2 => Exploding
        self.__status = 3   ## Decreasing life/strength of brick from 3(max) to 0(disappear)
        super().__init__(shape, [font['black'], bg[brickCol[self.__type][self.__status]]], pos)

    def hit(self, newStat):
        self.__status = newStat
        self.setColor([self.getColor()[0], bg[brickCol[self.__type][self.__status]]])

        if(not self.__status):
            self.destroy()

    def getType(self):
        return self.__type

    def collide(self, thru=False):
        if(not self.__type and not thru):
            self.hit(self.__status - 1)

        elif(self.__type == 2 or thru):
            self.hit(0)
