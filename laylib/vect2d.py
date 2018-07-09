
from math import cos, sin


class Vector2d(object):

    """ Vector2d : Basic operations vectors in 2d
       file version: 0.2
       Author : A.Amine (Gttd) """

    def __init__(self, x=0.0, y=0.0):
        self.values = (x, y)

    # vect * s
    def factor(self, s):
        return Vector2d(self.values[0] * s, self.values[1] * s)

    def rotate(self, angle):
        # deg -> rad
        angle *= 0.0174532925199444
        xrot = (self.values[0] * cos(angle)) - (self.values[1] * sin(angle))
        yrot = (self.values[1] * cos(angle)) + (self.values[0] * sin(angle))
        return (xrot, yrot)

    def magnitude(self):
        return (self.values[0] ** 2 + self.values[1] ** 2) ** 0.5

    def normalize(self):
        mag = self.magnitude()
        return (self.values[0] / mag, self.values[1] / mag)

    def dot(self, other):
        return (self.values[0] * other[0]) + (self.values[1] * other[1])

    def set(self, x, y):
        return Vector2d(x, y)

    # distance between 2 points
    def dist(self, other):
        d = ((self.values[0] - other[0])**2 +
             (self.values[1] - other[1])**2) ** 0.5
        return d

    # =============== overloading op

    def __repr__(self):
        # L'affichage de l'objet dans l'interpréteur
        return "Vector2d(%s, %s)" % self.values

    def __add__(self, other):
        x = self.values[0] + other[0]
        y = self.values[1] + other[1]
        return Vector2d(x, y)

    def __sub__(self, other):
        x = self.values[0] - other[0]
        y = self.values[1] - other[1]
        return Vector2d(x, y)

    def __mul__(self, other):
        x = self.values[0] * other[0]
        y = self.values[1] * other[1]
        return Vector2d(x, y)

    def __pow__(self, other):
        x = self.values[0] ** other[0]
        y = self.values[1] ** other[1]
        return Vector2d(x, y)

    def __truediv__(self, other):
        x = self.values[0] / other[0]
        y = self.values[1] / other[1]
        return Vector2d(x, y)

    def __floordiv__(self, other):
        x = self.values[0] // other[0]
        y = self.values[1] // other[1]
        return Vector2d(x, y)

    def __mod__(self, other):
        x = self.values[0] % other[0]
        y = self.values[1] % other[1]
        return Vector2d(x, y)

    # i:
    def __iadd__(self, other):
        # op + is overloaded
        return self + other

    def __isub__(self, other):
        return self - other

    def __imul__(self, other):
        return self * other

    def __itruediv__(self, other):
        return self / other

    def __ifloordiv__(self, other):
        return self // other

    def __imod__(self, other):
        return self % other
    # scl

    def __iter__(self):
        return self.values.__iter__()

    def __len__(self):
        return len(self.values)

    def __getitem__(self, key):
        if key > 1:
            raise ValueError('Index exceed the limit of Vector2d. (0, 1)')
        return self.values[key]
