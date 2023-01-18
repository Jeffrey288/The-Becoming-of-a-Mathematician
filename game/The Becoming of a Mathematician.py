"""
The Becoming of a Mathematician.py
"""

import sys, os

# Disable
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore
def enablePrint():
    sys.stdout = sys.__stdout__

# Ref: https://stackoverflow.com/questions/8391411/suppress-calls-to-print-python

print(
"""

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
The Becoming of a Mathematician

(This project is a part of the HKDSE ICT SBA. Please do not
redistribute this program without the developer's permission.)

Please read the Game Manual for information on how to play
this game. Change game settings and profile picture in the 
Game Settings folder.

Please ignore the libpng warnings. They have no effect on
the program, but cannot be suppressed.

Enjoy~~
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

"""
)


blockPrint()

import pygame
import simpleaudio
from pygame.locals import *
import traceback
import mErrors

enablePrint()



def MainMenu(Screen):

    pygame.init()
    pygame.font.init()

    # Screen and Background
    EntranceSequence.EntranceSequence(Screen)

    menu = pyMenu.FrameMenu(Screen, GlobalVar.CentralClock)

    menu.AddGraphics(pygame.image.load(GlobalVar.MenuIcon))
    menu.InsertText("The Becoming of a Mathematician", Title = True)
    menu.InitiateMenu()

    ad = menu.InsertMenu("Adventure Mode")
    mu = menu.InsertMenu("Multiplayer Mode")
    pr = menu.InsertMenu("Practice Mode")
    menu.InsertText("", Enter=True)
    qu = menu.InsertMenu("Quit Game")

    displayFuncSurf = menu.DisplayFunctionSurf()

    def DisplayFunction():
        Screen.fill((255, 255, 255))
        Screen.blit(displayFuncSurf, (0, 0))

    Enter = True

    run = True
    while run:

        Screen.fill((255, 255, 255))

        for event in pygame.event.get():
            GlobalVar.Quit(event)
            counter = menu.Scrolling(event)
            if counter == pr:
                Enter = True
                PracticeMode.m_PracticeMode(Screen)
            elif counter == qu:
                run = False
            elif counter == ad:
                Enter = True
                AdventureMode.m_AdventureMode(Screen)
            elif counter == mu:
                Enter = True
                MultiplayerMode.m_MultiplayerMode(Screen)

        if Enter:

            GlobalVar.audio.FeedAudio(GlobalVar.MenuMusic)
            displayFuncSurf = menu.DisplayFunctionSurf()
            pyAnimation.FadeIn(Screen, DisplayFunction, GlobalVar.CentralClock, GlobalVar.GameFPS)
            Enter = False


        menu.Blit()
        GlobalVar.LoopBundle()

    pyAnimation.FadeOut(Screen, GlobalVar.CentralClock, GlobalVar.GameFPS)
    pygame.quit()


if __name__ == '__main__':

    # すべてはここからはじまるのだ。
    try:

        import GlobalVar
        import ATextBox
        import pyText
        import pyMenu

        import Main_AdventureMode as AdventureMode
        import Main_MultiplayerMode as MultiplayerMode
        import Main_PracticeMode as PracticeMode
        import time
        import pyAnimation
        import Main_EntranceSequence as EntranceSequence



        Size = GlobalVar.SettingDict["Resolution"]
        ScreenWidth = Size[0]
        ScreenHeight = Size[1]
        Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
        pygame.display.set_caption("The Becoming of a Mathematician")
        MainMenu(Screen)

    except mErrors.QuestionError as e:

        print("Question.json file not found. Please reinstall the game or contact the game developer.")

    except mErrors.BossError as e:

        print("Boss.txt file not found. Please reinstall the game or contact the game developer.")

    except GlobalVar.QuitError:

        pass

    except Exception as e:
    
        file = open("files/ErrorFile.txt", "w")
        traceback.print_exc(file=file)
        file.close()

        try:
            popUp = ATextBox.PopUp(Screen)
            popUp.TextBox.InsertText("The game has crashed:\n"
                                              + str(e) + "\n Please contact the game developer.", "center"),
            popUp.TextBox.Finalize()
            popUp.Start()

            run = True
            while run:

                for event in pygame.event.get():
                    GlobalVar.Quit(event)
                    result = popUp.TextBox.Event(event, popUp.Offset())
                    if result:
                        run = False

                popUp.Blit()
                GlobalVar.LoopBundle()

            pyAnimation.FadeOut(Screen, GlobalVar.CentralClock, GlobalVar.GameFPS)
        except:
            pass

