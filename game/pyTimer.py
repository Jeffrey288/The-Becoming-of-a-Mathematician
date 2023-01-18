"""
pyTimer.py
"""

import pygame
from math import *
from GlobalVar import *

class BgTimer:

    def __init__(self, timerLength, clock): # timerLength in seconds

        self.timerLength = timerLength # self.timerLength in seconds
        self.clock = clock
        self.Reset() # self.timerLeft in milliseconds

    def Reset(self):
        self.timeLeft = self.timerLength * 1000

    def Update(self):
        self.timeLeft -= self.clock.get_time()
        if self.timeLeft <= 0:
            self.timeLeft = 0
            return False
        else:
            return True

class Timer(BgTimer):

    def __init__(self, timerLength, clock, fontSize, font = BlockyFont, color = (0, 0, 0)):
        super().__init__(timerLength, clock)
        self.font = pygame.font.Font(font, fontSize)
        self.color = color

    def Surface(self):

        mins = floor(self.timeLeft / 1000) // 60
        sec = floor(self.timeLeft / 1000) % 60
        ms = floor((self.timeLeft // 100) % 10)
        Surf = self.font.render(f"{mins:02}:{sec:02}.{ms:01}", 1, self.color)
        return Surf

    def Time(self):

        return self.timeLeft / 1000 if self.timeLeft >= 0 else 0

def main():
    pygame.init()
    Screen = pygame.display.set_mode((900, 600))
    myClock = pygame.time.Clock()
    myTimer = Timer(3, myClock, 30,color=(100, 200, 200))

    while myTimer.Update():
        Screen.fill((0,0,0))
        Screen.blit(myTimer.Surface(), (0, 0))
        pygame.display.update()
        myClock.tick(30)

if __name__ == "__main__":
    main()
