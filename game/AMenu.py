"""
AMenu.py
"""

import APlayer
import pygame
import pyMenu
import AShop
from pygame.locals import *
from GlobalVar import *
import APlayer
import pyImage
import pyAnimation

def a_Menu(screen, playerInfo):

    menu = pyMenu.FrameMenu(screen)

    menu.AddGraphics(pygame.image.load(Settings))

    menu.InsertText("Game Menu", Title = True)

    menu.InitiateMenu()
    menu.InsertMenu("View Statistics")
    menu.InsertMenu("Save Game")
    menu.InsertMenu("Quit Game")

    menu.InsertText("", Enter=True)
    menu.InsertMenu("Return to Village")

    def displayFunction():
        screen.fill(color.white)
        menu.Blit()

    displayFunctionSurf = menu.DisplayFunctionSurf()
    def display2Function():
        screen.blit(displayFunctionSurf, (0, 0))

    # pyAnimation.EnterFade(screen, display2Function, CentralClock, GameFPS)

    while True:

        displayFunction()

        for event in pygame.event.get():
                Quit(event)
                counter = menu.Scrolling(event)
                if counter == 0:
                    # View stats
                    a_Stats(screen, playerInfo)
                elif counter == 1:
                    # Save game
                    a_Save(screen, playerInfo)
                elif counter == 2:
                    # Quit game
                    exitFlag = a_QuitMenu(screen)
                    if exitFlag:
                        return True
                elif counter == 3:
                    return False

        LoopBundle()

def a_QuitMenu(screen):

    menu = pyMenu.FrameMenu(screen)

    menu.InsertText("Quit Game", Title = True)
    menu.InsertText("Are you sure you want to quit the game?", Header = True)
    menu.InsertText("Unsaved data will be discarded.", Explanation = True)
    menu.InsertText("", Enter=True)

    menu.InitiateMenu()
    menu.InsertMenu("No")
    menu.InsertMenu("Yes")

    while True:
        screen.fill(color.white)
        menu.Blit()
        for event in pygame.event.get():
            Quit(event)
            counter = menu.Scrolling(event)
            if counter == 0:
                return False
            elif counter == 1:
                return True
        LoopBundle()

def a_Save(screen, playerInfo):

    def Exists(filename):

        try:
            file = open(filename, 'r')
        except:
            return False
        else:
            return True

    def Confirmation(screen):

        subMenu = pyMenu.FrameMenu(screen)

        subMenu.AddGraphics(pygame.image.load(Floppy))

        subMenu.InsertText("Save Game", Title=True)
        subMenu.InsertText("The old save is not empty.", Text=True)
        subMenu.InsertText("Would you like to overwrite the old save?", Text=True)
        subMenu.InsertText("", Enter=True)

        subMenu.InitiateMenu()
        subMenu.InsertMenu("No")
        subMenu.InsertMenu("Yes")

        while True:
            screen.fill(color.white)
            subMenu.Blit()
            for event in pygame.event.get():
                Quit(event)
                counter = subMenu.Scrolling(event)
                if counter == 0:
                    return False
                elif counter == 1:
                    return True
            LoopBundle()

    menu = pyMenu.FrameMenu(screen)
    menu.AddGraphics(pygame.image.load(Floppy))
    filename = PlayerDataFileName

    if Exists(filename):
        check = Confirmation(screen)
        if check:
            pass
        else:
            return
    else:
        pass

    # Saving procedure
    APlayer.SaveFile(filename, playerInfo)

    menu.InsertText("Save Game", Title=True)
    menu.InsertText("", Enter=True)
    menu.InsertText("", Enter=True)
    menu.TextWrap("Game data has been saved successfully.", Header=True)
    menu.InsertText("You may safely quit the game.", Header=True)
    menu.InsertText("(Press Enter to continue)", Explanation=True)

    while True:
        screen.fill(color.white)
        menu.Blit()
        for event in pygame.event.get():
            Quit(event)
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    return
        LoopBundle()

