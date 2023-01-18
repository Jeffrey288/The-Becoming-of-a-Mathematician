"""
pyImage.py
"""


import pygame

def ScaleGraphics(graphics, metric, xbool, ybool):

    if xbool and not ybool:
        ratioCoeff = metric / graphics.get_width()
        return pygame.transform.scale(graphics, (metric, int(ratioCoeff * graphics.get_height())))
    elif not xbool and ybool:
        ratioCoeff = metric / graphics.get_height()
        return pygame.transform.scale(graphics, (int(ratioCoeff * graphics.get_width()), metric))
    else:
        print("Error occurred in ScaleGraphics")

# Not used
def SmoothScaleGraphics(graphics, metric, xbool, ybool):

    if xbool and not ybool:
        ratioCoeff = metric / graphics.get_width()
        return pygame.transform.smoothscale(graphics, (metric, int(ratioCoeff * graphics.get_height())))
    elif not xbool and ybool:
        ratioCoeff = metric / graphics.get_height()
        return pygame.transform.smoothscale(graphics, (int(ratioCoeff * graphics.get_width()), metric))
    else:
        print("Error occurred in ScaleGraphics")

def Crop(image, position, dimensions):

    Surf = pygame.Surface(dimensions, pygame.SRCALPHA)
    Surf.blit(image, (-position[0], -position[1]))
    return Surf

def Wallpaper(image, size):

    a = ScaleGraphics(image, size[1], False, True)
    if a.get_width() < size[0]:
        k = pygame.Surface(size)
        k.fill((255, 255, 255))
        k.blit(a, (int((size[0] - a.get_width())/2), 0))
        a = k
    else:
        a = Crop(a, (int((a.get_width() - size[0])/2), 0), size)
    return a
