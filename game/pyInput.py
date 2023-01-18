"""
pyInput.py
"""

import pyText
import pygame
from pygame.locals import *
import GlobalVar

# Comment: one of the biggest disadvantage of pygame (and python) is that
# in game development, engines have to be developed yourself, and it is
# in fact very fustrating and time consuming. Therefore, professional game
# developers choose to use other languages like Java and C, or web
# languages like JavaScript to write games.


'''
class TextInput

TextInput(font, width, clock,
                color = (0,0,0),
                mode = "text",
                initialText = '',
                cursorBlinkTime = 500,
                typeFirstTime = 500,
                typeTime = 50,
                cursorThickness = 1,
                cursorColor = (0, 0, 0)):
Creates a TextInput object.
              
Surface()
Returns the surface of the text input object.

Debug()
Prints the cursor position and the text stored.

Typing()
If placed in a loop, it starts accepting edits from the player.

Text()
Returns the text stored in the text input object.


'''

class TextInput:

    def __init__ (self, font, width, clock,
                  color = (0,0,0),
                  initialText = '',
                  cursorBlinkTime = 500,
                  typeFirstTime = 1000,
                  typeTime = 70,
                  cursorThickness = 1,
                  cursorColor = (0, 0, 0)):

        # Argument assignment
        self.height = font.get_height()
        self.width = width
        self.font = font
        self.textSurface = pygame.Surface((self.width, self.font.get_height()), pygame.SRCALPHA)
        self.color = color

        # Determines if the player can write text anymore
        self.textFlag = True

        # My own clock
        self.clock = clock

        # Text Related
        self.text = initialText
        self.cursorPos = 0   # len(self.text) is maximum

        # Cursor Related
        self.cursorBlinkTime = cursorBlinkTime
        self.cursorClock = 0
        self.showCursor = True

        self.cursorThickness = cursorThickness
        self.cursor = pygame.Surface((self.cursorThickness, self.height))
        self.cursorColor = cursorColor
        self.cursor.fill(cursorColor)

        # Key Repetition
        self.typeFirstTime = typeFirstTime
        self.typeTime = typeTime
        self.typeClock = 0
        self.typeFirst = False
        self.typeHeld = None

    def Surface(self):
        return self.textSurface

    def Text(self):
        return self.text

    def addText(self, char):
        self.text = self.text[:self.cursorPos] + char + self.text[self.cursorPos:]
        self.cursorPos += 1

    def backSpace(self):
        self.text = self.text[:self.cursorPos - 1] + self.text[self.cursorPos:]
        self.cursorPos = max(0, min(self.cursorPos - 1, len(self.text)))

    def delete(self):
        self.text = self.text[:self.cursorPos] + self.text[self.cursorPos + 1:]

    def left(self):
        self.cursorPos = max(0, self.cursorPos - 1)

    def right(self):
        self.cursorPos = min(self.cursorPos + 1, len(self.text))

    def holdTest(self):
        if self.typeHeld == 'backspace':
            self.backSpace()
        elif self.typeHeld == 'delete':
            self.delete()
        elif self.typeHeld == 'left':
            self.left()
        elif self.typeHeld == 'right':
            self.right()
        elif self.textFlag:
            self.addText(self.typeHeld)

    def Debug(self):
        print("cursor:", self.cursorPos)
        print("text:", self.text)

    def EventCheck(self, event):

        if event.type == KEYDOWN:
            if event.key == K_RETURN:
                return True

            elif event.key == K_DELETE:
                self.delete()
                self.typeHeld = "delete"

            elif event.key == K_BACKSPACE:
                self.backSpace()
                self.typeHeld = "backspace"

            elif event.key == K_LEFT:
                self.left()
                self.typeHeld = "left"

            elif event.key == K_RIGHT:
                self.right()
                self.typeHeld = "right"

            else:
                if event.key not in (K_BACKSPACE, K_RETURN, K_TAB, K_CLEAR, \
                                     K_PAUSE, K_ESCAPE, K_DELETE, K_UP, K_DOWN, K_RIGHT, \
                                     K_LEFT, K_INSERT, K_HOME, K_END, \
                                     K_PAGEUP, K_PAGEDOWN, K_RSHIFT, K_LSHIFT, \
                                     K_RCTRL, K_LCTRL, K_RALT, K_LALT):
                    char = event.unicode
                    if self.textFlag:
                        # Adds text
                        self.addText(char)
                        self.typeHeld = char

        elif event.type == KEYUP:
            self.typeFirst = False
            self.typeClock = 0
            self.typeHeld = None

    def UpdateCursor(self):

        self.cursorClock += self.clock.get_time()
        if self.cursorClock > self.cursorBlinkTime:
            self.cursorClock = self.cursorClock % self.cursorBlinkTime
            self.showCursor = not self.showCursor
        self.UpdateScreen()
        self.TypeHeld()

    def UpdateScreen(self):

        self.textSurface = pygame.Surface((self.width, self.font.get_height()), pygame.SRCALPHA)

        posCounter = self.cursorThickness

        if len(self.text) == 0:
            if self.showCursor:
                rect2 = self.cursor.get_rect()
                rect2.centery = int(self.textSurface.get_height() / 2)
                rect2.left = posCounter
                self.textSurface.blit(self.cursor, rect2)
            self.font.set_italic(True)
            self.textSurface.blit(self.font.render("Type Here", 1, pygame.Color("gray")), (posCounter, 0))
            self.font.set_italic(False)

        for counter in range(len(self.text)):
            char = self.text[counter]
            charWidth = self.font.size(char)[0]
            if posCounter + charWidth + self.cursorThickness < self.width:
                self.textSurface.blit(self.font.render(char, 1, self.color), (posCounter, 0))
                posCounter += charWidth
                if counter == self.cursorPos - 1 and self.showCursor:
                    rect2 = self.cursor.get_rect()
                    rect2.centery = int(self.textSurface.get_height() / 2)
                    rect2.left = posCounter
                    self.textSurface.blit(self.cursor, rect2)
                posCounter += self.cursorThickness
            else:
                self.text = self.text[:counter]
                self.cursorPos = min(self.cursorPos, len(self.text))
                break
        if posCounter + self.font.size("M")[0] > self.width:
            self.textFlag = False
        else:
            self.textFlag = True

    def TypeHeld(self):

        try:
            if self.typeHeld != None:
                keys = pygame.key.get_pressed()
                if True not in keys:
                    self.typeHeld = None
        except Exception as e:
            pass

        if self.typeHeld != None:
            self.typeClock += self.clock.get_time()
            if self.typeClock > self.typeFirstTime and self.typeFirst == False:
                self.typeClock = 0
                self.typeFirst = True
                self.holdTest()
            elif self.typeClock > self.typeTime and self.typeFirst:
                self.typeClock %= self.typeTime
                self.holdTest()

    def Typing(self, event = None):

            if event:
                self.EventCheck(event)
                self.UpdateScreen()
            else:
                for event in pygame.event.get():
                    GlobalVar.Quit(event)
                    if self.EventCheck(event):
                        self.UpdateScreen()
                        return True
                self.UpdateScreen()
                self.UpdateCursor()
                self.TypeHeld()







if __name__ == "__main__":
    pass

    pygame.init()
    pygame.font.init()

    # Screen
    ScreenWidth = int(1280 / 1.5)
    ScreenHeight = int(960 / 1.5)
    Screen = pygame.display.set_mode((ScreenWidth, ScreenHeight))

    # Test Font
    BasicFont = pygame.font.Font(GlobalVar.GameFont, 20)

    clock = pygame.time.Clock()
    s = TextInput(BasicFont, 500, clock,  color = (133, 0, 0), cursorColor = (200, 100, 200))

    while True:

        if s.Typing():
            my = s.Text()
            break

        # s.Debug()
        Screen.fill((0,0,0))
        Screen.blit(s.textSurface,(0, 100))
        keys = pygame.key.get_pressed()

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

    print(my)

