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
        self.__brickCtr = (int)((cols - 4) / 3)
        self.__bricks = []
        self.__powers = []
        self.__explode = []
        self.__lifeRec = True
        # np.empty((6, self.__brickCtr))

        for i in range(0, 6):
            self.__bricks.append([])
            for j in range(0, self.__brickCtr):
                if(i == j):
                    self.__bricks[i].append(Brick(1, [2 + i, 2 + 3 * j]))
                # placing unbreakable bricks

                elif(i == j - 1):
                    self.__bricks[i].append(Brick(2, [2 + i, 2 + 3 * j]))
                # placing exploding bricks

                elif(self.__brickCtr - 2 - j == i):
                    self.__bricks[i].append(Brick(2, [2 + i, 2 + 3 * j]))
                # placing exploding bricks

                else:
                    self.__bricks[i].append(Brick(0, [2 + i, 2 + 3 * j]))
                # placing normal bricks
        
                # placing powerups 
                if(self.__brickCtr - 1 - j == i):
                    if(i == 0):
                        self.__powers.append(padExpand([2 + i, 2 + 3 * j]))

                    elif(i == 1):
                        self.__powers.append(padShrink([2 + i, 2 + 3 * j]))

                    elif(i == 2):
                        self.__powers.append(ballMul([2 + i, 2 + 3 * j]))

                    elif(i == 3):
                        self.__powers.append(ballFast([2 + i, 2 + 3 * j]))

                    elif(i == 4):
                        self.__powers.append(ballThru([2 + i, 2 + 3 * j]))
                        
                    elif(i == 5):
                        self.__powers.append(padGrab([2 + i, 2 + 3 * j]))

        self.__paddle = Paddle([rows - 2, (int)(cols / 2) - 2])
        self.__balls = [Ball([self.__paddle.getPos()[0] - 1, self.__paddle.getPos()[1] + (int)(self.__paddle.getDim()[1] / 2)])]
        self.__ballCtr = 1

    def findPup(self, type):
        for x in self.__powers:
            if(x.getType() == type):
                return x

    def handle_input(self, txt):
        if(txt == 'a' or txt == 'A'):
            self.__paddle.keybrd(1, self.__balls)

        elif(txt == 'd' or txt == 'D'):
            self.__paddle.keybrd(0, self.__balls)

        elif(txt == ' '):
            self.__paddle.release(self.__balls)
            self.__lifeRec = False
            
            if(self.findPup(6).getTime() == -1):
                self.__paddle.setStick(False)

    def verticalCol(self, pos1, pos2, dim1, dim2): 
        if(set(range(pos1[0], pos1[0] + dim1[0])) & set(range(pos2[0], pos2[0] + dim2[0]))):
            return False 

        return True 

    def findBrickByPos(self, pos):
        for m in range(0, len(self.__bricks)):
            for n in range(0, len(self.__bricks[m])):
                if(self.__bricks[m][n].getPos() == pos):
                    if(not self.__bricks[m][n].getActive()):
                        return None
                    return self.__bricks[m][n]

    def findBricks(self, brick):
        posit = brick.getPos()
        dim = brick.getDim()

        if(brick.getType() == 2):
            for a in range(posit[0] - 1 * dim[0], posit[0] + 2 * dim[0], dim[0]):
                for b in range(posit[1] - 1 * dim[1], posit[1] + 2 * dim[1], dim[1]):
                    if(a == posit[0] and b == posit[1]):
                        continue

                    ret = self.findBrickByPos([a, b])
                    if(ret != None):
                        self.__explode.append(ret)

    def explosion(self):
        length = len(self.__explode)
        for z in range(0, length):
            self.findBricks(self.__explode[z])
            self.__explode[z].collide(True)
            self.__score += points

            for k in range(0, 6):
                if(self.__powers[k].getPos() == self.__explode[z].getPos()):
                    self.__powers[k].fall()

        for z in range(0, length):
            del self.__explode[0]

    def colChck(self, pos1, dim1, pos2, dim2):
        if(set(range(pos1[0], pos1[0] + dim1[0])) & set(range(pos2[0], pos2[0] + dim2[0]))):
            if(set(range(pos1[1], pos1[1] + dim1[1])) & set(range(pos2[1], pos2[1] + dim2[1]))):
                return True

        return False

    def collision(self, obj, flags):
        # obj always moving obj such as ball or powerup
        # flags[0] --> paddle interaction type, flags[1] --> brick interaction type

        p1 = np.array(obj.getPos()[:])
        v1 = np.array(obj.getVel()[:])
        dim1 = obj.getDim()[:]

        sign = [1, 1]

        if(v1[0]):
            sign[0] = (int)(v1[0] / abs(v1[0]))

        if(v1[1]):
            sign[1] = (int)(v1[1] / abs(v1[1]))

        for r in range(0, abs(v1[0]) + 1):
            for c in range(0, abs(v1[1]) + 1):
                cr = p1[0] + r * sign[0]
                cc = p1[1] + c * sign[1]
                pos1 = [cr, cc]

                if(cr == p1[0] and cc == p1[1]):
                    continue

                if(flags[0] == 1):
                    pos2 = np.array(self.__paddle.getPos()) + np.array(self.__paddle.getVel())
                    dim2 = self.__paddle.getDim()

                    if(self.colChck(pos1, dim1, pos2, dim2)):
                        if(self.verticalCol(obj.getPos(), self.__paddle.getPos(), dim1, dim2)):
                            self.__paddle.collide(obj)
                            obj.collide([-1 * obj.getVel()[0], obj.getVel()[1]])
                            return

                elif(flags[0] == 2):

                    pos2 = np.array(self.__paddle.getPos()) + np.array(self.__paddle.getVel())
                    dim2 = self.__paddle.getDim()

                    if(self.colChck(pos1, dim1, pos2, dim2)):
                        if(self.verticalCol(obj.getPos(), self.__paddle.getPos(), dim1, dim2)):
                            return 1

                if(flags[1]):

                    for i in range(0, len(self.__bricks)):
                        for j in range(0, len(self.__bricks[i])):
                            if(not self.__bricks[i][j].getActive()):
                                continue

                            pos2 = np.array(self.__bricks[i][j].getPos()) + np.array(self.__bricks[i][j].getVel())
                            dim2 = self.__bricks[i][j].getDim()

                            if(self.colChck(pos1, dim1, pos2, dim2)):

                                thru = obj.getThru()
                                self.findBricks(self.__bricks[i][j])
                                self.__bricks[i][j].collide(thru)
                                if(not self.__bricks[i][j].getActive()):
                                    self.__score += points

                                    for k in range(0, 6):
                                        if(self.__powers[k].getPos() == self.__bricks[i][j].getPos()):
                                            self.__powers[k].fall()

                                if(thru):
                                    continue

                                if(self.verticalCol(obj.getPos(), self.__bricks[i][j].getPos(), dim1, dim2)):
                                    obj.collide([-1 * obj.getVel()[0], obj.getVel()[1]])
                                    return

                                else:
                                    obj.collide([obj.getVel()[0], -1 * obj.getVel()[1]])
                                    return

        return 0 

    def activation(self):
        for i in range(0, len(self.__powers)):
            if(self.__powers[i].getTime() != -1):
                if(self.__powers[i].getType() == 3): 
                    continue

                self.__powers[i].power(self.__paddle, self.__balls)

    def reset(self):
        self.__paddle.setShape(listify(" " * padLen))
        if(not self.__lifeRec):
            self.__paddle.setStick(False)

        for b in range(0, len(self.__balls)):
            self.__balls[b].setFrame(ballFps)
            self.__balls[b].setThru(False)


    def padPowCol(self):
        temp = []
        for i in range(0, len(self.__powers)):
            if(not self.__powers[i].getActive()):
                continue

            ret = self.collision(self.__powers[i], [2, 0])

            if(ret):
                self.__powers[i].collide()
                temp.append(self.__powers[i])

        for i in range(0, len(temp)):
            temp[i].setTime(time.time())

            ctype = temp[i].getType()

            if(ctype == 1 or ctype == 2 or ctype == 3):
                self.__paddle.release(self.__balls)

            if(ctype == 3):
                self.__ballCtr *= 2
                temp[i].power(self.__paddle, self.__balls)

    def lifeLoss(self):

        self.__lives -= 1

        if(not self.__lives):
            self.__score -= (time.time() - self.__start) / 10
            print(font['red'] + bg['reset'] + "You Lost! Game Over! Your final score is %.3f" %(self.__score))
            quit()

        for l in range(0, 6):
            if(self.__powers[l].getTime() != -1):

                self.__powers[l].setTime(-1)

        self.__balls.append(Ball([self.__paddle.getPos()[0] - 1, self.__paddle.getPos()[1] + (int)(self.__paddle.getDim()[1] / 2)]))
        self.__lifeRec = True
        self.__paddle.setStick(True)

    def won(self):
        self.__score -= (time.time() - self.__start) / 10
        print(font['red'] + bg['reset'] + "Congratulations! You Won! Your final score is %.3f" %(self.__score))
        quit()

    def timeCheck(self, tempTime, pup):
        if(pup.getTime() != -1 and tempTime - pup.getTime() - period >= 1e-3):
            pup.setTime(-1)
            ctype = pup.getType()

            if(ctype == 3):
                self.__ballCtr = (int)(np.ceil(self.__ballCtr / 2))
                pup.normal(self.__paddle, self.__balls, self.__ballCtr)

            if(ctype == 1 or ctype == 2 or ctype == 3):
                self.__paddle.release(self.__balls)

            elif(not self.__lifeRec and ctype == 6):
                self.__paddle.release(self.__balls)

    def play(self):

        os.system('cls' if os.name == 'nt' else 'clear')
        ctr = 0

        while True:

            self.activation()

            if self.__input.kbhit():
                inp = self.__input.getch()
                self.handle_input(inp)
                self.__input.flush()

            if(len(self.__explode)):
                self.explosion()

            self.padPowCol()

            for ball in self.__balls:
                self.collision(ball, [1, 1])

            tempTime = time.time()
            for l in range(0, 6):
                self.timeCheck(tempTime, self.__powers[l])

                if(ctr % self.__powers[l].getFrame() == 0):
                    self.__powers[l].move()

            tmpDel = []
            for b in range(0, len(self.__balls)):
                if(ctr % self.__balls[b].getFrame() == 0):
                    self.__balls[b].move(1)
                if(not self.__balls[b].getActive()):
                    tmpDel.append(self.__balls[b])

            for ball in tmpDel:
                self.__balls.remove(ball)

            if(not self.__balls):
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

            for b in range(0, len(self.__balls)):
                self.__screen.populate(self.__balls[b])

            self.__screen.disp()

            time.sleep(1 / fps)
            ctr += 1
            if(ctr == 11):
                ctr = 1

            self.reset()
