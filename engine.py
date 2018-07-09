import pygame as pg
from settings import *
from laylib.resources import *
from body import *
from explosion import *
from random import *


class Engine:
    """
    The game logic: Main class.
    """

    def __init__(self):
        """ set all game data anbd params """
        self.running = True
        self.playing = True
        self.dt = 0.0
        self.clock = pg.time.Clock()
        self.screen = pg.display.get_surface()
        # Game ressources to load once on the main.
        self.img = self.snd = self.fnt = None
        self.ship = None
        self.lives = SHIP_LIVES
        self.score = self.best_score = 0
        self.level = 0
        self.life_pos = SCORE_POS[0] - 6
        self.time_of_play = pg.time.get_ticks()

    def main_loop(self):
        """ run the main game loop """
        while self.running:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.event_listener()
            self.update()
            self.draw()

    def new_game(self):
        """
        reset the game and variables like score life..etc
        """
        # remove old astroids if any
        for asteroid in self.asteroid_sprites:
            asteroid.kill()
        # remove risidual particles if any
        for particle in self.particles_sprites:
            particle.kill()

        self.lives = SHIP_LIVES
        self.score = 0
        self.level = 0
        self.playing = True
        self.next_level()

    def next_level(self):
        """
        Jump to the next
        """
        self.level += 1
        # if ship exist destroy it and creat a new one
        if self.ship:
            self.ship.kill()
        # create some asteroids
        for _ in range(ASTR_NUMBER + self.level):
            Asteroid(self, TYPE_BIG)
        # set a new ship
        self.ship = Ship(self)

    def event_listener(self):
        """
        manage the game events keyboard, mouse...etc
        """
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.playing = False
                    self.running = False
                if event.key == pg.K_RETURN:
                    if not self.playing:
                        self.new_game()

    def update(self):
        """
        this will update the whole game
        """
        self.all_sprites.update(self.dt)
        # when the bullet hits asteroids both deseapear
        hits = self.collide(self.asteroid_sprites,
                            self.bullet_sprites, True, True)
        # if its a big or medium asteroid creat two asteroids
        for hit in hits:
            if hit.type == TYPE_BIG:
                Explosion(self, hit.pos, hit.radius, NB_PRTCL_BIG)
                Asteroid(self, TYPE_MEDIUM, hit.pos)
                Asteroid(self, TYPE_MEDIUM, hit.pos)
            elif hit.type == TYPE_MEDIUM:
                Explosion(self, hit.pos, hit.radius, NB_PRTCL_MED)
                Asteroid(self, TYPE_SMALL, hit.pos)
                Asteroid(self, TYPE_SMALL, hit.pos)
            elif hit.type == TYPE_SMALL:
                Explosion(self, hit.pos, hit.radius, NB_PRTCL_SML)
            # play the explosion fx
            self.snd[BOOM_FX].play()
            self.score += 10
            # mark the last time astroid get destoyed for next level transition
            self.time_of_play = pg.time.get_ticks()

        # if an asteroid hit the ship, ship get destroyed
        ship_hit = self.collide(self.asteroid_sprites,
                                self.ship_sprites, False, False)
        # if we are not in the invulnerability period:
        if ship_hit:
            if pg.time.get_ticks() - self.ship.last_respawn > SHIELD_PERIOD:
                self.death()
        # see if player win the level jump up to the next:
        if not len(self.asteroid_sprites) and self.playing:
            if pg.time.get_ticks() - self.time_of_play > TIME_TO_NEXT_LVL:
                self.next_level()

    def draw(self):
        """ this will draw the whole game """
        self.screen.fill(BLACK)
        if self.playing:
            self.all_sprites.draw(self.screen)
            self.res.print_font(self.fnt[0], str(
                "{}".format(self.score)), SCORE_POS)
            self.res.print_font(self.fnt[0], str(
                "{:02d}".format(self.level)), LEVEL_POS)
            self.res.print_font(self.fnt[0], str(
                "{:.3f}".format(self.clock.get_fps())), FPS_POS)
            # draw player lives:
            for _ in range(self.lives):
                self.screen.blit(self.img[SHIP_IMG], (self.life_pos, LIFE_POS))
                self.life_pos += 16
            self.life_pos = SCORE_POS[0] - 6
        elif self.running:
            self.res.print_font(self.fnt[1], str(
                "GAME OVER"), (300, 245))
            self.res.print_font(self.fnt[2], str(
                "press ENTER to restart"), (300, 290))
            self.res.print_font(self.fnt[3], str(
                "Best score: {}".format(self.best_score)), (10, 10))
        pg.display.flip()

    def death(self):
        """ destroy the ship """
        self.ship.kill()
        # creat explosions
        Explosion(self, self.ship.pos * 0.90, self.ship.radius, NB_PRTCL_BIG)
        Explosion(self, self.ship.pos, self.ship.radius, NB_PRTCL_BIG)
        # play explosion sound
        self.snd[BOOM_FX].play()
        # if the ship is still alive..
        if self.lives > 1:
            self.lives -= 1
            self.ship = Ship(self)
        else:
            self.game_over()

    def game_over(self):
        # stop the thruster sound if playing
        self.snd[THRUSTER_FX].stop()
        self.playing = False
        # save the best score:
        self.best_score = int(self.res.get_res_info('best.zd'))
        if self.score > self.best_score:
            self.best_score = self.score
            self.res.save_res_info(self.best_score, 'best.zd', False)

    def load_game(self, dataFolder, persistenceLayer):
        """
        the environement.py call this method on the main.
        load game resources, (should be extern to this class)
        fetch whatever resources we need.
        """
        self.res = Resources(dataFolder)
        data = self.res.get_res_info(persistenceLayer)
        self.img = self.res.load_img_list(data['imgList'], 1.0, True)
        self.snd = self.res.load_snd_list(data['sndList'])
        self.fnt = self.res.load_fnt_list(data['fntList'])
        self.music_titles = self.res.get_music_list(data['mscList'])
        print(self.res.__dict__)
        # set sprites groups:
        self.all_sprites = pg.sprite.Group()
        self.ship_sprites = pg.sprite.Group()
        self.asteroid_sprites = pg.sprite.Group()
        self.bullet_sprites = pg.sprite.Group()
        self.particles_sprites = pg.sprite.Group()

    def load_levels(self, dataFolder, fileLevels):
        """
        if the prototype contain levels use this function.
        """
        res = Resources(dataFolder)
        self.levels = res.get_res_info(fileLevels)

    def destroy_game(self):
        """
        At the end of main file destory all ressources.
        """
        self.all_sprites.empty()

        if self.img:
            del self.img
        if self.snd:
            del self.snd
        if self.fnt:
            del self.fnt
        if self.res:
            del self.res

    @staticmethod
    def collide(body1, body2, k1, k2):
        """ test groupe sprites collision"""
        return pg.sprite.groupcollide(body1, body2, k1, k2,
                                      pg.sprite.collide_circle)
