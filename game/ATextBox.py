"""
ATextBox.py
"""


import pygame
import pyText
import pyMenu
import pyImage
import pyFloating
from pygame.locals import *
from GlobalVar import *


class TextBox:
    # Constants
    TotalHeight = 0.4
    BoxShift = 0.05 / TotalHeight  # Box Text shift is 0.05 height
    BoxSpacing = 0.02 / TotalHeight  # Box Text spacing is 0.02 height
    TextShift = 0.03  # Distance between special objects and text
    TextSize = 0.03 / TotalHeight
    FloatWidth = 0.07
    FloatHeight = 0.06 / TotalHeight

    SelectionWidth = 1 - 2 * BoxShift

    def __init__(self, size, textBoxFrame=None, menuAlignment="left", nowHeight = 0.4):

        self.height = int(size[1])
        self.width = int(size[0])
        self.menuAlignment = menuAlignment

        # Display Constants
        self.boxShift = int(self.BoxShift * self.height)
        self.horzBoxShift = int(self.boxShift / nowHeight * self.TotalHeight)
        self.boxSpacing = int(self.BoxSpacing * self.height)
        self.textShift = int(self.TextShift * self.width)
        self.textSize = int(self.TextSize * self.height * self.TotalHeight / nowHeight)

        # Floater (The arrow that prompts the player to press Enter)
        self.floatWidth = int(self.FloatWidth * self.width)
        self.floatHeight = int(self.FloatHeight * self.height * self.TotalHeight / nowHeight)
        self.floaterRect = (self.width - self.floatWidth - self.horzBoxShift * 2,
                            self.height - self.floatHeight - self.boxShift)
        self.floater = pyFloating.Floating(FloaterArrow, (self.floatWidth, self.floatHeight), CentralClock)

        # Font
        self.GameFont = pygame.font.Font(GameFont, self.textSize)
        self.GameBoldFont = pygame.font.Font(GameFont, self.textSize)
        self.GameBoldFont.set_bold(True)

        # Selection Menus
        self.selectionHeight = self.textSize
        self.selectionWidth = int(self.SelectionWidth * self.width)
        self.selectionSurface = (self.selectionWidth, self.selectionHeight)

        self.BlitList = []
        self.MenuList = []
        self.TextList = []
        self.counter = 0
        self.menuCounter = 0
        self.Menu = None

        if textBoxFrame == None:
            self.textBoxFrame = pygame.transform.scale(DefaultTextBox, (self.width, self.height))
        else:
            self.textBoxFrame = pygame.transform.scale(textBoxFrame, (self.width, self.height))

    def InsertText(self, text, alignment="left", bold=False, color=(0, 0, 0)):

        lines = pyText.TextWrap(text, self.GameBoldFont if bold else self.GameFont, self.width - self.horzBoxShift * 2)
        for i in lines:
            self.TextList.append([self.counter, i, alignment, bold, color])
            self.counter += 1

    def InsertMenu(self, text, color=(0, 0, 0)):

        self.MenuList.append([self.counter, text, color])
        self.counter += 1
        self.menuCounter += 1
        return self.menuCounter - 1

    def Finalize(self):

        if self.MenuList:
            self.Menu = pyMenu.SelectionMenu(DefaultMenuScroller, self.selectionSurface)

        topCoord = int((self.height - (self.boxSpacing * (self.counter - 1) + self.textSize * self.counter)) / 2)

        for i in self.TextList:
            height = int((self.boxSpacing + self.textSize) * (i[0]))
            if i[3]:
                surf = self.GameBoldFont.render(i[1], 1, i[4])
            else:
                surf = self.GameFont.render(i[1], 1, i[4])

            if i[2] == "left":
                rect = (self.horzBoxShift, topCoord + height)
            elif i[2] == "right":
                rect = (self.width - self.horzBoxShift - surf.get_width(), topCoord + height)
            else:
                rect = (int(self.width - surf.get_width()) / 2,
                        topCoord + height)
            self.BlitList.append((surf, rect))

        if self.MenuList:

            for i in self.MenuList:
                height = int((self.boxSpacing + self.textSize) * (i[0]))
                if self.menuAlignment == "left":
                    rect = (self.horzBoxShift, topCoord + height)
                elif self.menuAlignment == "right":
                    rect = (self.width - self.horzBoxShift - self.selectionWidth - self.selectionHeight,
                            topCoord + height)
                else:
                    rect = (int(self.width - self.selectionWidth - self.selectionHeight) / 2,
                            topCoord + height)
                self.Menu.CreateItem(i[1], self.GameFont, rect)

    def Blit(self):

        tempSurf = self.textBoxFrame.copy()
        for i in self.BlitList:
            tempSurf.blit(i[0], i[1])

        if self.Menu:
            self.Menu.DisplayItem(tempSurf)
        else:
            tempSurf.blit(self.floater.Update(), self.floaterRect)

        return tempSurf

    def Event(self, eventHa, offset = (0, 0)):

        if self.Menu:
            return self.Menu.Scrolling(eventHa, offset)
        else:
            if eventHa.type == KEYDOWN:
                if eventHa.key == K_RETURN:
                    return True
                else:
                    return False

    def Reset(self):

        self.BlitList = []
        self.MenuList = []
        self.TextList = []
        self.counter = 0
        self.Menu = None
        self.menuCounter = 0


