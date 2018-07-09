# util lib for rapid prototyping games

import math
import pygame as pg

# distance between two Circles.


def dist(x1, y1, x2, y2):
    d = ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5
    return d


def rad2deg(rad):
    return rad * 180.0 / math.pi()


def deg2rad(deg):
    return deg * 3.14 / 180.0

# this function rotates a point p around the point origin.


def _rotate(x, y, angle):
    vector = ((x * math.cos(angle) - y * math.sin(angle)),
              (x * math.sin(angle) + x * math.cos(angle)))
    return vector

# this function rotates a point p1 around the point p0.


def rotate2p(x1, y1, x0, y0, angle):
    dx = x1 - x0
    dy = y1 - y0

    vector = ((dx * math.cos(angle) - dy * math.sin(angle)),
              (dx * math.sin(angle) + dx * math.cos(angle)))
    vector[0] += x0
    vector[1] += y0
    return vector


# time & space

 # get times function set frame rate ...etc
def get_time(type='ms'):
    # get in seconds format
    if type is 's':
        return pg.time.get_ticks() / 1000.0
    else:
        return pg.time.get_ticks()

# graphics stuffs :
# rotate an image while keeping its center and size


def rotateDeg(image, angle):
    angle %= 360.0
    orig_rect = image.get_rect()
    rot_image = pg.transform.rotate(image, angle)
    orig_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(orig_rect).copy()
    return rot_image


def xIntersect(body1, body2):
    return (body1.x + body1.w) < (body2.x + body2.w) * 0.5 or \
        (body1.x + body1.w) >= (body2.x + body2.w) * 0.5


def yIntersect(body1, body2):
    return (body1.y + body1.h) < (body2.y + body2.h) or \
        (body1.y + body1.h) >= (body2.y + body2.h)


# return 1 if sides intersection
# return 2 if top/bottom intersection
# otherwise return 0.
# def rIntersection(boy1, box2):
#   left1 = box1.x
#   right1 = box1.x + box1.w
#   top1 = box1.y
#   bottom1 = box1.y + box1.h

#   left2 = box2.x
#   right2 = box2.x + box2.w
#   top2 = box2.y
#   bottom2 = box2.y + box2.h

#   if (right2 >= left1) or (left2 <= right1):
#       return 1
#   if (top2 >= bottom1) or (bottom2 <= top1):
#       return 2
#   return 0
