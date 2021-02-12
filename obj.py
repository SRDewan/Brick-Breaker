import numpy as np

from config import *
from util import *

class Object:

    def __init__(self, shape, color, pos, active=True, vel=[0, 0]):
       self.__shape = shape 
       self.__color = color  # color[0] => fgcolor, color[1] => bgcolor
       self.__pos = pos      # pos = [x, y] of top left corner pixel/character of obj
       self.__vel = vel      # vel = [xvel, yvel]
       self.__active = active 

    def draw(self, grid):
        [xlen, ylen] = getShape(self.__shape)

        if(not self.__active):
            return

        for i in range(0, xlen):
            for j in range(0, ylen):
                grid[self.__pos[0] + i][self.__pos[1] + j] = self.__color[1] + self.__shape[i][j]

    def destroy(self):
        self.__active = False
