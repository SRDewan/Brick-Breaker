from config import *
from obj import *
from util import *

class Ball(Object):

    def __init__(self, pos):

        shape = listify("O")
        super().__init__(shape, [font['black'], bg['black']], pos)
        self.setFrame(5)
        self.__thru = False
        self.__oldyVel = 0

    def getThru(self):
        return self.__thru 

    def setThru(self, stat):
        self.__thru = stat 

    def getOldVel(self):
        return self.__oldyVel

    def setOldVel(self, new):
        self.__oldyVel = new 