class Scene:
    # Constants
    DisplayHeight = 0.6  # Graphics take 40% of the screen height
    BoxHeight = 1 - DisplayHeight

    # Initiator Function
    def __init__(self, screen, textBoxFrame=None, nowHeight = 0.4):

        # Copying Arguments
        self.screen = screen
        self.height = screen.get_height()
        self.width = screen.get_width()

        # Screen planning
        self.displayHeight = int((1-nowHeight) * self.height)
        self.boxHeight = self.height - self.displayHeight

        self.TextBox = TextBox((self.width, self.boxHeight), textBoxFrame, nowHeight = nowHeight)
        self.displayWallpaper = None

    def Display(self):
        self.screen.blit(self.TextBox.Blit(), (0, self.displayHeight))

    def ChangeWallpaper(self, Wallpaper, update = True):

        self.displayWallpaper = pyImage.Wallpaper(pygame.image.load(Wallpaper), self.screen.get_size())
        if update:
            self.Update()

    def Update(self):
        self.screen.blit(self.displayWallpaper, (0, 0))


class PopUp:

    BoxHeight = 0.4
    BoxWidth = 0.5

    # Initiator Function
    def __init__(self, screen, textBoxFrame=None):
        # Copying Arguments
        self.screen = screen
        self.height = screen.get_height()
        self.width = screen.get_width()

        self.boxHeight = int(self.BoxHeight * self.height)
        self.boxWidth = int(self.BoxWidth * self.width)
        self.BoxRect = (int((self.width - self.boxWidth) / 2), int((self.height - self.boxHeight)) / 2)
        self.TextBox = TextBox((self.boxWidth, self.boxHeight), textBoxFrame)

    def Offset(self):
        return self.BoxRect

    def Start(self):
        surf = pygame.Surface((self.screen.get_size()))
        surf.set_alpha(150)
        self.screen.blit(surf, (0, 0))

    def Blit(self):
        self.screen.blit(self.TextBox.Blit(), self.BoxRect)


if __name__ == '__main__':
    s = pygame.display.set_mode((1200 // 2, 800 // 2))
    k = TextBox((1200 // 2, 800 // 2 * 0.4))
    k.InsertText("Fkfdsf")
    k.Finalize()
    while True:

        for event in pygame.event.get():
            Quit(event)

            result = k.Event(event)
            if result:
                print("HAhsdklfhskf")

        s.blit(k.Blit(), (0, 0))
        LoopBundle()