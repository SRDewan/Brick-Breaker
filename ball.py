from config import *
from obj import *
from util import *

class Ball(Object):

    def __init__(self, pos):

        shape = listify("O")
        super().__init__(shape, [font['black'], bg['black']], pos)
        self.__thru = False

    def getThru(self):
        return self.__thru 

    def setThru(self):
        self.__thru = True
