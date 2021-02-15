import os
import colorama as col 

rows, cols= os.popen('stty size', 'r').read().split()
rows = int(rows) - 5
cols = int(cols) - 10

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
            ["white", "white", "white", "white"],
        ]

padLen = 5
change = 2
delay = 0.2
jump = 1
points = 5
period = 15
