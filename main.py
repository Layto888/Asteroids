"""
Made with with python and pygame
to test and improve the laylib framwork rapid game prototyping.
Asteroids 2D.

Author: Amardjia Amine
Date: 16/06/2018
Github: ---
"""

from laylib.environment import *
from engine import *
from settings import *


def main():
    # init global environment
    game_ship = Environment(

        WIDTH,     # width
        HEIGHT,   # height
        False,   # full screen
        'Asteroids'  # window title
    )
    # load resources, set the game
    game_ship.load_complete(Engine(), 'data', 'resources.dat')
    # play
    game_ship.gInstance.main_loop()
    # quit the game
    game_ship.destroy()


if __name__ == "__main__":
    main()
