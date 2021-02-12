"""Defining input class."""
import sys
import termios
import tty
import signal
import os 
import time
import numpy as np

from config import *
from screen import *
from brick import *
from input import *

class Game:

    def __init__(self):
        self.__screen = Screen()
        self.__brick = Brick(font['white'], [1, 1])
        self.__lives = 3
        
    def play(self):

        os.system('cls' if os.name == 'nt' else 'clear')

        while True:

            self.__screen.clear()
            self.__screen.populate(self.__brick)
            self.__screen.disp()

            inp = take_inp()
            if(inp == 'f'):
                self.__screen[0][0] = 'F'
            time.sleep(delay)
