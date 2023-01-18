"""
pyAnimation.py
"""

import pygame
FadeInConst = 1.08
FadeOutConst = 1.08

def FadeOut(screen, clock, fps):

    surf = pygame.Surface((screen.get_size()))
    alpha = 2

    while alpha < 255:
        pygame.event.get()
        alpha = min(alpha**FadeOutConst, 255)
        surf.set_alpha(int(alpha))
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(fps)

def FadeIn(screen, displayFunction, clock, fps):

    surf = pygame.Surface((screen.get_size()))
    alpha = 255

    while alpha > 0:
        pygame.event.get()
        alpha = max(0, alpha//FadeInConst)
        surf.set_alpha(int(alpha))
        # Blits the screenshot onto the screen
        displayFunction()
        # Blits the half-transparent black overlay
        screen.blit(surf, (0, 0))
        pygame.display.update()
        clock.tick(fps)

def EnterFade(screen, displayFunction, clock, fps, waitTime = 50):

    FadeOut(screen, clock, fps)
    pygame.time.delay(waitTime)
    FadeIn(screen, displayFunction, clock, fps)

if __name__ == "__main__":

    screen = pygame.display.set_mode((500, 500))
    screen.fill((255, 255, 255))
    surf = pygame.Surface((300, 300))
    surf.set_alpha(0)
    screen.blit(surf, (0, 0))
    pygame.display.update()
    while True:
        screen.fill((255, 255, 255))
        FadeOut(screen)

    input()



