"""
mSprite.py
"""

import pyImage

class Sprite:

    __slots__ = "name", "fullHP", "graphics", "nowHP"

    def __init__(self, name, fullHP, graphics, nowHP = -1):

        self.name = name
        self.fullHP = fullHP
        self.graphics = graphics
        self.nowHP = self.fullHP if nowHP == -1 else nowHP

    def returnSurface(self, height):
        return pyImage.ScaleGraphics(self.graphics, height, False, True)

    def copy(self):
        return Sprite(self.name, self.fullHP, self.graphics)