"""
pyFloating.py
"""

import pygame
import pyImage
import math


class Floating:

    def __init__(self, floater, dim, clock, period = 1.5): # period in seconds

        self.height = dim[1]
        self.width = dim[0]
        self.floater = pyImage.ScaleGraphics(floater, self.width, True, False)
        self.floaterHeight = self.floater.get_height()
        self.floatHeight = self.height - self.floaterHeight
        self.y = 0
        self.angularFrequency = 2 * math.pi / period / 1000 # in rad ms^-1
        self.time = 0
        self.clock = clock
        # y = cos(wt), where w is in ms^-1 and t is in ms

    def Reset(self):
        self.time = 0

    def Update(self):
        self.time += self.clock.get_time()
        self.y = self.floatHeight * (math.sin(self.angularFrequency * self.time) + 1)/2
        tempSurf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        tempSurf.blit(self.floater, (0, self.y))
        return tempSurf