def a_Stats(screen, playerInfo):

    expDict = playerInfo.Experience()
    playerSkill = playerInfo.Skills()
    equipmentDict = playerInfo.Equipment()
    potionDict = playerInfo.Potions()

    def Stat(pageNumber):

        screen.fill(color.white)
        screen.blit(titleTextSurf, (textHorzShift, topCoord))
        if pageNumber == 0:
            One()
        elif pageNumber == 1:
            Two()
        elif pageNumber == 2:
            Three()
        elif pageNumber == 3:
            Four()

        screen.blit(graphicsList[pageNumber], (graphicsHorzShift, graphicsVertShift))

    def Blit(tempText, tempExplanation, tempTop):

        tempSurf = textFont.render(tempText, 1, color.black)
        tempESurf = explanationFont.render(tempExplanation, 1, color.black)

        screen.blit(tempSurf, (textHorzShift, tempTop))
        tempTop += textFontSize + textSpacing
        screen.blit(tempESurf, (textHorzShift, tempTop))
        tempTop += explanationFontSize + textSpacing * 2


        return tempTop

    def Heading(headingText):

        tempTop = textStartVert
        # Heading
        tempSurf = headerFont.render(headingText, 1, color.black)
        screen.blit(tempSurf, (textHorzShift, tempTop))
        tempTop += headerFontSize + headerSpacing

        return tempTop

    def One():

        tempTop = Heading("Experience and Balance (1/4)")

        # Level
        tempText = "Level: " + str(expDict["level"]) + "/" + str(playerInfo.Maximum["level"])
        tempExplanation = "By levelling up using EXP you can earn skill points."

        tempTop = Blit(tempText, tempExplanation, tempTop)

        # Experience
        tempText = "Experience Points (EXP): " + str(expDict["exp"])
        tempExplanation = "(" + str(expDict["expLevel"]) + " EXP needed for the next level; " \
                          + str(expDict["expReq"]) + " left to go)"
        tempExplanation2 = "You can gain EXP from fighting and grinding."

        tempSurf = textFont.render(tempText, 1, color.black)
        tempESurf = explanationFont.render(tempExplanation, 1, color.black)
        tempE2Surf = explanationFont.render(tempExplanation2, 1, color.black)

        screen.blit(tempSurf, (textHorzShift, tempTop))
        tempTop += textFontSize + textSpacing
        screen.blit(tempESurf, (textHorzShift, tempTop))
        tempTop += explanationFontSize + textSpacing
        screen.blit(tempE2Surf, (textHorzShift, tempTop))
        tempTop += explanationFontSize + textSpacing * 2

        # Skill Points
        tempText = "Skill Points: " + str(playerInfo.skillPt)
        tempExplanation = "You can use skill points to level up your skills."

        tempTop = Blit(tempText, tempExplanation, tempTop)

        # Balance
        tempText = "Balance: $" + str(playerInfo.Cash())
        tempExplanation = "You can use cash to buy equipment and potions."

        tempTop = Blit(tempText, tempExplanation, tempTop)

    def Two():

        tempTop = Heading("Skills (2/4)")

        explanation = (
            "You will deal a base damage of " + str(playerInfo.fullAP()) + ".",
            "Reduces the damage you take by " + f"{playerInfo.defensePerc() * 100:.3g}" + "%.",
            "Lengthening your answering time by  " + f"{playerInfo.timePerc() * 100:.3g}" + "%.",
            "You have a " + f"{playerInfo.dodgePerc() * 100:.3g}" + "% chance of dodging an attack.",
            "Your maximum health is " + str(playerInfo.fullHP()) + ".",
        )

        for i in range(5):
            skill = playerInfo.SkillIndex[i + 1]
            tempText = playerInfo.SkillName[skill] + ": " \
                       + str(playerSkill[skill]) + " / " \
                       + str(playerInfo.Maximum["skills"][skill])
            tempExplanation = explanation[i]

            tempTop = Blit(tempText, tempExplanation, tempTop)

    def Three():

        tempTop = Heading("Equipment (3/4)")

        explanation = (
            "Reducing the damage you take by " + f"{playerInfo.chestPerc() * 100:.3g}" + "%.",
            "Reducing the damage you take by " + f"{playerInfo.legPerc() * 100:.3g}" + "%.",
            "Strengthing your attacks by " + f"{playerInfo.swordPerc() * 100:.3g}" + "%.",
        )

        for i in range(3):
            equipment = AShop.ShopClass.EquipmentIndex[i + 1]
            tier = equipmentDict[equipment]
            equipementName = AShop.ShopClass.equipmentName(equipment, tier) if tier != 0 else "None"

            tempText = equipment.title() + ": " + equipementName
            tempExplanation = explanation[i]

            tempTop = Blit(tempText, tempExplanation, tempTop)

    def Four():

        tempTop = Heading("Potions (4/4)")

        explanation = (
            "Regenerates " + f"{HealthPotionPerc * 100:.3g}" + "% of your full health.",
            "Increases your attack power by " + f"{AttackPotionPerc * 100:.3g}" + "% (one turn only).",
            "Reducing the damage you take by " + f"{DefendPotionPerc * 100:.3g}" + "% (one turn only).",
        )

        for i in range(3):
            potion = AShop.ShopClass.PotionIndex[i + 1]
            qnty = potionDict[potion]
            potionName = AShop.ShopClass.potionName(potion)

            tempText = potionName + ": " + str(qnty)
            tempExplanation = explanation[i]

            tempTop = Blit(tempText, tempExplanation, tempTop)

    WidthTotal = 29.7
    HeightTotal = 21.0

    # Text Related
    TopCoord = 2.1 / HeightTotal
    TitleFont = 1.4 / HeightTotal
    HeaderFont = 0.9 / HeightTotal
    TextFont = 0.65 / HeightTotal
    ExplanationFont = 0.50 / HeightTotal
    TitleSpacing = 1.6 / HeightTotal
    HeaderSpacing = 0.6 / HeightTotal
    TextSpacing = 0.30 / HeightTotal
    TextHorzShift = 3.2 / WidthTotal

    # Image Related
    GraphicsSize = 9.7 / HeightTotal
    GraphicsVertShift = 5.0 / HeightTotal
    GraphicsHorzShift = 15.4 / WidthTotal
    MenuHorzShift = 2.2 / WidthTotal
    MenuSpacing = 1.1 / WidthTotal
    MenuTextWidth = (5.5 + 1/3) / WidthTotal
    MenuVertShift = 1.9 / HeightTotal
    ScrollerSize = 1.8 / HeightTotal
    MenuTextSize = 0.7 / HeightTotal
    MenuHeight = 1.6 / HeightTotal

    height = screen.get_height()
    width = screen.get_width()

    topCoord = int(TopCoord * height)
    titleFontSize = int(TitleFont * height)
    headerFontSize = int(HeaderFont * height)
    textFontSize = int(TextFont * height)
    explanationFontSize = int(ExplanationFont * height)
    titleSpacing = int(TitleSpacing * height)
    headerSpacing = int(HeaderSpacing * height)
    textSpacing = int(TextSpacing * height)
    textHorzShift = int(TextHorzShift * width)

    graphicsSize = int(GraphicsSize * height)
    graphicsHorzShift = int(GraphicsHorzShift * width)
    graphicsVertShift = int(GraphicsVertShift * height)
    menuHorzShift = int(MenuHorzShift * width)
    menuSpacing = int(MenuSpacing * width)
    menuVertShift = int(MenuVertShift * height)
    scrollerSize = int(ScrollerSize * height)
    menuTextSize = int(MenuTextSize * height)
    menuHeight = int(MenuHeight * height)
    menuTextWidth = int(MenuTextWidth * width)

    titleFont = pygame.font.Font(DefaultMenuTitleFontString, titleFontSize)
    headerFont = pygame.font.Font(DefaultMenuHeaderFontString, headerFontSize)
    textFont = pygame.font.Font(DefaultMenuTextFontString, textFontSize)
    explanationFont = pygame.font.Font(DefaultMenuExplanationFontString, explanationFontSize)
    menuFont = pygame.font.Font(DefaultMenuMenuFontString, menuTextSize)

    textStartVert = topCoord + titleFontSize + titleSpacing

    pageNumber = 0

    """
    There are 4 pages.
    First page: basic information
    Second page: skills
    Third page: equipment
    Fourth page: potions
    """

    MenuStatOne = pygame.image.load(DefaultMenuStatOne)
    MenuStatTwo = pygame.image.load(DefaultMenuStatTwo)
    MenuStatThree = pygame.image.load(DefaultMenuStatThree)
    MenuStatFour = pygame.image.load(DefaultMenuStatFour)

    graphicsList = [
        MenuStatOne,
        MenuStatTwo,
        MenuStatThree,
        MenuStatFour,
    ]

    for i in range(4):
        graphicsList[i] = pyImage.ScaleGraphics(graphicsList[i], graphicsSize, False, True)

    # Defining the scrolling
    menuRect = [
        (menuHorzShift, height - menuVertShift - menuHeight),
        (menuHorzShift + scrollerSize + menuTextWidth + menuSpacing, height - menuVertShift - menuHeight),
        (menuHorzShift + 2 * scrollerSize + 2 * menuTextWidth + menuSpacing * 2, height - menuVertShift - menuHeight),
    ]
    
    mainMenu = pyMenu.SelectionMenu(DefaultMenuScroller, (menuTextWidth, scrollerSize), alignment="center")
    mainMenu.CreateItem("Previous Page", menuFont, menuRect[0])
    mainMenu.CreateItem("Return", menuFont, menuRect[1])
    mainMenu.CreateItem("Next Page", menuFont, menuRect[2])

    titleTextSurf = titleFont.render("Player Statistics", 1, color.black)

    refillRect = (
        0,
        height - menuVertShift - menuHeight,
        width,
        menuVertShift + menuHeight
    )

    Stat(pageNumber)

    # Main Loop:
    exitMenu = False
    while not exitMenu:

        pygame.draw.rect(screen, color.white, refillRect)

        mainMenu.DisplayItem(screen)

        for event in pygame.event.get():
            Quit(event)

            if event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    mainMenu.ScrollItem(1)
                if event.key == K_LEFT:
                    mainMenu.ScrollItem(-1)
            counter = mainMenu.Scrolling(event)

            if counter == 2:
                pageNumber = (pageNumber + 1) % 4
                Stat(pageNumber)
            elif counter == 0:
                pageNumber = (pageNumber + 3) % 4
                Stat(pageNumber)
            elif counter == 1:
                exitMenu = True

        pygame.display.update()

