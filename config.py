import os
import colorama as col 

rows, cols= os.popen('stty size', 'r').read().split()
rows = int(rows) - 10
cols = int(cols) - 10

lvlnum = 3

font = {
        "red": col.Fore.RED,
        "blue": col.Fore.BLUE,
        "green": col.Fore.GREEN,
        "yellow": col.Fore.YELLOW,
        "black": col.Fore.BLACK,
        "purple": col.Fore.MAGENTA,
        "white": col.Fore.WHITE,
        "reset": col.Fore.RESET,
        }

for i in font:
    font[i] += col.Style.BRIGHT

bg = {
        "red": col.Back.RED,
        "blue": col.Back.BLUE,
        "green": col.Back.GREEN,
        "yellow": col.Back.YELLOW,
        "black": col.Back.BLACK,
        "purple": col.Back.MAGENTA,
        "white": col.Back.WHITE,
        "reset": col.Back.RESET,
        }

brickCol = [["black", "red", "yellow", "green"],
            ["purple", "purple", "purple", "purple"],
            ["blue", "blue", "blue", "blue"],
        ]

padLen = 5
change = 2
gravity = 1

fps = 150
timeLim = 100
ballFps = 5
brickFps = 5
powFps = 10
gravFps = 20
jump = 1

points = 5
period = 15
