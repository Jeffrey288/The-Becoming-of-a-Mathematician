"""
pyMenu.py
"""


import pygame
from pygame.locals import *
import pyImage
import pyText
import GlobalVar
import pyInput
import pyMouse


class SelectionMenu:

    def __init__(self, scroller, background, scrollerShift = 3, textShift = 3, alignment = "left", spacing = 0, scrollerSize = -1):

        # Initiate variables
        self.itemList = []
        self.scroller = scroller
        self.scrollerShift = scrollerShift
        self.background = GlobalVar.DefaultMenuBackground
        self.selectedBackground = GlobalVar.DefaultMenuSelectBackground

        self.width = background[0] # x
        self.height = background[1] # y
        self.size = background # size
        self.textShift = textShift
        self.spacing = spacing
        self.alignment = alignment

        if scrollerSize != -1:
            self.scrollerSize = scrollerSize
        else:
            self.scrollerSize = self.height

        # Edit scroller and create scrollerSurf
        self.scroller = pygame.transform.scale(self.scroller, (self.scrollerSize - self.scrollerShift * 2, self.scrollerSize - self.scrollerShift * 2))
        self.scrollerSurf = pygame.Surface((self.scrollerSize, self.scrollerSize), pygame.SRCALPHA)
        self.scrollerRect = self.scroller.get_rect()
        self.scrollerRect.center = (int(self.scrollerSize / 2), int(self.scrollerSize / 2))
        self.scrollerSurf.blit(self.scroller, self.scrollerRect)

        # Initiate counter
        self.counter = 0
        self.selected = -1

    def CreateSurf(self, text, font, position, name = '', color = (0, 0, 0), multiline = False, scrollerPos = "left"):

        # Assign textSurf to text image if image is used instead of text.
        if multiline:
            textList = pyText.TextWrap(text, font, self.width, 0, color)
            textSurf = pyText.TextRender(textList, font, self.spacing, self.alignment, color)
        else:
            textSurf = font.render(text, 1, color)

        tempRect = textSurf.get_rect()
        tempRect.centery = int(self.height / 2)
        if self.alignment == "left":
            tempRect.left = int(self.textShift)
        elif self.alignment == "center":
            tempRect.centerx = int(self.width / 2)
        elif self.alignment == "right":
            tempRect.right = int(self.width - self.textShift)
        else:
            print("Error occurred in CreateItem")

        size = textSurf.get_size()
        tempBg = pygame.Surface(self.size, pygame.SRCALPHA)

        selectedBg = tempBg.copy()
        selectedBg.blit(pygame.transform.scale(self.selectedBackground, size), tempRect)
        tempBg.blit(pygame.transform.scale(self.background, size), tempRect)

        tempBg.blit(textSurf, tempRect)
        selectedBg.blit(textSurf, tempRect)

        tempDict = {}
        if name == '':
            tempDict['name'] = text
        else:
            tempDict['name'] = name
        tempDict['pos'] = position
        tempDict['surface'] = tempBg
        tempDict['selected'] = selectedBg
        tempDict['scrollerPos'] = scrollerPos


        return tempDict

    def CreateItem(self, text, font, position, name='', color=(0, 0, 0), multiline=False, scrollerPos = "left"):

        tempDict = self.CreateSurf(text, font, position, name, color, multiline,scrollerPos)

        self.itemList.append(tempDict)

        return len(self.itemList) - 1

    def ChangeItem(self, index, text, font, position, name='', color=(0, 0, 0), multiline=False, scrollerPos = "left"):

        tempDict = self.CreateSurf(text, font, position, name, color, multiline, scrollerPos)

        try:
            self.itemList[index] = tempDict
        except:
            print("Error occured in SelectionMenu.ChangeItem")

        return len(self.itemList) - 1

    def RemoveItem(self, index):

        try:
            del(self.tempDict[index])
        except:
            print("Error occured in SelectionMenu.RemoveItem")

        return len(self.itemList) - 1

    def ChangePos(self, pos, index = -1, name = ""):

        if index != -1 and not name:
            self.itemList[index]['pos'] = pos
        elif index == -1 and name:
            for i in self.itemList:
                if i["name"] == name:
                    i["pos"] = pos
                    break
        elif index != -1 and self.itemList[index]["name"] == name:
            self.itemList[index]["name"] = pos
        else:
            print("Errored occurred in ChangePos.")

    def ScrollItem(self, direction=1):

        self.counter = (self.counter + direction + len(self.itemList)) % len(self.itemList)
        return self.counter

    def Clicking(self, event, offset = (0, 0)):

        if event.type == MOUSEMOTION:
            for num, i in enumerate(self.itemList):
                if pyMouse.InArea(event, i["pos"], self.size, offset):
                    self.selected = num
                    self.counter = num
                    break
                else:
                    self.selected = -1
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.selected == -1:
                    return None
                else:
                    try:
                        GlobalVar.ButtonClick.play()
                    except:
                        pass
                    return self.selected

    def Scrolling(self, event, offset = (0, 0)):

        if event.type == KEYDOWN:
            if event.key == K_DOWN:
                self.ScrollItem(1)
            elif event.key == K_UP:
                self.ScrollItem(-1)
            elif event.key == K_RETURN:
                try:
                    GlobalVar.ButtonClick.play()
                except:
                    pass
                return self.counter
        return self.Clicking(event, offset)

    def GetSize(self, index=-1, name=""):

        if index != -1 and not name:
            return self.itemList[index]["surface"].get_size()
        elif index == -1 and name:
            for i in self.itemList:
                if i["name"] == name:
                    return i["surface"].get_size()
        elif index != -1 and self.itemList[index]["name"] == name:
            return self.itemList[index]["surface"].get_size()
        else:
            print("Errored occurred in ChangePos.")

    def GetSelected(self):
        return self.selected

    def DisplayItem(self, screen):

        for i in range(len(self.itemList)):
            scrollerPos = self.itemList[i]['scrollerPos']
            if scrollerPos == "below":
                if i == self.counter:
                    screen.blit(self.scrollerSurf, (self.itemList[i]['pos'][0] + int((self.GetSize(index = i)[0] - self.scrollerSize)/2), self.itemList[i]['pos'][1] + self.height))
                pos = self.itemList[i]['pos']
            elif scrollerPos == "above":
                if i == self.counter:
                    screen.blit(self.scrollerSurf, (self.itemList[i]['pos'][0] + int((self.GetSize(index = i)[0] - self.scrollerSize)/2), self.itemList[i]['pos'][1]))
                pos = (self.itemList[i]['pos'][0], self.itemList[i]['pos'][1] + self.scrollerSize)
            elif scrollerPos == "left":
                if i == self.counter:
                    tempRect = self.scrollerSurf.get_rect()
                    tempRect.centery = int(self.height/2)+self.itemList[i]['pos'][1]
                    tempRect.left = self.itemList[i]['pos'][0]
                    screen.blit(self.scrollerSurf, tempRect)
                pos = (self.itemList[i]['pos'][0] + self.scrollerSize, self.itemList[i]['pos'][1])
            elif scrollerPos == "right":
                if i == self.counter:
                    tempRect = self.scrollerSurf.get_rect()
                    tempRect.centery = int(self.height/2)+self.itemList[i]['pos'][1]
                    tempRect.left = self.itemList[i]['pos'][0] + self.GetSize(index = i)[0]
                    screen.blit(self.scrollerSurf, tempRect)
                pos = self.itemList[i]['pos']
            else:
                print("Error occurred in DisplayItem: invalid argument scrollerPos = ", scrollerPos)
            screen.blit(self.itemList[i]['surface'] if self.selected != i else self.itemList[i]['selected'], pos)


    def Debug(self):
        print("No. of Items: ", len(self.itemList))
        for i in range(len(self.itemList)):
            print(f'{i:<5}{self.itemList[i]["name"]:<20}{self.itemList[i]["pos"]}')

    def GetCounter(self):
        return self.counter

    def SetCounter(self, counter):
        self.counter = counter
        return self.counter

