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
from paddle import *
from ball import *
from input import *

class Game:

    def __init__(self):
        self.__input = KBHit()
        self.__screen = Screen()
        self.__lives = 3
        self.__score = 0
        self.__brickCtr = (int)((cols - 4) / 4)
        self.__bricks = []
        # np.empty((6, self.__brickCtr))

        for i in range(0, 6):
            self.__bricks.append([])
            for j in range(0, self.__brickCtr):
                self.__bricks[i].append(Brick(0, [2 + 2 * i, 2 + 4 * j]))
        
        self.__paddle = Paddle([rows - 2, (int)(cols / 2) - 2])
        self.__ball = Ball([rows - 3, (int)(cols / 2)])

    def handle_input(self, txt):
        if(txt == 'a' or txt == 'A'):
            self.__paddle.keybrd(1, self.__ball)

        elif(txt == 'd' or txt == 'D'):
            self.__paddle.keybrd(0, self.__ball)

        elif(txt == ' '):
            self.__paddle.release(self.__ball)

    def collision(self, obj1, obj2):

        if(pos1[0] in range(pos2[0], pos2[0] + dim2[0]) and pos1[0] in range(pos2[1], pos2[1] + dim2[1])):
            pass

    def handle_collisions(self):
        collision(self.__ball, self.__paddle)

        for i in range(0, len(self.__bricks)):
            for j in range(0, len(self.__bricks[i])):
                collision(self.__ball, self.__bricks[i][j])

    def play(self):

        os.system('cls' if os.name == 'nt' else 'clear')

        while True:

            if self.__input.kbhit():
                inp = self.__input.getch()
                self.handle_input(inp)
                
                self.__input.flush()

            self.__ball.move(1)
            self.__screen.clear()

            print("Lives: ", self.__lives)
            print("Score: ", self.__score)

            for i in range(0, 6):
                for j in range(0, self.__brickCtr):
                    self.__screen.populate(self.__bricks[i][j])

            self.__screen.populate(self.__paddle)
            self.__screen.populate(self.__ball)

            self.__screen.disp()

            time.sleep(delay)
