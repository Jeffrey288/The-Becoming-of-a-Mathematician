"""
pyMouse.py
"""

from pygame.locals import *


def InArea(event, start, size, offset):

    if event.type == MOUSEMOTION:
        pos = event.pos
        if start[0] + offset[0] <= pos[0] <= start[0] + size[0] + offset[0] \
                and start[1] + offset[1] <= pos[1] <= start[1] + size[1] + offset[1]:
            return True
    return False
