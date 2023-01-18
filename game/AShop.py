"""
AShop.py
"""


import pyAnimation
import pyImage
import pyMenu
import pygame
from pygame.locals import *
import GlobalVar
import math
import APlayer
import pyFloating
import pyText
import pyInput


class ShopClass:

    EquipmentIndex = {
        1: "chestplate",
        2: "leggings",
        3: "sword"
    }

    PotionIndex = {
        1 : "regenPot",
        2 : "attackPot",
        3 : "defendPot"
    }

    EquipmentPrefix = {
        1 : "Wooden",
        2 : "Carbon",
        3 : "Silver",
        4 : "Iron",
        5 : "Steel",
        6 : "Gold",
        7 : "Diamond",
        8 : "Platinum",
        9 : "Lonsadleite"
    }

    TopEquipmentName = {
        "chestplate" : "Laplace's T-Shirt",
        "leggings" : "Euler's Beach Trunks",
        "sword" : "Newton's Apple Tree Twig'"
    }

    PotionName = {
        "regenPot" : "Potion of Regeneration",
        "attackPot" : "Potion of Braveness",
        "defendPot" : "Potion of Perseverance"
    }

    PotionPrice = {
        "regenPot" : 1000,
        "attackPot" : 4000,
        "defendPot" : 4000
    }

    @staticmethod
    def EquipmentGraphics(equipment, tier):
        if tier < 10:
            if equipment == "chestplate":
                return pygame.image.load(GlobalVar.DefaultChestplate)
            elif equipment == "leggings":
                return pygame.image.load(GlobalVar.DefaultLeggings)
            elif equipment == "sword":
                return pygame.image.load(GlobalVar.DefaultSword)
            else:
                print("Error occurred in ShopClass.equipmentGraphics.")
        else:
            if equipment == "chestplate":
                return pygame.image.load(GlobalVar.DefaultShirt)
            elif equipment == "leggings":
                return pygame.image.load(GlobalVar.DefaultTrunks)
            elif equipment == "sword":
                return pygame.image.load(GlobalVar.DefaultTwig)
            else:
                print("Error occurred in ShopClass.equipmentGraphics.")

    @staticmethod
    def PotionGraphics(equipment):
        if equipment == "regenPot":
            return pygame.image.load(GlobalVar.DefaultPotion2)
        elif equipment == "attackPot":
            return pygame.image.load(GlobalVar.DefaultPotion1)
        elif equipment == "defendPot":
            return pygame.image.load(GlobalVar.DefaultPotion3)
        else:
            return pygame.image.load(GlobalVar.DefaultPotion4)

    @ staticmethod
    def SkillGraphics():
        return pygame.image.load(GlobalVar.DefaultSkills)

    @staticmethod
    def equipmentPrice(equipment, tier):
        if equipment == "chestplate":
            return math.ceil(8000 * (tier * (1 + tier / 10) ** (tier / 5)))
        elif equipment == "leggings":
            return math.ceil(6000 * (tier * (1 + tier / 10) ** (tier / 5)))
        elif equipment == "sword":
            return math.ceil(10000 * (tier * (1 + tier / 10) ** (tier / 5)))
        else:
            print("Error occurred in ShopClass.equipmentPrice.")

    @staticmethod
    def equipmentName(equipment, tier):
        if tier < 10:
            if equipment in ["chestplate", "leggings", "sword"]:
                return ShopClass.EquipmentPrefix[tier] + " " + equipment.title()
            else:
                print("Error occurred in ShopClass.equipmentName.")
        elif tier == 10:
            return ShopClass.TopEquipmentName[equipment]

    @staticmethod
    def potionName(potion):
        return ShopClass.PotionName[potion]

    @staticmethod
    def potionPrice(potion):
        return ShopClass.PotionPrice[potion]