class FrameMenu:

    # Originally originated from the making of a_Stats in AMenu

    HeightTotal = 21.0
    WidthTotal = 29.7

    # Text Related
    TopCoord = 2.1 / HeightTotal
    TitleFont = 1.4 / HeightTotal
    HeaderFont = 0.9 / HeightTotal
    SubHeaderFont = 0.75 / HeightTotal
    TextFont = 0.65 / HeightTotal
    ExplanationFont = 0.50 / HeightTotal
    TitleSpacing = 1.6 / HeightTotal
    HeaderSpacing = 0.6 / HeightTotal
    SubHeaderSpacing = 0.4 / HeightTotal
    TextSpacing = 0.30 / HeightTotal
    ExplanationSpacing = 0.20/HeightTotal
    TextHorzShift = 3.2 / WidthTotal

    # Image Related
    GraphicsSize = 9.7 / HeightTotal
    GraphicsVertShift = 5.0 / HeightTotal
    GraphicsHorzShift = 15.4 / WidthTotal

    ScrollerSize = 1.4 / HeightTotal
    MenuTextSize = 1.1 / HeightTotal
    MenuHeight = 1.4 / HeightTotal
    MenuSpacing = 0.3 / HeightTotal
    MenuWidth = 20 / WidthTotal
    MenuTextShift = 0.3 / WidthTotal

    def __init__(self, screen, clock = None):

        self.screen = screen
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()

        self.topCoord = int(self.TopCoord * self.height)
        self.titleFontSize = int(self.TitleFont * self.height)
        self.headerFontSize = int(self.HeaderFont * self.height)
        self.textFontSize = int(self.TextFont * self.height)
        self.explanationFontSize = int(self.ExplanationFont * self.height)
        self.menuTextSize = int(self.MenuTextSize * self.height)
        self.subHeaderFontSize = int(self.HeaderFont * self.height)

        self.titleFont = pygame.font.Font(GlobalVar.DefaultMenuTitleFontString, self.titleFontSize)
        self.headerFont = pygame.font.Font(GlobalVar.DefaultMenuHeaderFontString, self.headerFontSize)
        self.textFont = pygame.font.Font(GlobalVar.DefaultMenuTextFontString, self.textFontSize)
        self.explanationFont = pygame.font.Font(GlobalVar.DefaultMenuExplanationFontString, self.explanationFontSize)
        self.menuFont = pygame.font.Font(GlobalVar.DefaultMenuMenuFontString, self.menuTextSize)
        self.subHeaderFont = pygame.font.Font(GlobalVar.DefaultMenuHeaderFontString, self.subHeaderFontSize)
        self.inputFontString = GlobalVar.DefaultInputFontString

        self.titleSpacing = int(self.TitleSpacing * self.height)
        self.headerSpacing = int(self.HeaderSpacing * self.height)
        self.textSpacing = int(self.TextSpacing * self.height)
        self.subHeaderSpacing = int(self.SubHeaderSpacing * self.height)
        self.explanationSpacing = int(self.ExplanationSpacing * self.height)
        self.textHorzShift = int(self.TextHorzShift * self.width)

        self.menuSpacing = int(self.MenuSpacing * self.width)
        self.scrollerSize = int(self.ScrollerSize * self.height)

        self.menuHeight = int(self.MenuHeight * self.height)
        self.menuWidth = int(self.MenuWidth * self.width)
        self.menuTextShift = int(self.MenuTextShift * self.width)

        self.graphics = None
        self.graphicsSize = int(self.GraphicsSize * self.height)
        self.graphicsHorzShift = int(self.GraphicsHorzShift * self.width)
        self.graphicsVertShift = int(self.GraphicsVertShift * self.height)
        self.graphicsRect = (self.graphicsHorzShift, self.graphicsVertShift)

        self.inputSpacing = self.textSpacing
        self.textWidth = self.graphicsHorzShift - self.textHorzShift

        self.menu = None
        self.input = []
        self.ret = False

        if clock:
            self.clock = clock
        else:
            self.clock = pygame.time.Clock()

        self.blitList = []

        self.tempTop = self.topCoord

    def TextWrap(self, text, Header = False, Title = False, Text = False, Explanation = False, Subheader = False, color = (0, 0, 0), graphics = False):

        if graphics:
            self.textWidth = self.graphicsHorzShift - self.textHorzShift
        else:
            if self.graphics:
                self.textWidth = self.graphicsHorzShift - self.textHorzShift
            else:
                self.textWidth = self.width - self.textHorzShift*2

        if Title:
            font = self.titleFont
        elif Header:
            font = self.headerFont
        elif Text:
            font = self.textFont
        elif Explanation:
            font = self.explanationFont
        elif Subheader:
            font = self.subHeaderFont
        else:
            print("An error has occurred in TextWrap")
            return

        textList = pyText.TextWrap(text, font, self.textWidth)

        for i in textList:
            self.InsertText(i, Header = Header, Text = Text, Explanation = Explanation, Subheader = Subheader, Title = Title, color = color)

    def AddGraphics(self, graphics):

        if graphics:
            if isinstance(graphics, str):
                self.graphics = pygame.image.load(graphics)
            else:
                self.graphics = graphics
            self.graphics = pyImage.ScaleGraphics(self.graphics, self.graphicsSize, False, True)
        else:
            self.graphics = None

    def InitiateMenu(self):

        if self.menu:
            pass
        else:
            myScroller = GlobalVar.DefaultMenuScroller
            myBackground = (self.menuWidth, self.menuHeight)

            self.menu = SelectionMenu(myScroller, myBackground, textShift = self.menuTextShift, scrollerSize = self.scrollerSize)

    def InsertText(self, text, color = (0, 0, 0), Header = False, Text = False, Explanation = False, Title = False, Subheader = False, Enter = False):

        if Title:
            if text:
                tempSurf = self.titleFont.render(text, 1, color)
                self.blitList.append([tempSurf, (self.textHorzShift, self.tempTop)])
            self.tempTop += self.titleFontSize + self.titleSpacing
        elif Header:
            if text:
                tempSurf = self.headerFont.render(text, 1, color)
                self.blitList.append([tempSurf, (self.textHorzShift, self.tempTop)])
            self.tempTop += self.headerFontSize + self.headerSpacing
        elif Text:
            if text:
                tempSurf = self.textFont.render(text, 1, color)
                self.blitList.append([tempSurf, (self.textHorzShift, self.tempTop)])
            self.tempTop += self.textFontSize + self.textSpacing
        elif Explanation:
            if text:
                tempSurf = self.explanationFont.render(text, 1, color)
                self.blitList.append([tempSurf, (self.textHorzShift, self.tempTop)])
            self.tempTop += self.explanationFontSize + self.explanationSpacing
        elif Subheader:
            if text:
                tempSurf = self.subHeaderFont.render(text, 1, color)
                self.blitList.append([tempSurf, (self.textHorzShift, self.tempTop)])
            self.tempTop += self.subHeaderFontSize + self.subHeaderSpacing
        elif Enter:
            self.tempTop += self.titleFontSize + self.textSpacing*2
        else:
            print("An error has occurred in InsertText")

    def InsertMenu(self, text, pos = None):

        if self.menu != None:
            if pos:
                return self.menu.CreateItem(text, self.menuFont, pos)
            else:
                index = self.menu.CreateItem(text, self.menuFont, (self.textHorzShift, self.tempTop))
                self.tempTop += self.menuSpacing + self.menuHeight
                return index
        else:
            print("Menu is not initialized!")

    def Blit(self):

        for surf in self.blitList:
            self.screen.blit(surf[0], surf[1])
        if self.menu:
            self.menu.DisplayItem(self.screen)
        if self.graphics:
            self.screen.blit(self.graphics, (self.graphicsHorzShift, self.graphicsVertShift))
        for input in self.input:
            self.screen.blit(input["textPrompt"], input["textRect"])
            self.screen.blit(input["inputObj"].Surface(), input["inputRect"])

    def Scrolling(self, event):
        if self.input:
            rep = self.menu.Scrolling(event)
            if self.menu.GetSelected() not in [-1, 0]:
                self.ret = True
            elif self.ret and self.menu.GetSelected() == -1:
                self.menu.SetCounter(0)
                self.ret = False
            return rep
        else:
            return self.menu.Scrolling(event)

    def UpdateCursor(self):

        for input in self.input:
            if self.menu.GetCounter() == input["index"]:
                return input["inputObj"].UpdateCursor()

    def Typing(self, event = None):
        for input in self.input:
            if self.menu.GetCounter() == input["index"]:
                return input["inputObj"].Typing(event)

    def Text(self):
        for input in self.input:
            if self.menu.GetCounter() == input["index"]:
                return input["inputObj"].Text()

    def Counter(self):
        return self.menu.GetCounter()

    def InsertInput(self, promptText, promptColor=pygame.Color("Black"),
                    inputColor=pygame.Color("Black"), Header = False, Title = False, Text = False):

        if self.menu != None:
            pass
        else:
            self.InitiateMenu()

        if Header:
            font = self.headerFont
            size = self.headerFontSize
            spacing = self.headerSpacing
        elif Title:
            font = self.titleFont
            size = self.titleFontSize
            spacing = self.titleSpacing
        elif Text:
            font = self.textFont
            size = self.textFontSize
            spacing = self.textSpacing
        else:
            print("Error occured in InsertInput!")
            return

        textPrompt = font.render(promptText, 1, promptColor)
        textRect = (self.textHorzShift, self.tempTop)
        textWidth = textPrompt.get_width()

        inputFont = pygame.font.Font(self.inputFontString, size)
        inputObj = pyInput.TextInput(inputFont,
                                  self.width - self.textHorzShift - 2 * self.inputSpacing - textWidth,
                                  self.clock, inputColor)
        inputRect = (self.textHorzShift + textWidth + self.inputSpacing,
                     self.tempTop)

        index = self.InsertMenu("", (self.width, self.height))

        self.tempTop += size + spacing

        self.input.append(
            {
                "textPrompt": textPrompt,
                "textRect": textRect,
                "inputObj": inputObj,
                "inputRect": inputRect,
                "index": index
            }
        )

        return index

    def DisplayFunctionSurf(self):

        tempSurf = pygame.Surface(self.screen.get_size())
        tempSurf.fill((255, 255, 255))

        tempCopy = FrameMenu(tempSurf)

        tempCopy.graphics = self.graphics
        tempCopy.menu = self.menu
        tempCopy.input = self.input
        tempCopy.blitList = self.blitList

        if self.menu:
            tempCopy.menu.SetCounter(self.menu.GetCounter())

        tempCopy.Blit()

        return tempSurf



