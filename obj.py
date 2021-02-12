import numpy as np

from config import *
from util import *

class Object:

    def __init__(self, shape, color, pos, vel=[0, 0]):
       self.__shape = shape 
       self.__color = color
       self.__pos = pos 
       self.__vel = vel 

    def draw(self, grid):
        self.__obj = self.__shape
        [xlen, ylen] = getShape(self.__obj)

        for i in range(0, xlen):
            for j in range(0, ylen):
                self.__obj[i][j] += self.__color 

        grid[self.__pos[0] : self.__pos[0] + xlen, self.__pos[1] : self.__pos[1] + ylen] = self.__obj
