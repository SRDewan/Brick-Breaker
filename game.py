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
from powerup import *
from input import *

class Game:

    def __init__(self):
        self.__input = KBHit()
        self.__screen = Screen()
        self.__lives = 3
        self.__score = 0
        self.__brickCtr = (int)((cols - 4) / 4)
        self.__bricks = []
        self.__powers = []
        # np.empty((6, self.__brickCtr))

        for i in range(0, 6):
            self.__bricks.append([])
            for j in range(0, self.__brickCtr):
                if(i == j):
                    self.__bricks[i].append(Brick(1, [2 + 2 * i, 2 + 4 * j]))

                else:
                    self.__bricks[i].append(Brick(0, [2 + 2 * i, 2 + 4 * j]))
        
                if(self.__brickCtr - 1 - j == i):
                    self.__powers.append(Powerup("%d%d%d"%(i, i, i), [2 + 2 * i, 2 + 4 * j]))

        self.__paddle = Paddle([rows - 2, (int)(cols / 2) - 2])
        self.__ball = Ball([self.__paddle.getPos()[0] - 1, self.__paddle.getPos()[1] + (int)(self.__paddle.getDim()[1] / 2)])

    def handle_input(self, txt):
        if(txt == 'a' or txt == 'A'):
            self.__paddle.keybrd(1, self.__ball)

        elif(txt == 'd' or txt == 'D'):
            self.__paddle.keybrd(0, self.__ball)

        elif(txt == ' '):
            self.__paddle.release(self.__ball)

    def verticalCol(self, pos1, pos2, dim1, dim2): 
        if(set(range(pos1[0], pos1[0] + dim1[0])) & set(range(pos2[0], pos2[0] + dim2[0]))):
            return False 

        return True 

    def collision(self, obj1, obj2, horizontal=True, thru=False):
        # obj1 always moving obj such as ball

        pos1 = np.array(obj1.getPos()[:]) + np.array(obj1.getVel()[:])
        dim1 = obj1.getDim()[:]

        pos2 = np.array(obj2.getPos()[:]) + np.array(obj2.getVel()[:])
        dim2 = obj2.getDim()[:]

        if(set(range(pos1[0], pos1[0] + dim1[0])) & set(range(pos2[0], pos2[0] + dim2[0]))):
            if(set(range(pos1[1], pos1[1] + dim1[1])) & set(range(pos2[1], pos2[1] + dim2[1]))):
                if(self.verticalCol(obj1.getPos(), obj2.getPos(), dim1, dim2)):
                    return 1 

                elif(horizontal):
                    return 2 

        return 0 

    def handle_collisions(self):
        ret = self.collision(self.__ball, self.__paddle, False)

        if(ret):
            self.__paddle.collide(self.__ball)
            self.__ball.collide([-1 * self.__ball.getVel()[0], self.__ball.getVel()[1]])

        for i in range(0, len(self.__bricks)):
            for j in range(0, len(self.__bricks[i])):
                if(not self.__bricks[i][j].getActive()):
                    continue

                ret = self.collision(self.__ball, self.__bricks[i][j])

                if(ret):
                    self.__bricks[i][j].collide()
                    if(not self.__bricks[i][j].getActive()):
                        self.__score += points

                        for k in range(0, 6):
                            if(self.__powers[k].getPos() == self.__bricks[i][j].getPos()):
                                self.__powers[k].fall()

                    if(ret == 1):
                        self.__ball.collide([-1 * self.__ball.getVel()[0], self.__ball.getVel()[1]])

                    else:
                        self.__ball.collide([self.__ball.getVel()[0], -1 * self.__ball.getVel()[1]])

    def lifeLoss(self):
        self.__lives -= 1

        if(not self.__lives):
            print(font['red'] + bg['reset'] + "Game Over!")
            quit()

        self.__ball = Ball([self.__paddle.getPos()[0] - 1, self.__paddle.getPos()[1] + (int)(self.__paddle.getDim()[1] / 2)])

    def play(self):

        os.system('cls' if os.name == 'nt' else 'clear')

        while True:

            if self.__input.kbhit():
                inp = self.__input.getch()
                self.handle_input(inp)
                
                self.__input.flush()

            self.handle_collisions()

            for l in range(0, 6):
                self.__powers[l].move()

            self.__ball.move(1)

            if(not self.__ball.getActive()):
                self.lifeLoss()

            self.__screen.clear()

            print(font['white'] + bg['reset'] + "Lives: ", self.__lives)
            print(font['white'] + bg['reset'] + "Score: ", self.__score)

            for i in range(0, 6):
                    self.__screen.populate(self.__powers[i])

            for i in range(0, 6):
                for j in range(0, self.__brickCtr):
                    self.__screen.populate(self.__bricks[i][j])

            self.__screen.populate(self.__paddle)
            self.__screen.populate(self.__ball)

            self.__screen.disp()

            time.sleep(delay)