if __name__ == "__main__":

    def displayList(list):
        for i in list:
            print(i)
    
    pygame.init()
    pygame.font.init()

    # Screen
    ScreenWidth = int(1280/1.5)
    ScreenHeight = int(960/1.5)
    Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))
    TextShift = 25
    TextHeight = 200

    Screen.fill((241, 43, 32))
    # Test Font
    BasicFont = pygame.font.Font(GlobalVar.DefaultMenuMenuFontString, 20)

    something = pyText.TextWrap("""\u12516\u12531\u12487\u12524Simply put, I hate you.""", BasicFont, ScreenWidth - 2 * TextShift, TextShift)
    displayList(something)
    abcde = pyText.TextRender(something, BasicFont, 10, color = (255,0,0))

    BasicBackground = (100, 40)
    Scroller = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(Scroller, (0, 255, 0), (20, 20), 20)
    menu = SelectionMenu(Scroller, BasicBackground, 6)
    menu.CreateItem("Choice 1", BasicFont, (20, 20), color=(0, 250, 0))
    menu.CreateItem("Choice 2", BasicFont, (20, 70), color=(0, 250, 0))
    menu.CreateItem("Choice 3", BasicFont, (20, 120), color=(0, 250, 0))
    menu.Debug()

    menu.ChangePos((50, 500), name = "Choice 2")

    while True:

        Screen.fill((241, 43, 32))

        for event in pygame.event.get():
            GlobalVar.Quit(event)
            print(menu.Scrolling(event))


        Screen.blit(abcde, (TextShift * 2, ScreenHeight - TextHeight))
        menu.DisplayItem(Screen)
        pygame.display.flip()

    pygame.quit()
