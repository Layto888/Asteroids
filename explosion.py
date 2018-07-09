import pygame as pg
from settings import *
from laylib.resources import *
from random import *
from pygame.math import Vector2 as vect2d


class Particle (pg.sprite.Sprite):
    """
    unique particle class
    """

    def __init__(self, engine, pos, radius):
        self.groups = engine.all_sprites, engine.particles_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image = engine.img[BULLET_IMG]
        self.radius = radius * 0.35
        self.rect = self.image.get_rect()
        self.pos = vect2d(0, self.radius).rotate(uniform(0.0, 360.0))
        self.vel = self.pos.normalize() * uniform(PARTICLE_MIN_SPEED,
                                                  PARTICLE_MAX_SPEED)
        self.pos += vect2d(pos)
        self.start_time = pg.time.get_ticks()

    def update(self, dt):
        self.image.set_alpha(10)
        self.pos += self.vel * dt
        self.vel *= (1.0 - dt)
        self.rect.center = self.pos
        # kill the particle after a certain time
        if self.is_over():
            self.kill()

    def draw(self):
        self.image.set_alpha(10)
        print('alpha is set')

    def is_over(self):
        # tell us when the particle is dead
        return pg.time.get_ticks() - self.start_time > PARTICLE_LIFE_TIME


class Explosion():
    """
    generate a groupe of particles sprites
    """

    def __init__(self, engine, pos, radius, particles_num=150):
        for _ in range(particles_num):
            Particle(engine, pos, radius)
