"""
Main_EntranceSequence.py
"""

import pygame
import pyAnimation
import pyText
import GlobalVar
import ATextBox
from pygame.locals import *


def EntranceSequence(screen):

    width = screen.get_width()
    height = screen.get_height()

    font = pygame.font.Font(GlobalVar.BlockyFont, height//10)
    lines = pyText.TextWrap("The Becoming of\na Mathematician", font, int(width*4/5))
    displaySurf = pyText.TextRender(lines, font, int(height/20), "center", (255, 255, 255))
    rect = displaySurf.get_rect()
    rect.center = (width//2, height//2)

    def DisplayFunction():
        screen.fill((0, 0, 0))
        screen.blit(displaySurf, rect)

    pyAnimation.FadeIn(screen, DisplayFunction, GlobalVar.CentralClock, GlobalVar.GameFPS)

    popUp = ATextBox.PopUp(screen)

    def Menu(msg):

        def func():
            popUp.TextBox.InsertText(msg,
                                     "center", bold = True)
            popUp.TextBox.InsertMenu("OK.")
            popUp.TextBox.InsertMenu("Understood.")

        return func

    functionList = [
        lambda : popUp.TextBox.InsertText("When you see an arrow on the bottom right corner, "
                                          "press Enter to proceed.", "center", bold = True),
        Menu("In a menu as shown, use the up, down buttons to choose an option."),
        Menu("You can also use your mouse to click on the options."),
        lambda: popUp.TextBox.InsertText("Please read the game manual for more information.", "center", bold=True),
        lambda : popUp.TextBox.InsertText("Have fun!\n(You may skip this tutorial by pressing "
                                          "ESC next time.)", "center", bold = True)
    ]

    DisplayFunction()
    pygame.time.delay(1000)

    for i in functionList:

        popUp.TextBox.Reset()
        i()
        popUp.TextBox.Finalize()

        DisplayFunction()
        popUp.Start()

        run = True
        while run:

            for event in pygame.event.get():
                GlobalVar.Quit(event)
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pyAnimation.FadeOut(screen, GlobalVar.CentralClock, GlobalVar.GameFPS)
                        return
                result = popUp.TextBox.Event(event, popUp.Offset())
                if result or result == 0:
                    run = False

            popUp.Blit()
            GlobalVar.LoopBundle()

    pyAnimation.FadeOut(screen, GlobalVar.CentralClock, GlobalVar.GameFPS)
