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
        self.__start = time.time()
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
                    if(i == 0):
                        self.__powers.append(padExpand("%d%d%d"%(i, i, i), [2 + 2 * i, 2 + 4 * j]))

                    elif(i == 1):
                        self.__powers.append(padShrink("%d%d%d"%(i, i, i), [2 + 2 * i, 2 + 4 * j]))

                    elif(i == 2):
                        self.__powers.append(ballMul("%d%d%d"%(i, i, i), [2 + 2 * i, 2 + 4 * j]))

                    elif(i == 3):
                        self.__powers.append(ballFast("%d%d%d"%(i, i, i), [2 + 2 * i, 2 + 4 * j]))

                    elif(i == 4):
                        self.__powers.append(ballThru("%d%d%d"%(i, i, i), [2 + 2 * i, 2 + 4 * j]))
                        
                    elif(i == 5):
                        self.__powers.append(padGrab("%d%d%d"%(i, i, i), [2 + 2 * i, 2 + 4 * j]))

        self.__paddle = Paddle([rows - 2, (int)(cols / 2) - 2])
        self.__ball = Ball([self.__paddle.getPos()[0] - 1, self.__paddle.getPos()[1] + (int)(self.__paddle.getDim()[1] / 2)])

    def findPup(self, type):
        for x in self.__powers:
            if(x.getType() == type):
                return x

    def handle_input(self, txt):
        if(txt == 'a' or txt == 'A'):
            self.__paddle.keybrd(1, self.__ball)

        elif(txt == 'd' or txt == 'D'):
            self.__paddle.keybrd(0, self.__ball)

        elif(txt == ' '):
            self.__paddle.release(self.__ball)
            
            if(self.findPup(6).getTime() == -1):
                self.__paddle.setStick(False)

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
                    thru = self.__ball.getThru()
                    self.__bricks[i][j].collide(thru)
                    if(not self.__bricks[i][j].getActive()):
                        self.__score += points

                        for k in range(0, 6):
                            if(self.__powers[k].getPos() == self.__bricks[i][j].getPos()):
                                self.__powers[k].fall()

                    if(thru):
                        continue

                    if(ret == 1):
                        self.__ball.collide([-1 * self.__ball.getVel()[0], self.__ball.getVel()[1]])

                    else:
                        self.__ball.collide([self.__ball.getVel()[0], -1 * self.__ball.getVel()[1]])

        temp = []
        for i in range(0, len(self.__powers)):
            if(not self.__powers[i].getActive()):
                continue

            ret = self.collision(self.__powers[i], self.__paddle, False)

            if(ret):
                self.__powers[i].collide()
                temp.append(self.__powers[i])

        for i in range(0, len(temp)):
            temp[i].power(self.__paddle, self.__ball)

    def lifeLoss(self):
        self.__lives -= 1

        if(not self.__lives):
            self.__score -= (time.time() - self.__start) / 10
            print(font['red'] + bg['reset'] + "You Lost! Game Over! Your final score is %.3f" %(self.__score))
            quit()

        for l in range(0, 6):
            if(self.__powers[l].getTime() != -1):
                self.__powers[l].normal(self.__paddle, self.__ball)

        self.__ball = Ball([self.__paddle.getPos()[0] - 1, self.__paddle.getPos()[1] + (int)(self.__paddle.getDim()[1] / 2)])
        self.__paddle.setStick(True)

    def won(self):
        self.__score -= (time.time() - self.__start) / 10
        print(font['red'] + bg['reset'] + "Congratulations! You Won! Your final score is %.3f" %(self.__score))
        quit()

    def timeCheck(self, tempTime, pup):
        if(pup.getTime() != -1 and tempTime - pup.getTime() - period >= 1e-3):
            pup.normal(self.__paddle, self.__ball)

    def play(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        ctr = 0

        while True:

            if self.__input.kbhit():
                inp = self.__input.getch()
                self.handle_input(inp)
                
                self.__input.flush()

            self.handle_collisions()

            tempTime = time.time()
            for l in range(0, 6):
                self.timeCheck(tempTime, self.__powers[l])

                if(ctr % self.__powers[l].getFrame() == 0):
                    self.__powers[l].move()

            if(ctr % self.__ball.getFrame() == 0):
                self.__ball.move(1)

            if(not self.__ball.getActive()):
                self.lifeLoss()

            win = True 
            for i in range(0, len(self.__bricks)):
                for j in range(0, len(self.__bricks[i])):
                    if(self.__bricks[i][j].getType() != 1 and self.__bricks[i][j].getActive()):
                        win = False 
                        break

                if(not win):
                    break

            if(win):
                self.won()

            self.__screen.clear()

            print(font['white'] + bg['reset'] + "Lives: ", self.__lives)
            print(font['white'] + bg['reset'] + "Score: ", self.__score)
            print(font['white'] + bg['reset'] + "Time: %.2f" %(time.time() - self.__start))

            for i in range(0, 6):
                    self.__screen.populate(self.__powers[i])

            for i in range(0, 6):
                for j in range(0, self.__brickCtr):
                    self.__screen.populate(self.__bricks[i][j])

            self.__screen.populate(self.__paddle)
            self.__screen.populate(self.__ball)

            self.__screen.disp()

            time.sleep(1 / fps)
            ctr += 1
            if(ctr == 7):
                ctr = 1
