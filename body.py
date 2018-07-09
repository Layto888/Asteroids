import pygame as pg
from settings import *
from random import *
from pygame.math import Vector2 as vect2d
from laylib.resources import *
from laylib.util import *


class Ship(pg.sprite.Sprite):
    """
    The ship class is the player in the game
    it moves rotates and shots mobs.
    Ship commands:
    Left - Right keys: only rotate the ship 360°
    up key: Thuster acceleration in the direction pointed by the ship.
    """

    def __init__(self, engine):
        self.groups = engine.all_sprites, engine.ship_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.engine = engine
        self.image = engine.img[SHIP_IMG]
        self.img_copy = self.image
        self.radius = 12
        self.rect = self.image.get_rect()
        self.pos = vect2d(WIDTH / 2, HEIGHT / 2)
        self.vel = vect2d(0.0, 0.0)
        self.acc = vect2d(0.0, 0.0)
        # self.thrust = self.right = self.left = False
        self.rot = 0.0
        self.rot_vel = 0.0
        self.last_shot = 0
        self.res = Resources()
        self.last_respawn = pg.time.get_ticks()

    def update(self, dt):
        """ this will update Ship """
        self.vel = vect2d(0.0, 0.0)
        self.rot_vel += self.rot_vel * ROT_FRICTION
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.rot_vel = SHIP_ROT_VEL
        if keys[pg.K_RIGHT]:
            self.rot_vel = -SHIP_ROT_VEL
        if keys[pg.K_UP]:
            self.acc += vect2d(0, -SHIP_MAX_VEL).rotate(-self.rot)
            # play on a specific channel the acceleration sound
            self.res.play_fx(THRUSTER_FX, self.engine.snd[THRUSTER_FX])
        else:
            self.engine.snd[THRUSTER_FX].fadeout(TIME_FADE_OUT)
        if keys[pg.K_SPACE]:
            # create a new bullet when the space bar is pressed : shoot.
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_SHOT_RATE:
                self.last_shot = now
                self.engine.snd[BULLET_FX].play()
                Bullet(self.engine, self.pos, self.rot)
        # movement equation of the ship with space friction / acceleration.
        self.rotate(dt)
        self.translate(dt)
        # keep the ship in the window
        bondary_limit(self.pos)

    def rotate(self, dt):
        """ rotate a surface around its center."""
        self.image = pg.transform.rotate(self.img_copy, self.rot)
        self.rot = (self.rot + self.rot_vel * dt) % 360
        self.rect = self.image.get_rect()

    def translate(self, dt):
        """move the object by time"""
        self.vel += self.acc * dt
        self.pos += self.vel * dt + 0.5 * self.acc * dt ** 2
        self.rect.center = self.pos
        self.acc += self.vel * SHIP_FRICTION


class Asteroid(pg.sprite.Sprite):
    """
    The Asteroid class represent the enemy class.
    We have Big, medium and small asteroids,
    they rotate when transelate with different speed,
    they get divided when shoted, except for the smallest ones.
    """

    def __init__(self, engine, astr_type, pos=None):
        self.groups = engine.all_sprites, engine.asteroid_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.type = astr_type
        # switch types
        if self.type == TYPE_BIG:
            self.radius = 50
            self.image = engine.img[randint(BIGAS1_IMG, BIGAS3_IMG)]
            self.rect = self.image.get_rect()
            self.pos = vect2d(WIDTH / 2, HEIGHT / 2)
            # asteroids must start far from the ship
            while dist(self.pos.x, self.pos.y,
                       WIDTH / 2.0, HEIGHT / 2.0) < self.radius * 7.0:
                self.pos = vect2d(randint(0, WIDTH), randint(0, HEIGHT))

            self.vel = vect2d(0, 1).rotate(
                uniform(-ASTR_ROT_VEL, ASTR_ROT_VEL)) * BIG_ASTR_VEL
        elif self.type == TYPE_MEDIUM:
            self.radius = 25
            self.image = engine.img[randint(MIDAS1_IMG, MIDAS3_IMG)]
            self.rect = self.image.get_rect()
            self.pos = vect2d(pos)
            self.vel = vect2d(0, 1).rotate(
                uniform(-ASTR_ROT_VEL, ASTR_ROT_VEL)) * MEDIUM_ASTR_VEL
        elif self.type == TYPE_SMALL:
            self.radius = 12
            self.image = engine.img[randint(SMLAS1_IMG, SMLAS3_IMG)]
            self.rect = self.image.get_rect()
            self.pos = vect2d(pos)
            self.vel = vect2d(0, 1).rotate(
                uniform(-ASTR_ROT_VEL, ASTR_ROT_VEL)) * SMALL_ASTR_VEL

        self.img_copy = self.image
        # for rotation
        self.rot = 0.0
        self.rot_vel = uniform(-ASTR_ROT_VEL, ASTR_ROT_VEL)

    def update(self, dt):
        """ update the asteroid rotation translation -
            limit the edge """
        self.rotate(dt)
        self.translate(dt)
        bondary_limit(self.pos)

    def rotate(self, dt):
        """ rotate a surface around its center."""
        self.rot = (self.rot + self.rot_vel * dt) % 360
        self.image = pg.transform.rotate(self.img_copy, self.rot)
        self.rect = self.image.get_rect()

    def translate(self, dt):
        """move the object by time"""
        self.pos += self.vel * dt
        self.rect.center = self.pos


class Bullet(pg.sprite.Sprite):
    """
    Bullet class represent the gun in the ship.
    """

    def __init__(self, engine, pos, ship_rotation):
        self.groups = engine.all_sprites, engine.bullet_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.radius = 1
        self.image = engine.img[BULLET_IMG]
        self.rect = self.image.get_rect()
        self.pos = vect2d(pos)
        self.rect.center = pos
        self.vel = vect2d(0, 1).rotate(-ship_rotation) * BULLET_VEL
        self.spawn_time = pg.time.get_ticks()

    def update(self, dt):
        self.pos += self.vel * dt
        self.rect.center = self.pos
        # kill bullets after a certain time
        if pg.time.get_ticks() - self.spawn_time > BULLET_DURATION:
            self.kill()
        # if bullet hit asteroid kill it


def bondary_limit(position: vect2d) -> None:
    # check if an object exced the boudary of the screen
    if position.x < 0:
        position.x += WIDTH
    elif position.x > WIDTH:
        position.x -= WIDTH
    if position.y < 0:
        position.y += HEIGHT
    elif position.y > HEIGHT:
        position.y -= HEIGHT
