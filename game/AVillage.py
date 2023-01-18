"""
AVillage.py
"""


import ATutor
import pyMenu
import pygame
import GlobalVar
import AGrinding
import ABossBattle
import AShop
import AMenu
import pyAnimation
import ATextBox
import pyImage
import mDebug


def a_Village(screen, playerInfo, sequence = True):

    def displayFunction():
        screen.fill((255, 255, 255))
        menu.Blit()

    menu = pyMenu.FrameMenu(screen)

    Wallpaper = pygame.image.load(GlobalVar.DefaultVillageWallpaper)
    menu.AddGraphics(Wallpaper)

    menu.InsertText("Village", GlobalVar.color.black, Title = True)

    menu.InitiateMenu()

    shops = menu.InsertMenu("The Shops")
    grind = menu.InsertMenu("Grinding")
    fight = menu.InsertMenu("Journey On...")

    menu.InsertText("", Enter = True)
    guide = menu.InsertMenu("Math Guide")
    gmenu = menu.InsertMenu("Game Menu")


    displayFunctionSurf = menu.DisplayFunctionSurf()
    def display2Function():
        screen.fill((255, 255, 255))
        screen.blit(displayFunctionSurf, (0, 0))

    pyAnimation.EnterFade(screen, display2Function, GlobalVar.CentralClock, GlobalVar.GameFPS)

    popUp = ATextBox.PopUp(screen)

    functionList = [
        lambda : popUp.TextBox.InsertText("Welcome to the Village!", "center", bold = True),
        lambda : popUp.TextBox.InsertText("Your goal is to defeat Mathematicians by intellectual battles: "
                                          "answering the math questions that they ask you. You can fight "
                                          "Mathematicians by selecting “Journey On...”.", "center"),
        lambda : popUp.TextBox.InsertText("You should practice and become stronger before fighting them. "
                                          "To do that, select “Grinding”. This mode allows you to battle "
                                          "people.", "center"),
        lambda : popUp.TextBox.InsertText("You can gain skill points and money by fighting Mathematicians "
                                          "and by Grinding. Spend them at “The Shops” to strength your attack"
                                          " or defense skills.", "center"),
        lambda : popUp.TextBox.InsertText("For other settings, please access “Game Menu”. You can check your "
                                          "game statistics, save your game, or quit the game through there.",
                                          "center"),
        lambda: popUp.TextBox.InsertText("Game Statistics in the \"Game Menu\" has detailed explanation about what "
                                         "equipment and potions do. If you are unsure about them, "
                                         "be sure to visit it.", "center"),
        lambda : popUp.TextBox.InsertText("Have fun!", "center", bold = True)
    ] if sequence else [
        lambda: popUp.TextBox.InsertText("Welcome back!", "center", bold=True)
    ]

    for i in functionList:
        popUp.TextBox.Reset()
        i()
        popUp.TextBox.Finalize()
        displayFunction()
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

    GlobalVar.audio.FeedAudio(GlobalVar.VillageMusic)

    # menu.menu.SetCounter(1)

    exitFlag = False
    while not exitFlag:

        displayFunction()

        for event in pygame.event.get():

            temp = mDebug.ReloadPlayer(event)
            if temp:
                playerInfo = temp
                temp = None

            GlobalVar.Quit(event)

            choice = menu.Scrolling(event)
            if choice == shops:
                # Shops
                AShop.a_DoShop(screen, playerInfo)
            elif choice == grind:
                # Grinding
                AGrinding.a_DoGrinding(screen, playerInfo)
            elif choice == fight:
                # Fight Boss
                exitFlag = ABossBattle.a_DoBoss(screen, playerInfo)
            elif choice == gmenu:
                # Menu
                exitFlag = AMenu.a_Menu(screen, playerInfo)
            elif choice == guide:
                # Guide
                ATutor.a_tutor(playerInfo)

            if choice != None and choice != 3 and not exitFlag:
                GlobalVar.audio.FeedAudio(GlobalVar.VillageMusic)
                displayFunctionSurf = menu.DisplayFunctionSurf()
                pyAnimation.EnterFade(screen, displayFunction, GlobalVar.CentralClock, GlobalVar.GameFPS)

        GlobalVar.LoopBundle()

    pyAnimation.FadeOut(screen, GlobalVar.CentralClock, GlobalVar.GameFPS)

def main():
    import pygame
    import APlayer
    screen = pygame.display.set_mode((1280, 800))
    playerInfo = APlayer.LoadSave("TestPlayer.txt")
    a_Village(screen, playerInfo, False)

if __name__ == "__main__":
    main()

