"""
ALoad.py
"""


import pyMenu
from GlobalVar import *
import APlayer
import pyAnimation

def LoadOptions(screen):

    menu = pyMenu.FrameMenu(screen)

    menu.AddGraphics(pygame.image.load(Floppy))

    menu.InsertText("Load Options", Title = True)
    menu.InsertText("Please choose a load option.", Text=True)

    menu.InitiateMenu()
    one = menu.InsertMenu("New Game")
    menu.InsertText("Play the game from the start", Explanation=True)
    menu.InsertText("", Enter=True)
    two = menu.InsertMenu("Load from Save")
    menu.InsertText("Play from where you last left off", Explanation=True)
    menu.InsertText("", Enter=True)
    three = menu.InsertMenu("Return to Main Menu")

    displayFunctionSurf = menu.DisplayFunctionSurf()
    def display2Function():
        screen.blit(displayFunctionSurf, (0, 0))

    def displayFunction():
        screen.fill(color.white)
        menu.Blit()

    pyAnimation.EnterFade(screen, display2Function, CentralClock, GameFPS)

    while True:

        displayFunction()

        for event in pygame.event.get():
                Quit(event)
                counter = menu.Scrolling(event)
                if counter == one:
                    return APlayer.Initialize(), True, True
                elif counter == two:
                    return APlayer.LoadSave(PlayerDataFileName), False, True
                elif counter == three:
                    return None, None, False
        LoopBundle()
