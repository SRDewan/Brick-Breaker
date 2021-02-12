from obj import *
from util import *

class Brick(Object):

    def __init__(self, color, pos):

        self.__shape = listify(" ___ \n|___|")
        super().__init__(self.__shape, color, pos)
        