class ShopMenu:

    GraphicsShift = 0.60 / 6.8
    GraphicsSpacing = 0.60 / 6.8
    ItemMenuShift = 0.2 / 2.1
    GraphicsTextSpacing = 0.2 / 6.8
    ItemMenuTextSpacing = 0.2 / 2.1
    CursorTextRatio = 0.7/(2.1 + 0.7)
    GraphicsTextRatio = 0.7

    def __init__(self, scroller, fontName, dim, exitRect, exitMsg = "Leave shop"):

        self.height = dim[1]
        self.width = dim[0]
        self.counter = 1

        self.graphicsShift = int(self.GraphicsShift * self.width)
        self.graphicsSpacing = int(self.GraphicsSpacing * self.width)
        self.itemMenuShift = int(self.ItemMenuShift * self.height)
        self.graphicsTextSpacing = int(self.GraphicsTextSpacing * self.height)

        self.graphicsSize = int((self.width - self.graphicsShift*2 - self.graphicsSpacing*2)/3)
        self.graphicsHeight = int(self.height * self.GraphicsTextRatio)
        self.itemMenuHeight = self.height - self.graphicsHeight - self.graphicsTextSpacing
        self.cursorSize = int(self.CursorTextRatio * self.itemMenuHeight)
        self.itemMenuHeight -= int(self.CursorTextRatio * self.itemMenuHeight)
        self.itemMenuWidth = 2 * (self.graphicsShift - self.itemMenuShift) + self.graphicsSize
        self.itemMenuSpacing = int((self.width - 3 * self.itemMenuWidth - 2 * self.itemMenuShift)/2)
        self.itemMenuTextSpacing = int(self.ItemMenuTextSpacing * self.itemMenuHeight)
        self.itemMenuTextSize = int((self.itemMenuHeight - 2 * self.itemMenuTextSpacing) / 3)

        self.exitRect = exitRect

        self.scroller = scroller
        self.fontName = fontName
        self.itemMenuFont = pygame.font.Font(self.fontName, self.itemMenuTextSize)
        self.graphicsRect = [
            (self.graphicsShift + int(self.graphicsSize/2), int(self.graphicsHeight/2)),
            (self.graphicsShift + self.graphicsSize + self.graphicsSpacing +
             int(self.graphicsSize/2), int(self.graphicsHeight/2)),
            (self.graphicsShift + self.graphicsSize * 2 + self.graphicsSpacing * 2 +
             int(self.graphicsSize/2),  int(self.graphicsHeight/2))
        ]
        self.itemMenuRect = [
            (self.width, self.height),
            (self.itemMenuShift, self.graphicsTextSpacing + self.graphicsHeight),
            (self.itemMenuShift + self.itemMenuWidth + self.itemMenuSpacing,
                self.graphicsTextSpacing + self.graphicsHeight),
            (self.itemMenuShift + self.itemMenuWidth * 2 + self.itemMenuSpacing * 2,
                self.graphicsTextSpacing + self.graphicsHeight)
        ]
        self.exitMenuFont = pygame.font.Font(self.fontName, self.exitRect[3])

        self.itemMenu = pyMenu.SelectionMenu(self.scroller,
                                             (self.itemMenuWidth + 10, self.itemMenuHeight),
                                             alignment = "center", scrollerSize = self.cursorSize)
        for i in range(4):
            self.itemMenu.CreateItem("", self.itemMenuFont, self.itemMenuRect[i],
                                     str(i), multiline=True, scrollerPos="below")
        self.itemMenu.ScrollItem(+1)

        self.exitMenu = pyMenu.SelectionMenu(pygame.transform.rotate(self.scroller, -90),
                                             (self.exitRect[2]+3, self.exitRect[3]),
                                             alignment = "left")
        self.exitMsg = exitMsg
        self.exitMenu.CreateItem(self.exitMsg, self.exitMenuFont, (self.exitRect[:2]), "0")
        self.exitMenu.CreateItem("", self.exitMenuFont, (self.width, self.height), "1")

        self.itemMenu.SetCounter(self.counter)
        self.exitMenu.SetCounter(self.counter)

        self.graphics = [None, None, None]

        self.temp = 1

    def ChangeItem(self, index, text, graphics = None):

        try:
            if graphics:
                self.graphics[index - 1] = pyImage.ScaleGraphics(graphics,  self.graphicsHeight, False, True)
            else:
                self.graphics[index - 1] = pyImage.ScaleGraphics(pygame.image.load(GlobalVar.DefaultShopSoldOut),
                                                                  self.graphicsHeight, False, True)
            self.itemMenu.ChangeItem(index, text, self.itemMenuFont, self.itemMenuRect[index],
                                     str(index), multiline = True, scrollerPos="below")
        except:
            print("Error occurred in ShopMenu.ChangeItem.")

    def Scroll(self, event, offset):

        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.counter += 3
                self.counter %= 4
            elif event.key == K_RIGHT:
                self.counter += 1
                self.counter %= 4
            elif event.key == K_UP:
                if self.counter == 0:
                    self.counter = self.temp
            elif event.key == K_DOWN:
                if self.counter != 0:
                    self.temp = self.counter
                    self.counter = 0
            elif event.key == K_RETURN:
                return self.counter
            self.itemMenu.SetCounter(self.counter)
            self.exitMenu.SetCounter(self.counter)
        else:
            item = self.itemMenu.Clicking(event, offset)
            ex = self.exitMenu.Clicking(event)
            re = False
            if item in range(1, 4):
                re = True
            else:
                if ex == 0:
                    re = True
            self.counter = self.itemMenu.GetSelected() if self.itemMenu.GetSelected() in range(4) else self.counter
            self.counter = self.exitMenu.GetSelected() if self.exitMenu.GetSelected() in range(4) else self.counter
            self.itemMenu.SetCounter(self.counter)
            self.exitMenu.SetCounter(self.counter)
            if re:
                return self.counter

    def DisplayMenu(self):

        tempSurf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(3):
            tempRect = self.graphics[i].get_rect()
            tempRect.center = self.graphicsRect[i]
            tempSurf.blit(self.graphics[i], tempRect)
        self.itemMenu.DisplayItem(tempSurf)
        return tempSurf

    def DisplayExit(self, screen):

        self.exitMenu.DisplayItem(screen)

