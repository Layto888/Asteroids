import os
import json
import pygame as pg


SOUND_TITLE = 0
SOUND_VOLUME = 1
FONT_NAME = 0
FONT_SIZE = 1


class Resources(object):
    """
    Load all resources files, with json parsing method.
    Environment framework for games : Resources manager.
    Author: A.Amine
    Version: 0.2
    Last revision : 08/06/2018
    """

    def __init__(self, mainPath=''):
        self.mainPath = mainPath
        self.sound_ref = 0
        self.music_ref = 0
        self.font_ref = 0
        self.image_ref = 0
        self.persiLayer = ''
        self.screen = pg.display.get_surface()

    def load_sound(self, name, volume=1.0):
        name = os.path.join(self.mainPath, name)
        sound = pg.mixer.Sound(name)
        sound.set_volume(volume)
        assert sound
        self.sound_ref += 1
        return sound

    def load_snd_list(self, soundList):
        sounds = []
        for snd in soundList:
            sounds.append(self.load_sound(snd[SOUND_TITLE], snd[SOUND_VOLUME]))
        return sounds

    # play on a specific channel fx
    def play_fx(self, channel, sound_fx):
        if not pg.mixer.Channel(channel).get_busy():
            pg.mixer.Channel(channel).play(sound_fx)

    def fade_out_fx(channel, time):
        pass

    def load_image(self, name, scale, alpha_transparency=False):
        """ enable the transparency key"""
        if alpha_transparency:
            image = pg.image.load(os.path.join(
                self.mainPath, name)).convert_alpha()
        else:
            image = pg.image.load(os.path.join(self.mainPath, name)).convert()
        rect = image.get_rect()
        if scale < 1.0:
            image = pg.transform.scale(
                image, (int(rect.w * scale), int(rect.h * scale)))
        assert image
        self.image_ref += 1
        return image

    # for mixer music mp3 : return the titles as strings.
    def get_music_list(self, musicList):
        music_path = []
        for title in musicList:
            music_path.append(os.path.join(self.mainPath, title))
            self.music_ref += 1
        return music_path

    # Load and return a list of image and rects
    def load_img_list(self, imgList, scale, flag=False):
        image = []
        for name in imgList:
            image.append(self.load_image(name, scale, flag))
        return image

    def load_font(self, name, size):
        name = os.path.join(self.mainPath, name)
        font = pg.font.Font(name, size)
        assert font
        self.font_ref += 1
        return font

    def load_fnt_list(self, fntList):
        fonts = []
        for fnt in fntList:
            fonts.append(self.load_font(fnt[FONT_NAME], fnt[FONT_SIZE]))
        return fonts

    # functions to print text in the screen with white by default.
    def print_font(self, font, message, vect, color=(255, 255, 255)):
        self.screen.blit(font.render(message, True, color), vect)

    def load_global(self, imgList, sndList, fntList, mscList):
        """take arguments for sounds fx, images,
        music titles (string list) and fonts
        """
        img = self.load_img_list(imgList)
        snd = self.load_snd_list(sndList)
        fnt = self.load_fnt_list(fntList)
        msc = self.get_music_list(mscList)
        return img, snd, fnt, msc

    def destroy_global(self):
        pass

    # Parsing data with json
    def save_res_info(self, data, fileName, indent=True):
        if not indent:
            inf = json.dumps(data)
        else:
            inf = json.dumps(data, indent=4, sort_keys=True)
        fileName = os.path.join(self.mainPath, fileName)
        with open(fileName, "w") as fp:
            fp.write(inf)
        fp.close()

    # parsing file
    def get_res_info(self, fileName):
        self.persiLayer = fileName
        fileName = os.path.join(self.mainPath, fileName)
        with open(fileName, "r") as fp:
            str = fp.read()
        fp.close()

        return json.loads(str)
