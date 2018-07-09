"""
A simple 2D game.
Author: Amardjia Amine
"""

from laylib.environment import *
import pygame as pg


def main():
    # init global environment
    test = Environment(

        800,  # width
        600,   # height
        False,  # full screen
        'New 2D project'  # window title
    )
    """
    test.load_complete(ParticlesEngine(pg.mouse.get_pos()))
    # go play
    test.gInstance.main_loop()
    # quit
    # test.destroy()
    """


if __name__ == "__main__":
    main()