class PaymentBox:

    TextSpacing = 0.2 / 2.1
    HorzShift = 0.2/2.1
    FloaterWidth = 0.6 / 7.1

    def __init__(self, screen, pos, dim, fontName, typingFontName, textBoxWallpaper = None):

        self.height = dim[1]
        self.width = dim[0]
        self.pos = pos
        self.fontName = fontName
        self.typingFontName = typingFontName
        self.screen = screen

        self.textSpacing = int(self.height * self.TextSpacing)
        self.horzShift = int(self.HorzShift * self.width)
        self.textHeight = int( (self.height - self.textSpacing * 4) / 3 )
        self.textWidth = self.width - 2 * self.horzShift
        self.floaterWidth = int(self.FloaterWidth * self.width)
        self.floaterHeight = self.textHeight + self.textSpacing

        self.totalHeight = self.textHeight * 3 + self.textSpacing * 4

        if textBoxWallpaper:
            self.textBoxWallpaper = pygame.transform.scale(textBoxWallpaper, dim)
        else:
            self.textBoxWallpaper = pygame.transform.scale(GlobalVar.DefaultShopTextboxWallpaper, dim)

        self.font = pygame.font.Font(self.fontName, min(30, self.textHeight))
        self.typingFont = pygame.font.Font(self.typingFontName, min(30, self.textHeight))

    def PaymentConfirmation(self, confirmationText, textColor = (0, 0, 0), confirmationColor = (0, 0, 0), scroller = None):

        if scroller:
            myScroller = scroller
        else:
            myScroller = GlobalVar.DefaultMenuScroller

        textSurf = self.font.render(confirmationText, 1, textColor)
        blitRect = self.DisplayTextBox(3)

        menu = pyMenu.SelectionMenu(myScroller,
                                    (self.textWidth, self.textHeight),
                                    textShift = self.textSpacing)
        menu.CreateItem("No", self.font, blitRect[1], color = confirmationColor)
        menu.CreateItem("Yes", self.font, blitRect[2], color = confirmationColor)

        # Main loop
        while True:

            for event in pygame.event.get():
                GlobalVar.Quit(event)

                counter = menu.Scrolling(event, self.pos)
                if counter == 0:
                    return False
                elif counter == 1:
                    return True

            tempSurf = self.textBoxWallpaper.copy()
            tempSurf.blit(textSurf, blitRect[0])
            menu.DisplayItem(tempSurf)
            self.screen.blit(tempSurf, self.pos)

            pygame.display.update()
            GlobalVar.CentralClock.tick(30)

    def DisplayTextBox(self, lines):
        if lines == 1:
            return [(self.horzShift, int((self.totalHeight - self.textHeight) / 2))]
        elif lines == 2:
            return [(self.horzShift, int(self.totalHeight/2 - (self.textSpacing / 2) - self.textHeight)),
                    (self.horzShift, int(self.totalHeight/2 + (self.textSpacing / 2)))]
        elif lines == 3:
            return [(self.horzShift, self.textSpacing),
                    (self.horzShift, self.textHeight + self.textSpacing*2),
                    (self.horzShift, self.textHeight*2 + self.textSpacing*3)]
        else:
            print("Error occured in DisplayTextBox.")


    def PaymentDialogue(self, text, textColor = (0,0,0), floater = None):

        if floater:
            myFloater = pyFloating.Floating(floater,
                                            (self.floaterWidth, self.floaterHeight), GlobalVar.CentralClock)
        else:
            myFloater = pyFloating.Floating(GlobalVar.DefaultShopTextboxFloater,
                                            (self.floaterWidth, self.floaterHeight), GlobalVar.CentralClock)

        lines = pyText.TextWrap(text, self.font, self.textWidth)
        blitRect = self.DisplayTextBox(len(lines))
        linesSurf = pyText.TextRender(lines, self.font, self.textSpacing, color = textColor)

        floaterRect = (self.width - (self.floaterWidth + self.horzShift),
                       self.height - (self.floaterHeight + self.textSpacing))

        # Main loop
        while True:

            for event in pygame.event.get():
                GlobalVar.Quit(event)

                if event.type == KEYDOWN:
                   if event.key == K_RETURN:
                       return

            tempSurf = self.textBoxWallpaper.copy()
            tempSurf.blit(linesSurf, blitRect[0])
            tempSurf.blit(myFloater.Update(), floaterRect)
            self.screen.blit(tempSurf, self.pos)

            pygame.display.update()
            GlobalVar.CentralClock.tick(GlobalVar.GameFPS)


    def Quantity(self, range, msg = "Input quantity:", textColor = (0,0,0), promptColor = (0, 0, 0), typeColor = (0, 0, 0)):

        textLines = pyText.TextWrap(msg, self.font, self.textWidth)
        textSurf = pyText.TextRender(textLines, self.font, self.textSpacing, textColor)

        blitRect = self.DisplayTextBox(len(textLines) + 1)
        textPrompt = self.font.render(">>>", 1, promptColor)
        inputBox = pyInput.TextInput(self.typingFont, self.textWidth, GlobalVar.CentralClock, typeColor)
        inputBoxRect = (textPrompt.get_width() + self.textSpacing + blitRect[-1][0], blitRect[-1][1])

        while True:

            if inputBox.Typing():
                text = inputBox.Text()
                try:
                    if int(text) in range:
                        return int(text)
                except:
                    pass

            tempSurf = self.textBoxWallpaper.copy()
            tempSurf.blit(textSurf, blitRect[0])
            tempSurf.blit(textPrompt, blitRect[-1])
            tempSurf.blit(inputBox.Surface(), inputBoxRect)
            self.screen.blit(tempSurf, self.pos)

            pygame.display.update()
            GlobalVar.CentralClock.tick(30)

