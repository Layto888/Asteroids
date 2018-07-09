import pygame as pg
import sys
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')


class Environment(object):
    """
    Environment : Contain the whole game,window,
    resources...etc.
    creat an instance of the game engines
    """

    def __init__(self,
                 screenWidth,
                 screenHeight,
                 fullscreen,
                 windowTitle):

        # full screen & optimization
        flag = 0
        # init pygame
        pg.init()
        if not pg.display.get_init():
            logging.info('unable to init display pygame')
            self.destroy()
        else:
            pg.display.set_caption(windowTitle)
            if fullscreen:
                flag |= pg.FULLSCREEN
            flag |= pg.HWSURFACE
            flag |= pg.DOUBLEBUF
            pg.display.set_mode((screenWidth, screenHeight), flag)
            # display video infos
            logging.info('Display done: driver -> {}'
                         .format(pg.display.get_driver()))
            logging.info(pg.display.Info())
            # temporarily set which modifier keys are pressed to 0.
            pg.key.set_mods(0)
            pg.key.set_repeat(10, 10)
            # set the mixer sounds:
            pg.mixer.init()
            if pg.mixer.get_init():
                logging.info('initialize the mixer done...')
            else:
                logging.info('Unable to initialize the mixer')
                pg.mixer.quit()
            # set the font:
            pg.font.init()
            if not pg.font.get_init():
                logging.info('Unable to initialize the font')
                pg.font.quit()
            else:
                logging.info('initialize the font done: default type -> {}'
                             .format(pg.font.get_default_font()))

    def load_complete(
            self,
            instance,
            dataFolder=None,
            persistenceLayer=None,
            fileLevels=None):
        # get instance of the game:
        self.gInstance = instance
        """ load game resources & get infos from persistence layer.
        the instance (engine of the game must contain:
        load_game(), load_levels(), and destroy() functions)
        """
        if dataFolder and persistenceLayer:
            self.gInstance.load_game(dataFolder, persistenceLayer)
        if dataFolder and fileLevels:
            self.gInstance.load_levels(dataFolder, fileLevels)

    """
    Description:
    the instance of the game MUST contain functions:
    "main_loop()"
    and the optionals names if exists of:
    "destroy_game()"
    "load_game()"
    "load_levels()"
    """

    def destroy(self):
        if self.gInstance:
            # free all game resources
            self.gInstance.destroy_game()
        pg.mixer.quit()
        pg.font.quit()
        pg.quit()
        sys.exit('Exit')
