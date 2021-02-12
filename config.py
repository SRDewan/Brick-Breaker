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

delay = 0.5