def a_DoShop(screen, playerInfo):

    def GenerateRect(exitMsg):

        exitRectTextWidth = pygame.font.Font(GlobalVar.BattleFontString, exitRectHeight).size(exitMsg)[0]
        return (int(screenWidth / 2 - exitRectHeight - exitRectTextWidth / 2),
                    topShift + menuHeight + int((bottomShift - exitRectHeight) / 2),
                    exitRectTextWidth, exitRectHeight)

    def Title(title):

        balance = int(playerInfo.Cash())
        balanceText = "Balance: " + str(balance)

        titleSurf = titleFont.render(title, 1, GlobalVar.color.black)
        balanceSurf = balanceFont.render(balanceText, 1, GlobalVar.color.black)

        screen.blit(titleSurf, titleRect)
        screen.blit(balanceSurf, balanceRect)

    def ArmourShop(screen, playerInfo):

        def Update(index):
            equipment = ShopClass.EquipmentIndex[index]
            nowtier = playerInfo.Equipment()[equipment]
            tier = nowtier + 1

            if tier <= 10:
                armourMenu.ChangeItem(index,
                                      ShopClass.equipmentName(equipment, tier) + "\n" # text
                                      + '$' + str(ShopClass.equipmentPrice(equipment, tier)),
                                      ShopClass.EquipmentGraphics(equipment, tier)) # graphics
            else:
                armourMenu.ChangeItem(index, "Sold Out!")

        aExitMsg = "Leave Shop"
        armourMenu = ShopMenu(GlobalVar.DefaultShopScroller, GlobalVar.BattleFontString,
                              (screenWidth, menuHeight), GenerateRect(aExitMsg),
                              aExitMsg)

        for index in range(1, 4):
            Update(index)

        while True:

            screen.fill(GlobalVar.color.white)
            Title("Armour and Weapons Shop")
            screen.blit(armourMenu.DisplayMenu(), (0, topShift))
            armourMenu.DisplayExit(screen)

            for event in pygame.event.get():
                GlobalVar.Quit(event)
                counter = armourMenu.Scroll(event, (0, topShift))

                if counter == 0:
                    # Leave Shop
                    return
                elif counter in range(1, 4):
                    equipment = ShopClass.EquipmentIndex[counter]
                    tier = playerInfo.Equipment()[equipment]
                    # Can the item be purchased?
                    if tier + 1 <= 10:
                        # Payment Process begins
                        textBox = PaymentBox(screen, (textBoxHorzShift, topShift + menuHeight + textBoxVertShift),
                                             (textBoxWidth, textBoxHeight),
                                             GlobalVar.DefaultShopTextboxTextFontString,
                                             GlobalVar.DefaultShopTextboxInputFontString)

                        nowtier = playerInfo.Equipment()[equipment]
                        tier = nowtier + 1
                        name = ShopClass.equipmentName(equipment, tier)
                        price = ShopClass.equipmentPrice(equipment, tier)

                        # Does the player have enough money?
                        if playerInfo.Cash() >= price:
                            confirmation = textBox.PaymentConfirmation("Confirm Purchase: " + name + "?",
                                                                       GlobalVar.color.blue)
                            if confirmation:
                                # The player buys it
                                playerInfo.Cash(-1 * price)
                                playerInfo.Equipment({equipment : 1})
                                textBox.PaymentDialogue("You have successfully purchased a " + name + ".")
                                Update(counter)
                            else:
                                # The player does not buy it
                                textBox.PaymentDialogue("Payment cancelled.", GlobalVar.color.blue)

                        # The player does not have enough money
                        else:
                            textBox.PaymentDialogue("You do not have enough cash.")
                    else:
                        pass

            GlobalVar.CentralClock.tick(30)
            pygame.display.update()

    def PotionShop(screen, playerInfo):

        def Update(index):
            potion = ShopClass.PotionIndex[index]
            potionMenu.ChangeItem(index,
                                    ShopClass.potionName(potion) + "\n"  # text
                                    + '$' + str(ShopClass.potionPrice(potion)),
                                    ShopClass.PotionGraphics(potion))  # graphics

        aExitMsg = "Leave Shop"
        potionMenu = ShopMenu(GlobalVar.DefaultShopScroller, GlobalVar.BattleFontString,
                              (screenWidth, menuHeight), GenerateRect(aExitMsg),
                              aExitMsg)

        for index in range(1, 4):
            Update(index)

        while True:

            screen.fill(GlobalVar.color.white)
            Title("Potion Shop")
            screen.blit(potionMenu.DisplayMenu(), (0, topShift))
            potionMenu.DisplayExit(screen)

            for event in pygame.event.get():
                GlobalVar.Quit(event)

                counter = potionMenu.Scroll(event, (0, topShift))

                if counter == 0:
                    # Leave Shop
                    return
                elif counter in range(1, 4):
                    # Payment Process begins
                    textBox = PaymentBox(screen, (textBoxHorzShift, topShift + menuHeight + textBoxVertShift),
                                         (textBoxWidth, textBoxHeight),
                                         GlobalVar.DefaultShopTextboxTextFontString,
                                         GlobalVar.DefaultShopTextboxInputFontString)

                    # Ask the player for quantity
                    potion = ShopClass.PotionIndex[counter]
                    name = ShopClass.potionName(potion)
                    price = ShopClass.potionPrice(potion)

                    qnty = textBox.Quantity(range(0, 100),
                                            "How many of the " + name + " would you like to buy? (0 to 99)")

                    # Does the player want to actually buy it?
                    if qnty != 0:

                        totalPrice = qnty * price

                        # Does the player have enough money?
                        if playerInfo.Cash() >= totalPrice:
                            confirmation = textBox.PaymentConfirmation("Confirm Purchase: " + name
                                                                       + ", Quantity: " + str(qnty) + "?",
                                                                       GlobalVar.color.blue)

                            if confirmation:
                                playerInfo.Cash(-1 * totalPrice)
                                playerInfo.Potions({potion : qnty})
                                textBox.PaymentDialogue("Payment successful.", GlobalVar.color.blue)
                            else:
                                textBox.PaymentDialogue("Payment cancelled.", GlobalVar.color.blue)
                        else:
                            textBox.PaymentDialogue("You do not have enough cash.", GlobalVar.color.blue)
                    else:
                        textBox.PaymentDialogue("Payment cancelled.", GlobalVar.color.blue)


            pygame.display.update()
            GlobalVar.CentralClock.tick(30)

    def SkillShop(screen, playerInfo):

        def Title(title):

            balanceText = "Skill Points: " + str(playerInfo.SkillPt())

            titleSurf = titleFont.render(title, 1, GlobalVar.color.black)
            balanceSurf = balanceFont.render(balanceText, 1, GlobalVar.color.black)

            screen.blit(titleSurf, titleRect)
            screen.blit(balanceSurf, balanceRect)

        STextHeight = 0.4
        SExplanationHeight = 0.15
        SExplanationSpacing = 0.03
        STextSpacing = 0.5
        SHeightTotal = STextHeight * 3 + STextSpacing * 4
        STextShift = 0.3
        SWidthTotal = 6.3

        sTextHeight = int(STextHeight / SHeightTotal * menuHeight)
        sExplanationHeight = int(SExplanationHeight / SHeightTotal * menuHeight)
        sExplanationSpacing = int(SExplanationSpacing / SHeightTotal * menuHeight)
        sTextSpacing = int(STextSpacing / SHeightTotal * menuHeight)
        sTextShift = int(STextShift / SWidthTotal * screenWidth)
        sHalfWidth = int(screenWidth / 2)
        sTextWidth = sHalfWidth - 2 * sTextShift
        sFont = pygame.font.Font(GlobalVar.DefaultShopFontString, exitSize)
        sEFont = pygame.font.Font(GlobalVar.DefaultMenuExplanationFontString, sExplanationHeight)

        exitMsg = "Leave Shop"
        exitRect = GenerateRect(exitMsg)

        textRect = [
            exitRect,
            (sTextShift, topShift + sTextSpacing),
            (sTextShift, topShift + sTextSpacing * 2 + sTextHeight),
            (sTextShift, topShift + sTextSpacing * 3 + sTextHeight * 2),
            (sTextShift + sHalfWidth, topShift + sTextSpacing),
            (sTextShift + sHalfWidth, topShift + sTextSpacing * 2 + sTextHeight)
        ]

        explanationRect = [
            (sTextShift + sTextHeight, topShift + sTextSpacing + sExplanationSpacing + sTextHeight),
            (sTextShift + sTextHeight, topShift + sTextSpacing * 2 + sTextHeight + sExplanationSpacing + sTextHeight),
            (sTextShift + sTextHeight, topShift + sTextSpacing * 3 + sTextHeight * 2 + sExplanationSpacing + sTextHeight),
            (sTextShift + sHalfWidth + sTextHeight, topShift + sTextSpacing + sExplanationSpacing + sTextHeight),
            (sTextShift + sHalfWidth + sTextHeight, topShift + sTextSpacing * 2 + sTextHeight + sExplanationSpacing + sTextHeight)
        ]

        skillDict = playerInfo.Skills()
        menu = pyMenu.SelectionMenu(GlobalVar.MenuArrow,
                                    (sTextWidth, sTextHeight),
                                    textShift = sTextSpacing, scrollerSize=exitSize)


        menu.CreateItem(exitMsg, sFont, textRect[0])
        for index in range(1, 6):
            skill = APlayer.Player.SkillIndex[index]
            menu.CreateItem("[" + str(skillDict[skill]) + "/200] " + APlayer.Player.SkillName[skill],
                            sFont, textRect[index])


        explanationSurf = [0 for i in range(5)]

        def UpdateStatement():

            explanation = (
                "You will deal a base damage of " + str(playerInfo.fullAP()) + ".",
                "Reduces the damage you take by " + f"{playerInfo.defensePerc() * 100:.3g}" + "%.",
                "Lengthening your answering time by  " + f"{playerInfo.timePerc() * 100:.3g}" + "%.",
                "You have a " + f"{playerInfo.dodgePerc() * 100:.3g}" + "% chance of dodging an attack.",
                "Your maximum health is " + str(playerInfo.fullHP()) + ".",
            )

            for i in range(5):
                lines = pyText.TextWrap(explanation[i], sEFont, int(sHalfWidth - 2 * sTextShift - sTextHeight))
                explanationSurf[i] = pyText.TextRender(lines, sEFont, SExplanationSpacing)

        UpdateStatement()

        while True:

            screen.fill(GlobalVar.color.white)
            Title("Skill Shop")
            menu.DisplayItem(screen)
            for i in range(5):
                screen.blit(explanationSurf[i], explanationRect[i])
            pygame.display.update()

            for event in pygame.event.get():
                GlobalVar.Quit(event)

                counter = menu.Scrolling(event)

                if counter == 0:
                    # Leave Shop
                    return
                elif counter in range(1, 6):
                    # Payment Process begins
                    textBox = PaymentBox(screen, (textBoxHorzShift, topShift + menuHeight + textBoxVertShift),
                                         (textBoxWidth, textBoxHeight),
                                         GlobalVar.DefaultShopTextboxTextFontString,
                                         GlobalVar.DefaultShopTextboxInputFontString)

                    # Ask the player for quantity
                    skill = APlayer.Player.SkillIndex[counter]
                    name = APlayer.Player.SkillName[skill]
                    skillPt = playerInfo.SkillPt()
                    skillLvl = playerInfo.Skills()[skill]

                    # Does the player have any points?
                    if skillPt > 0:
                        # Can the player put points?
                        if skillLvl < 200:
                            maxPut = min(skillPt, 200 - skillLvl)
                            qnty = textBox.Quantity(range(0, maxPut + 1),
                                                    "How many points would you like to put into "
                                                    + APlayer.Player.SkillName[skill] + "? (0 - " + str(maxPut) + ")")

                            # Confirmation
                            if qnty != 0:
                                confirmation = textBox.PaymentConfirmation("Confirm: dedicate " + str(qnty)
                                                                           + " " + ("points" if qnty > 1 else "point") +
                                                                           " into " + name + "?", GlobalVar.color.blue)
                                if confirmation:
                                    playerInfo.SkillPt(-1 * qnty)
                                    newSkill = playerInfo.Skills({skill : qnty})
                                    textBox.PaymentDialogue("Payment successful! Your " + name + " skill is now "
                                                            + "level " + str(newSkill[skill]) + "!")

                                    # Redefine Menu
                                    skill = APlayer.Player.SkillIndex[counter]
                                    menu.ChangeItem(counter, "[" + str(skillDict[skill]) + "/200] " +
                                                    APlayer.Player.SkillName[skill],
                                                    sFont, textRect[counter])
                                    UpdateStatement()

                                else:
                                    textBox.PaymentDialogue("Payment cancelled.")
                            else:
                                textBox.PaymentDialogue("Payment cancelled.")
                        else:
                            textBox.PaymentDialogue("You have already maxed out " + name + "!")
                    else:
                        textBox.PaymentDialogue("You don't have any skill points!" +
                                                "\nEarn some from grinding or fighting Mathematicians.")

            GlobalVar.CentralClock.tick(30)

    # *******************End of Module Definition*****************************

    TopShift = 0.8
    MenuHeight = 2.1
    BottomShift = 1.4
    HeightTotal = TopShift + MenuHeight + BottomShift
    TitleSize = 0.30
    BalanceSize = 0.2
    TextBoxHeight = 1
    TextBoxWidth = 5.4
    WidthTotal = 6.8
    HorzShift = 0.4
    BalanceShift = WidthTotal - 2.0

    screenHeight = screen.get_height()
    screenWidth = screen.get_width()

    topShift = int(TopShift / HeightTotal * screenHeight)
    menuHeight = int(MenuHeight / HeightTotal * screenHeight)
    bottomShift = int(BottomShift / HeightTotal * screenHeight)
    textBoxHeight = int(TextBoxHeight / HeightTotal * screenHeight)
    textBoxWidth = int(TextBoxWidth / WidthTotal * screenWidth)
    textBoxVertShift = int((bottomShift - textBoxHeight) / 2)
    textBoxHorzShift = int((screenWidth - textBoxWidth) / 2)
    titleSize = int(TitleSize / HeightTotal * screenHeight)
    titleShift = int( (topShift - titleSize) / 2 )
    balanceSize = int(BalanceSize / HeightTotal * screenHeight)
    balanceHorzShift = int(BalanceShift / WidthTotal * screenWidth)
    balanceVertShift = int( (topShift - balanceSize) / 2 )
    horzShift = int(HorzShift / WidthTotal * screenWidth)

    titleFont = pygame.font.Font(GlobalVar.DefaultShopTitleFontString, titleSize)
    balanceFont = pygame.font.Font(GlobalVar.DefaultShopBalanceFontString, balanceSize)
    titleRect = (horzShift, titleShift)
    balanceRect = (balanceHorzShift, balanceVertShift)

    exitMsg = "Leave the Shops"
    exitRectHeight = int(0.0388 * screenHeight)
    exitRect = GenerateRect(exitMsg)
    exitSize = exitRect[3]

    mainMenu = ShopMenu(GlobalVar.DefaultShopScroller, GlobalVar.BattleFontString, (screenWidth, menuHeight), exitRect, exitMsg)

    mainMenu.ChangeItem(1, "Armour and Weapon Shop", ShopClass.EquipmentGraphics("chestplate", 1))
    mainMenu.ChangeItem(2, "Potion Shop", ShopClass.PotionGraphics("else"))
    mainMenu.ChangeItem(3, "Skill Shop", ShopClass.SkillGraphics())

    tempSurf = mainMenu.DisplayMenu()
    def displayFunction():
        screen.fill(GlobalVar.color.white)
        Title("The Shops")
        screen.blit(tempSurf, (0, topShift))
        mainMenu.DisplayExit(screen)

    GlobalVar.audio.FeedAudio(GlobalVar.ShopMusic)

    pyAnimation.EnterFade(screen, displayFunction, GlobalVar.CentralClock, GlobalVar.GameFPS)

    while True:

        tempSurf = mainMenu.DisplayMenu()
        displayFunction()

        for event in pygame.event.get():
            GlobalVar.Quit(event)
            counter = mainMenu.Scroll(event, (0, topShift))
            if counter == 0:
                return
            elif counter == 1:
                # Armour and Weapon Shop
                ArmourShop(screen, playerInfo)
            elif counter == 2:
                # Potion Shop
                PotionShop(screen, playerInfo)
            elif counter == 3:
                # Skill Shop
                SkillShop(screen, playerInfo)


        GlobalVar.LoopBundle()


def main():

    screen = pygame.display.set_mode((1280, 800))
    menu = ShopMenu(GlobalVar.DefaultShopScroller, GlobalVar.BattleFontString, (1280, 500), (30, 600, 900, 60))
    # Accepted range: 1280 to 400 ~ 500
    menu.ChangeItem(1, "Hikari\n$40000", pygame.image.load("assets/Hikari.png"))
    menu.ChangeItem(2, "Tairitsu\n$60000", pygame.image.load("assets/Tairitsu.png"))
    menu.ChangeItem(3, "Magnificent Tairitsu\n$400000", pygame.image.load("assets/Tairitsu3.jpg"))

    while True:
        screen.fill(GlobalVar.color.white)
        for event in pygame.event.get():
            GlobalVar.Quit(event)
            k = menu.Scroll(event)

        screen.blit(menu.DisplayMenu(), (0, 0))
        menu.DisplayExit(screen)
        pygame.display.update()

if __name__ == "__main__":
    main()