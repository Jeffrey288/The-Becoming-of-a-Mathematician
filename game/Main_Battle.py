"""
Main_Battle.py
"""

import pygame

import mDebug
import pyText
from mSprite import *
import pyMenu
import pyInput
import pyTimer
from pygame.locals import *
from pyImage import *
import mQuestions
import pyFloating
import random
import math
from GlobalVar import *


pygame.init()
pygame.font.init()


class Battle:

    # Battle is a class because we would like to use
    # inheritance to add sequences and edit the "main" function
    # The implementation for the Adventure Mode grinding,
    # monster battles and multiplayer mode are too similar
    # to not use inheritance with

    # Constants
    BoxShift = 0.05 # Box Text shift is 0.07 height
    BoxSpacing = 0.02 # Box Text spacing is 0.02 height
    DisplayHeight = 0.6 # Graphics take 40% of the screen height
    BoxHeight = 1 - DisplayHeight
    TextShift = 0.03 # Distance between special objects and text
    TextSize = 0.03
    FloatWidth = 0.07
    FloatHeight = 0.06

    SelectionWidth = 0.6


    # Initiator Function
    def __init__(self, screen, diff, playerSprite, oppSprite,
                 displayWallpaper = None,
                 textBoxFrame = None,
                 LightName = False
                 ):

        # Copying Arguments
        self.screen = screen
        self.height = screen.get_height()
        self.width = screen.get_width()
        self.diff = diff

        # Display Constants
        self.boxShift = int(self.BoxShift * self.height)
        self.boxSpacing = int(self.BoxSpacing * self.height)
        self.displayHeight = int(self.DisplayHeight * self.height)
        self.boxHeight = self.height - self.displayHeight
        self.textShift = int(self.TextShift * self.width)
        self.textSize = int(self.TextSize * self.height)

        # Floater (The arrow that prompts the player to press Enter)
        self.floatWidth = int(self.FloatWidth * self.width)
        self.floatHeight = int(self.FloatHeight * self.height)
        self.floaterRect = (self.width - self.floatWidth - self.boxShift * 2,
                              self.height - self.floatHeight - self.boxShift)
        self.floater = pyFloating.Floating(FloaterArrow, (self.floatWidth, self.floatHeight), CentralClock)

        # Fonts
        self.MathFont = pygame.font.Font(MathFont, self.textSize)
        self.MathInputFont = pygame.font.Font(MathInputFont, self.textSize)
        self.BattleFont = pygame.font.Font(BattleFontString, self.textSize)
        self.BoldBattleFont = pygame.font.Font(BattleFontString, self.textSize)
        self.BoldBattleFont.set_bold(True)

        # Game state
        self.playerSprite = playerSprite.copy()
        self.oppSprite = oppSprite.copy()
        self.round = 0
        self.playerBool = True # Whether the player is alive
        self.oppBool = True # Whether the opponent is alive

        # Selection Menus
        self.selectionHeight = self.textSize
        self.selectionWidth = int(self.SelectionWidth * self.width)
        self.selectionSurface = (self.selectionWidth, self.selectionHeight)

        # Display options
        if displayWallpaper == None:
            wallpaper = pygame.image.load(DefaultBattleWallpaper[0])
        else:
            wallpaper = pygame.image.load(displayWallpaper)

        wallpaper = ScaleGraphics(wallpaper, self.height, False, True)
        if wallpaper.get_width() < self.width:
            wallpaper = pygame.transform.scale(wallpaper, (self.width, self.height))
        width = wallpaper.get_width()
        self.displayWallpaper = Crop(wallpaper, (int((width - self.width) / 2), 0), (self.width, self.displayHeight))
        self.textBoxWallpaper = Crop(wallpaper, (int((width - self.width) / 2), self.displayHeight), (self.width, self.boxHeight))

        if textBoxFrame == None:
            battleBox = DefaultBattleBox
            self.textBoxFrame = pygame.transform.scale(battleBox, (self.width, self.boxHeight))
        else:
            self.textBoxFrame = pygame.transform.scale(pygame.image.load(textBoxFrame), (self.width, self.boxHeight))

        self.initSurf = self.FadeSurf()
        self.LightName = LightName

        audio.FeedAudio(BattleMusic[random.randint(0, 2)])

    # Execution Sequence
    def Main(self):
        # Generate a question
        questionObj = mQuestions.QuestionGenerator(self.diff, QuestionDatabase)
        self.RefreshBattle()
        self.DisplayQuestion(questionObj)

        self.RefreshBattle()
        self.DealDamage("player", 2000)
        self.RefreshBattle()
        self.DealDamage("opponent", 300)

    # Main Display Function: Displays the background
    def RefreshBattle(self):

        self.screen.fill(color.white)
        self.screen.blit(self.displayWallpaper, (0, 0))
        if self.textBoxWallpaper != None:
            self.screen.blit(self.textBoxWallpaper, (0, self.displayHeight))
        self.screen.blit(BattleDisplay(self.playerSprite, self.oppSprite,
                      (self.width, self.displayHeight),
                      round = self.round, playerBool = self.playerBool, oppBool = self.oppBool, LightName = self.LightName
                                       ), (0, 0))

    def DisplayTextBox(self):
        
        self.screen.blit(self.textBoxFrame, (0, self.displayHeight))

    def FadeSurf(self):

        tempSurf = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        tempSurf.fill(color.white)
        tempSurf.blit(self.displayWallpaper, (0, 0))
        if self.textBoxWallpaper != None:
            tempSurf.blit(self.textBoxWallpaper, (0, self.displayHeight))
        tempSurf.blit(BattleDisplay(self.playerSprite, self.oppSprite,
                                       (self.width, self.displayHeight),
                                       round=self.round, playerBool=self.playerBool, oppBool=self.oppBool), (0, 0))
        tempSurf.blit(self.textBoxFrame, (0, self.displayHeight))
        return tempSurf

    def Fade(self):

        self.screen.blit(self.initSurf, (0, 0))

    def LoopBundle(self):
        pass

    # Displays floater
    def DisplayFloater(self):
        self.screen.blit(self.floater.Update(), self.floaterRect)

    # The following are sequences in the game.
    # Sequences are in series.

    # DisplayQuestion displays the Q&A part of the sequence
    # and returns "result" and "timeLeft" for damage calculation
    # it is a dictionary
    def DisplayQuestion(self, questionObj):

        # Sequences in parallel
        def Display(stage):

            if stage >= 1:

                # Displays the background
                self.DisplayTextBox()

                # Displays the timer
                topCoord = self.displayHeight + self.boxShift
                timerSurf = timer.Surface()
                self.screen.blit(timerSurf, (self.width - self.boxShift * 2 - timerWidth, topCoord))

                # Display the timeLeft message
                topCoord += int((int(self.textSize * 1.5) - self.textSize) / 2)
                self.screen.blit(timeLeftSurf,
                                 (self.width - self.boxShift * 2 - timerWidth - self.textShift - timeLeftSurf.get_width(),
                                            topCoord))

                # Displays the question label
                topCoord += int((int(self.textSize * 1.5) - self.textSize) / 2)
                self.screen.blit(questionLabel, (self.boxShift, topCoord))

                # Displays the question
                topCoord += self.boxSpacing + self.textSize
                self.screen.blit(questionSurf, (self.boxShift, topCoord))

                # Displays the input box
                topCoord += questionHeight + self.boxSpacing
                self.screen.blit(answerPromptSurf, (self.boxShift, topCoord))
                self.screen.blit(questionInput.Surface(), (self.boxShift + answerPromptSurfWidth + self.textShift, topCoord))

                if stage >= 2:

                    # Displays the results
                    topCoord += answerPromptSurfHeight + self.boxSpacing
                    self.screen.blit(endSurf, (self.boxShift, topCoord))

                    # Displays the Enter arrow
                    self.DisplayFloater()

            LoopBundle()

            pass

        question = questionObj["question"]
        answer = questionObj["answer"]
        time = int(questionObj["time"])

        # Readies the player to answer the question
        startPrompt = pyText.TextRender(
            pyText.TextWrap(
                "You are about to answer a question.\n" + "Time limit : " + str(time) + "\n Press Enter to continue",
                self.BattleFont, int(self.width * 3 / 4)
            ),
            self.BattleFont, self.boxSpacing, "center", color = color.red
        )
        startRect = startPrompt.get_rect()
        startRect.top = self.displayHeight + self.boxShift
        startRect.centerx = int(self.width // 2)

        # Displays the pre-question prompt
        confirmed = False
        while not confirmed:

            if self.LoopBundle():
                break

            self.DisplayTextBox()
            self.screen.blit(startPrompt, startRect)
            self.DisplayFloater()
            pygame.display.update()

            for event in pygame.event.get():
                Quit(event)
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        confirmed = True
                        break

            LoopBundle()

        # Renders the question text
        questionLabel = self.BattleFont.render("Question", 1, color.black)
        questionText = pyText.TextWrap(mDebug.QuestionType(questionObj["comment"]) + question,
                                       self.MathFont, self.width - 2 * self.boxShift)
        questionSurf = pyText.TextRender(questionText, self.MathFont, int(self.boxSpacing//3))
        questionHeight = questionSurf.get_height()

        # Creates answer prompt
        answerPromptSurf = self.BattleFont.render("Input your answer: ", 1, color.black)
        answerPromptSurfWidth = answerPromptSurf.get_width()
        answerPromptSurfHeight = answerPromptSurf.get_height()
        questionInput = pyInput.TextInput(self.MathInputFont,
                                          self.width - 2 * self.boxShift - answerPromptSurfWidth - self.textShift, CentralClock)

        # Creates a timer
        timer = pyTimer.Timer(time, CentralClock, int(self.textSize * 1.5), color=color.red)
        timeLeftSurf = self.BattleFont.render("Time Left:", 1, color.black)
        timerWidth = pygame.font.Font(BattleFontString, int(self.textSize * 1.5)).size("00:00.0")[0]

        # Stage 1: Question Sequence
        while timer.Update() and not questionInput.Typing():
            if self.LoopBundle():
                break
            Display(1)

        # Assigning results
        timeLeft = timer.Time()
        userInput = questionInput.Text()

        # If-else states to determine the end-game message
        if timeLeft == 0:
            result = False
            endMessage = "Time's up!"
        else:
            result = mQuestions.AnswerChecker(answer, userInput)
            if result:
                endMessage = "You are correct!"
            else:
                endMessage = "You are incorrect!"

        endMessage += " Correct Answer: " + (f"{answer:.3g}" if type(answer) == type(1.1) else str(answer))
        endSurf = self.BattleFont.render(endMessage, 1, color.blue)

        # Stage 2: Displaying results
        confirmed = False
        while not confirmed:
            if self.LoopBundle():
                break
            Display(2)

            for event in pygame.event.get():
                Quit(event)
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        confirmed = True

        mDebug.SaveState(questionObj, userInput, result, questionObj["time"] - timeLeft)

        return {
            "result" : result,
            "timeLeft" : timeLeft
                }

    # DealDamage displays the damage dealt.
    # Player deals damage when side = "player"
    # Opponent deals damage when side = "opponent"
    def DealDamage(self, side, damage, dodgeFlag = False):

        # Is the ___ dead?
        # Creates the damage message
        if side == "player":
            self.oppSprite.nowHP -= damage
            if self.oppSprite.nowHP <= 0:
                self.oppSprite.nowHP = 0
                self.oppBool = False
            dmgMessage = pyText.TextWrap(
                "You have" + " dealt " +
                ((str(damage) + " damage") if damage else "no damage") + " on " +
                 self.oppSprite.name +
                (
                    ("\n\n" + (self.oppSprite.name + " has died!"))
                    if not self.oppBool else ""
                ),
                self.BattleFont, int((self.width - 2 * self.boxShift) * 3 / 4)
            )
        elif side == "opponent":
            self.playerSprite.nowHP -= damage
            if self.playerSprite.nowHP <= 0:
                self.playerSprite.nowHP = 0
                self.playerBool = False
            dmgMessage = pyText.TextWrap(
                (
                    "You have dodged the attack from " + self.oppSprite.name + "!\n\n"
                    if dodgeFlag else ""
                ) +
                (self.oppSprite.name + " has") + " dealt " +
                ((str(damage) + " damage") if damage else "no damage") + " on " +
                "You!" +
                (
                    ("\n\n" + "You have died!")
                    if not self.playerBool else ""
                ),
                self.BattleFont, int((self.width - 2 * self.boxShift) * 3 / 4)
            )
        else:
            print("Error occurred in DealDamage!")
    
        # Display the attack damage
        dmgSurf = pyText.TextRender(dmgMessage, self.BattleFont, self.boxSpacing, "center")
        dmgRect = dmgSurf.get_rect()
        dmgRect.center = (int(self.width / 2), self.displayHeight + int(self.boxHeight / 2))

        self.RefreshBattle()

        # Displays
        confirmed = False
        while not confirmed:

            if self.LoopBundle():
                break

            self.DisplayTextBox()
            
            self.screen.blit(dmgSurf, dmgRect)
            self.DisplayFloater()

            LoopBundle()


            for event in pygame.event.get():
                Quit(event)
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        confirmed = True

    # Displays a dialogue
    def Dialogue(self, speaker = None, text = ""):

        nameSurf = self.BoldBattleFont.render(speaker if speaker else self.oppSprite.name, 1, color.blue)

        displaySurf = pyText.TextWrap(text, self.BattleFont, self.width - 2 * self.boxShift)
        displaySurf = pyText.TextRender(displaySurf, self.BattleFont, int(self.boxSpacing * 3 / 4))
        displayRect = displaySurf.get_rect()
        displayRect.left = self.boxShift
        displayRect.bottom = int(self.height - (self.boxHeight - self.boxSpacing - displaySurf.get_height() - self.textSize) / 2)

        confirmed = False
        while not confirmed:

            self.DisplayTextBox()
            self.screen.blit(nameSurf, (self.boxShift, displayRect.top - self.boxSpacing - self.textSize))
            self.screen.blit(displaySurf, displayRect)
            self.DisplayFloater()

            for event in pygame.event.get():
                Quit(event)
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        confirmed = True

            LoopBundle()

    # Asks if the player would like to escape
    def PromptEscape(self):

        # Create Escape Menu
        escapePromptSurf = self.BoldBattleFont.render("Are you sure?", 1, color.blue)

        promptTopCoord = self.displayHeight + int(self.boxHeight / 2) - int(
            3 * (self.textSize + self.boxSpacing) / 2)
        escapeMenu = pyMenu.SelectionMenu(MenuArrow, self.selectionSurface, 0, self.boxSpacing)
        tempTopCoord = promptTopCoord + self.textSize + self.boxSpacing
        escapeMenu.CreateItem("No", self.BattleFont, (self.boxShift, tempTopCoord))
        tempTopCoord += self.textSize + self.boxSpacing
        escapeMenu.CreateItem("Yes", self.BattleFont, (self.boxShift, tempTopCoord))

        # Main Loop
        while True:

            if self.LoopBundle():
                break

            self.DisplayTextBox()
            self.screen.blit(escapePromptSurf, (self.boxShift, promptTopCoord))

            for event in pygame.event.get():
                Quit(event)

                result = escapeMenu.Scrolling(event)

                if result == 0:
                    return False
                elif result == 1:
                    return True

            escapeMenu.DisplayItem(self.screen)
            self.LoopBundle()
            LoopBundle()


class AdventureBattle(Battle):

    def __init__(self, screen, diff, playerInfo, bossInfo, BattleGraphics = None,
                 playerGraphics = None, initHP = -1, round = -1, LightName = False):

        self.playerInfo = playerInfo
        self.bossInfo = bossInfo.BossInfo()
        self.diff = diff

        if playerGraphics == None:
            self.playerGraphics = pygame.image.load(ProfileImage)
        else:
            self.playerGraphics = playerGraphics

        super().__init__(screen,
                         diff,
                         Sprite("You", self.playerInfo.fullHP(), self.playerGraphics, nowHP = initHP),
                         self.bossInfo["sprite"], displayWallpaper=BattleGraphics, LightName = LightName)

        self.round = round

    def StartDialogue(self):

        dialogue = self.bossInfo["dialogue"]
        for line in dialogue:
            self.Dialogue(line[0], line[1])

    def EndDialogue(self):

        dialogue = self.bossInfo["endDialogue"]
        for line in dialogue:
            self.Dialogue(line[0], line[1])

    def Reinitialize(self, bossInfo, diff = -1, round = -1, initHP = -1):
        self.playerBool = True
        self.oppBool = True

        self.bossInfo = bossInfo.BossInfo()
        self.oppSprite = self.bossInfo["sprite"]
        if initHP != -1:
            self.playerSprite.nowHP = initHP
        if diff != -1:
            self.diff = diff
        self.round = round

    def Main(self):

        self.RefreshBattle()
        # Pre-question
        escapeFlag, strengthFlag, defenseFlag = self.PreSelection()
        if escapeFlag:
            return "escape"
        else:
            pass

        # Generate a question
        questionObj = mQuestions.QuestionGenerator(self.diff, QuestionDatabase)
        questionObj = mDebug.EasyMode(questionObj)
        self.TimeDilation(questionObj)

        # Ask the question
        resultDict = self.DisplayQuestion(questionObj)

        # Calculate player AP
        bossDamage = self.CalculatePlayerAP(resultDict = resultDict,
                                            timeLimit = questionObj["time"],
                                            diffPt = questionObj["diffPt"],
                                            strengthFlag = strengthFlag)

        self.DealDamage("player", bossDamage)

        if not self.oppBool:
            return "win"
        else:
            pass

        # Calculate boss AP
        playerDamage = self.CalculateBossAP(diffPt = questionObj["diffPt"],
                                            defenseFlag = defenseFlag)
        self.DealDamage("opponent", playerDamage["damage"], playerDamage["dodgeFlag"])

        if not self.playerBool:
            return "lose"
        else:
            return "draw"

    # Before the player answers the questions, he can
    # choose to escape or drink a potion, dubbed PreSelection
    def PreSelection(self):

        promptSurf = self.BoldBattleFont.render("Choose an action:", 1, color.blue)

        # Create Menu
        promptTopCoord = self.displayHeight + int(self.boxHeight / 2) - int(4 * (self.textSize + self.boxSpacing) / 2)
        mainMenu = pyMenu.SelectionMenu(MenuArrow, self.selectionSurface, 0, self.boxSpacing)
        tempTopCoord = promptTopCoord + self.textSize + self.boxSpacing
        mainMenu.CreateItem("Escape", self.BattleFont, (self.boxShift, tempTopCoord)) # 0
        tempTopCoord += self.textSize + self.boxSpacing
        mainMenu.CreateItem("Potion", self.BattleFont, (self.boxShift, tempTopCoord)) # 1
        tempTopCoord += self.textSize + self.boxSpacing
        mainMenu.CreateItem("Proceed to Question", self.BattleFont, (self.boxShift, tempTopCoord)) # 2

        # Create Potion Warning
        potionWarningDisplayRect = self.boxShift + self.BattleFont.size("Potion")[0] + self.textShift + self.selectionHeight + self.boxSpacing\
            , promptTopCoord + 2*(self.textSize + self.boxSpacing)
        potionWarning = self.BattleFont.render("You have already used a potion!", 1, color.red)

        potionUsed = False
        strengthFlag = False
        defenseFlag = False

        # mainMenu.SetCounter(2)

        # Main Loop
        while True:

            self.DisplayTextBox()
            self.screen.blit(promptSurf, (self.boxShift, promptTopCoord))

            for event in pygame.event.get():
                Quit(event)

                result = mainMenu.Scrolling(event)
                if result == 0:
                    if self.PromptEscape():
                        return True, 0, 0
                    else:
                        pass
                elif result == 1:
                    if potionUsed:
                        pass
                    else:
                        potionUsed, strengthFlag, defenseFlag = self.PromptPotionChoose()
                elif result == 2:
                    return False, strengthFlag, defenseFlag

            if potionUsed:

                self.screen.blit(potionWarning, potionWarningDisplayRect)

            mainMenu.DisplayItem(self.screen)
            LoopBundle()


    # Asks if the player would like to use a potion
    def PromptPotionChoose(self):

        # Create Potion Menu
        potionPromptSurf = self.BoldBattleFont.render("Choose a potion?", 1, color.blue)

        promptTopCoord = self.displayHeight + int(self.boxHeight / 2) - int(5 * (self.textSize + self.boxSpacing) / 2)
        potionInfo = self.playerInfo.Potions({})
        potionMenu = pyMenu.SelectionMenu(MenuArrow, self.selectionSurface, 0, self.boxSpacing)
        tempTopCoord = promptTopCoord + self.textSize + self.boxSpacing
        potionMenu.CreateItem("[Qnty: " + str(potionInfo["regenPot"]) + "] Potion of Regeneration",
                              self.BattleFont, (self.boxShift, tempTopCoord))
        tempTopCoord += self.boxSpacing + self.textSize
        potionMenu.CreateItem("[Qnty: " + str(potionInfo["attackPot"]) + "] Potion of Braveness",
                              self.BattleFont, (self.boxShift, tempTopCoord))
        tempTopCoord += self.boxSpacing + self.textSize
        potionMenu.CreateItem("[Qnty: " + str(potionInfo["defendPot"]) + "] Potion of Perseverance",
                              self.BattleFont, (self.boxShift, tempTopCoord))
        tempTopCoord += self.boxSpacing + self.textSize
        potionMenu.CreateItem("Exit",
                              self.BattleFont, (self.boxShift, tempTopCoord))

        # Main Loop
        while True:

            self.DisplayTextBox()

            for event in pygame.event.get():
                Quit(event)

                self.screen.blit(potionPromptSurf, (self.boxShift, promptTopCoord))

                result = potionMenu.Scrolling(event)
                if result == 0:
                    if potionInfo["regenPot"] > 0:
                        self.playerInfo.Potions({"regenPot" : -1})
                        self.playerSprite.nowHP += int(HealthPotionPerc * self.playerSprite.fullHP)
                        if self.playerSprite.nowHP > self.playerSprite.fullHP:
                            self.playerSprite.nowHP = self.playerSprite.fullHP
                        self.RefreshBattle()
                        return True, False, False
                elif result == 1:
                    if potionInfo["attackPot"] > 0:
                        self.playerInfo.Potions({"attackPot" : -1})
                        return True, True, False
                elif result == 2:
                    if potionInfo["defendPot"] > 0:
                        self.playerInfo.Potions({"defendPot" : -1})
                        return True, False, True
                elif result == 3:
                    return False, False, False

                potionMenu.DisplayItem(self.screen)
                LoopBundle()

    # Calculates the extra time allowed
    def TimeDilation(self, questionObj):

        questionObj["time"] = (self.playerInfo.timePerc() + 1) * questionObj["time"]

    # Calculate how much damage is done to the boss
    def CalculatePlayerAP(self, resultDict, timeLimit, diffPt, strengthFlag):
        if resultDict["result"] == False or resultDict["timeLeft"] == 0:
            return 0
        else:

            # Base damage
            dmg = self.playerInfo.fullAP()
            mDebug.Damage(dmg)

            # Random factor
            dmg *= (0.99 + random.random() * 0.02)
            mDebug.Damage(dmg)

            # Player Perks
            dmg *= 1 + self.playerInfo.swordPerc()
            mDebug.Damage(dmg)

            # Time Left
            dmg *= (1/3) * (resultDict["timeLeft"] / timeLimit + 2)
            mDebug.Damage(dmg)

            # Difficulty Variation
            dmg *= 1 + diffPt
            mDebug.Damage(dmg)

            # Strength Potion
            if strengthFlag:
                dmg *= 1 + AttackPotionPerc
            mDebug.Damage(dmg)

            return math.ceil(dmg)

    # Calculate how much damage is done to the player
    def CalculateBossAP(self, diffPt, defenseFlag):

        # Agility Perk
        if random.random() < self.playerInfo.dodgePerc():

            return {
                "damage" : 0,
                "dodgeFlag" : True
            }

        else:

            # Base damage
            dmg = self.bossInfo["fullAP"]
            mDebug.Damage(dmg)

            # Random factor
            dmg *= 0.99 + random.random() * 0.02
            mDebug.Damage(dmg)

            # Player Perks
            dmg *= 1 - self.playerInfo.chestPerc()
            mDebug.Damage(dmg)
            dmg *= 1 - self.playerInfo.legPerc()
            mDebug.Damage(dmg)
            dmg *= 1 - self.playerInfo.defensePerc()
            mDebug.Damage(dmg)

            # Difficulty Variation
            dmg *= 1 - diffPt
            mDebug.Damage(dmg)

            # Strength Potion
            if defenseFlag:
                dmg *= 1 - DefendPotionPerc


            return {
                "damage": math.ceil(dmg),
                "dodgeFlag": False
            }

    # Displays a dialogue
    def FightContinues(self):
        continueMessageSurf = self.BattleFont.render("The fight continues...", 1, color.blue)
        continueMessageRect = (int((- continueMessageSurf.get_width() + self.width) / 2),
                              self.displayHeight + int((- continueMessageSurf.get_height() + self.boxHeight) / 2))
        confirmed = False
        while not confirmed:

            self.DisplayTextBox()
            self.screen.blit(continueMessageSurf, continueMessageRect)
            self.DisplayFloater()

            for event in pygame.event.get():
                Quit(event)
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        confirmed = True

            LoopBundle()

    # Displays a dialogue
    def BossAppears(self, bossType = "Civilian"):

        self.RefreshBattle()

        bossTypeSurf = self.BoldBattleFont.render(bossType, 1, color.black) if \
            bossType == "Final Boss" else self.BattleFont.render(bossType, 1, color.black)
        hasAppearedSurf = self.BoldBattleFont.render("has appeared!", 1, color.black) if \
            bossType == "Final Boss" else self.BattleFont.render("has appeared!", 1, color.black)
        bossNameSurf = pygame.font.Font(BattleFontString, self.textSize*2).\
            render(self.bossInfo["sprite"].name,
                   1, color.red if bossType == "Final Boss" else color.blue)

        bossNameRect = bossNameSurf.get_rect()
        bossNameRect.center = (int(self.width / 2), self.displayHeight + int(self.boxHeight / 2))

        bossTypeRect = bossTypeSurf.get_rect()
        bossTypeRect.bottom = bossNameRect.top - self.boxSpacing
        bossTypeRect.centerx = int(self.width / 2)

        hasAppearedRect = hasAppearedSurf.get_rect()
        hasAppearedRect.top = bossNameRect.bottom + self.boxSpacing
        hasAppearedRect.centerx = int(self.width / 2)

        confirmed = False
        while not confirmed:

            self.DisplayTextBox()

            self.screen.blit(bossNameSurf, bossNameRect)
            self.screen.blit(bossTypeSurf, bossTypeRect)
            self.screen.blit(hasAppearedSurf, hasAppearedRect)

            self.DisplayFloater()


            for event in pygame.event.get():
                Quit(event)
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        confirmed = True

            LoopBundle()

    # Displays a dialogue (for Grinding)
    def PromptContinue(self):

        msg = "Would you like to continue grinding?"
        msgSurf = self.BattleFont.render(msg, 1, color.blue)

        promptTopCoord = self.displayHeight + int(self.boxHeight / 2) - int(3 * (self.textSize + self.boxSpacing) / 2)
        escapeMenu = pyMenu.SelectionMenu(MenuArrow, self.selectionSurface, 0, self.boxSpacing)
        tempTopCoord = promptTopCoord + self.textSize + self.boxSpacing
        escapeMenu.CreateItem("Yes", self.BattleFont, (self.boxShift, tempTopCoord))
        tempTopCoord += self.textSize + self.boxSpacing
        escapeMenu.CreateItem("No", self.BattleFont, (self.boxShift, tempTopCoord))

        # Main Loop
        while True:

            self.DisplayTextBox()

            for event in pygame.event.get():
                Quit(event)

                self.screen.blit(msgSurf, (self.boxShift, promptTopCoord))
                result = escapeMenu.Scrolling(event)

                if result == 0:
                    return True
                elif result == 1:
                    return False

                escapeMenu.DisplayItem(self.screen)
                LoopBundle()

    # Displays rewards
    def Rewards(self, congratText = False):

        displayText = ""

        if congratText:
            displayText += "Congratulations on defeating ", self.oppSprite.name, ", Level ", str(self.diff) + "!\n"

        expGained = int(self.bossInfo["rewards"]["exp"] * (0.97 + 0.1 * random.random()))
        cashGained = int(self.bossInfo["rewards"]["cash"] * (0.97 + 0.1 * random.random()))
        displayText += "You have earned " + str(expGained) + \
                      " Experience Points and " + str(cashGained) + " Cash."

        expDict = self.playerInfo.Experience(expGained)
        self.playerInfo.Cash(cashGained)

        if expDict["levelUp"]:
            displayText += "\nYou have levelled up to Level " + str(expDict["level"]) + "!"

        displaySurf = pyText.TextWrap(displayText, self.BattleFont, self.width - 2 * self.boxShift)
        displaySurf = pyText.TextRender(displaySurf, self.BattleFont, self.boxSpacing, alignment="center")
        displayRect = displaySurf.get_rect()
        displayRect.center = (int(self.width / 2), int(self.displayHeight + self.boxHeight / 2))

        confirmed = False
        while not confirmed:

            self.DisplayTextBox()
            self.screen.blit(displaySurf, displayRect)
            self.DisplayFloater()

            for event in pygame.event.get():
                Quit(event)
                if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        confirmed = True

            LoopBundle()


class MultiplayerBattle(Battle):

    PlayerHP = PlayerHP
    PlayerAP = AttackDmg
    RandomRange = 0.05
    TimerRange = 1 / 3

    def __init__(self, screen, playerSprite = None, oppSprite = None, BattleGraphics = None, LightName = False):

        if playerSprite:
            self.playerSprite = playerSprite
        else:
            self.playerSprite = Sprite("Player 1", self.PlayerHP, pygame.image.load(ProfileImage))

        if oppSprite:
            self.oppSprite = oppSprite
        else:
            self.oppSprite = Sprite("Player 2", self.PlayerHP, pygame.image.load(Player2Image))

        super().__init__(screen, 1, self.playerSprite, self.oppSprite,
                         displayWallpaper = BattleGraphics, LightName = LightName)

        self.turn = 1

    # Chooses difficulty and returns the difficulty
    def DifficultySelection(self):

        # Create Selection Menu
        diffPromptSurf = self.BoldBattleFont.render("Choose a difficulty.", 1, color.blue)

        promptTopCoord = self.displayHeight + int(self.boxHeight / 2) - int(
            5 * (self.textSize + self.boxSpacing) / 2)

        diffMenu = pyMenu.SelectionMenu(MenuArrow, self.selectionSurface, 0, self.boxSpacing)
        tempTopCoord = promptTopCoord + self.textSize + self.boxSpacing
        diffMenu.CreateItem("(Level 1) Quadratic Equations and Graphs",
                              self.BattleFont, (self.boxShift, tempTopCoord))
        tempTopCoord += self.boxSpacing + self.textSize
        diffMenu.CreateItem("(Level 2) Arithmetic Sequences",
                              self.BattleFont, (self.boxShift, tempTopCoord))
        tempTopCoord += self.boxSpacing + self.textSize
        diffMenu.CreateItem("(Level 3) Geometric Sequence and Polynomials",
                              self.BattleFont, (self.boxShift, tempTopCoord))
        tempTopCoord += self.boxSpacing + self.textSize
        diffMenu.CreateItem("Escape",
                              self.BattleFont, (self.boxShift, tempTopCoord))

        # Main Loop
        while True:

            if self.LoopBundle():
                break

            self.DisplayTextBox()
            self.screen.blit(diffPromptSurf, (self.boxShift, promptTopCoord))

            for event in pygame.event.get():
                Quit(event)

                result = diffMenu.Scrolling(event)
                if result == 0:

                    return 1
                elif result == 1:

                    return 2
                elif result == 2:

                    return 3
                elif result == 3:
                    if self.PromptEscape():
                        return -1

            diffMenu.DisplayItem(self.screen)
            LoopBundle()

    def CalculateAP(self, resultDict, timeLimit, diffPt):

        result = resultDict["result"]
        timeLeft = resultDict["timeLeft"]
        if result and timeLeft:

            dmg = self.PlayerAP[self.diff]

            dmg *= 1 - self.RandomRange / 2 + self.RandomRange * random.random()

            dmg *= (1 - self.TimerRange) + self.TimerRange * timeLeft / timeLimit

            dmg *= 1 + diffPt

            return int(dmg)

        else:
            return 0

    def ChangeRound(self):
        self.turn = 1 if self.turn == 2 else 2


class OfflineBattle(MultiplayerBattle):

    def __init__(self, screen, playerSprite = None, oppSprite = None):

        super().__init__(screen, playerSprite, oppSprite, DefaultMultiOffline)


    def Main(self):

        self.RefreshBattle()

        self.Dialogue("Narrator", "A quarrel between friends does not make them enemies; it's a type of communication. "
                                  + "Go, my dear, and demonstrate your intellect.")

        roundCounter = 0

        run = True
        while run:

            if self.playerBool and self.oppBool:
                if roundCounter:
                    self.ChangeRound()
            else:
                run = False
                winner = self.turn
                break

            self.Dialogue("Narrator", "It is now your turn, " + (self.playerSprite.name if self.turn == 1 else self.oppSprite.name))
            self.diff = self.DifficultySelection()
            if self.diff == -1:
                self.Dialogue("Narrator", (self.playerSprite.name if self.turn == 1 else self.oppSprite.name) + " "
                              + "has abandoned.")
                run = False
                return
            question = mQuestions.QuestionGenerator(self.diff, QuestionDatabase)
            question = mDebug.EasyMode(question)
            resultDict = self.DisplayQuestion(question)
            dmg = self.CalculateAP(resultDict, question["time"], question["diffPt"])
            self.DealDamage("player" if self.turn == 1 else "opponent", dmg)
            roundCounter += 1

        self.Dialogue("Narrator", "Well done, " + (self.playerSprite.name if self.turn == 1 else self.oppSprite.name) + "!\n"
                      + "Now, don't brag just because you won, and don't cry because you lost. It takes time "
                      + "to become a great Mathematician, and I believe both of you can do it!")


# *************************************************************************************************************
# *********  The following are display modules used in the above classes.  ************************************
# *************************************************************************************************************


def BattleDisplay(playerSprite, oppSprite, dim, round = -1, playerBool = True, oppBool = True, NameTagBg = None, LightName = False):

    if LightName:
        color = (255, 249, 224)
    else:
        color = (26, 14, 0)

    if NameTagBg == None:
        NameTagWallpaper = DefaultBattleNameTag
    else:
        NameTagWallpaper = NameTagBg

    # Defining the surface that is going to be returned
    Surf = pygame.Surface(dim, pygame.SRCALPHA)
    height = dim[1]
    width = dim[0]

    # Health bar creation
    # Height : 55
    barHeight = int((55/350) * height)
    barWidth = int((400/900) * width)
    playerBar = HealthBar(playerSprite.fullHP, playerSprite.nowHP, (barWidth, barHeight), "left")
    if oppSprite.fullHP == 0:
        oppBar = pygame.Surface((1, 1), pygame.SRCALPHA)
    else:
        oppBar = HealthBar(oppSprite.fullHP, oppSprite.nowHP, (barWidth, barHeight), "right")

    # Text
    # Height = 31 + 5 * 2 divided by 2
    textHeight = int((30/350) * height)
    playerTag = BattleFont.render(playerSprite.name, 1, color)
    oppTag = BattleFont.render(oppSprite.name, 1, color)
    playerTag = ScaleGraphics(playerTag, textHeight, False, True)
    oppTag = ScaleGraphics(oppTag, textHeight, False, True)
    playerSize = playerTag.get_size()
    oppSize = oppTag.get_size()
    boxVertShift = int((7.5/350) * height)
    boxHorzShift = int((4/900) * width)
    playerName = pygame.transform.scale(NameTagWallpaper, (playerSize[0] + 2 * boxHorzShift, playerSize[1] + 2 * boxVertShift))
    oppName = pygame.transform.scale(NameTagWallpaper, (oppSize[0] + 2 * boxHorzShift, oppSize[1] + 2 * boxVertShift))
    playerName.blit(playerTag, (boxHorzShift, boxVertShift))
    oppName.blit(oppTag, (boxHorzShift, boxVertShift))

    if round > 0:
        roundTag = BattleFont.render("Round: " + str(round) + "/2", 1, color)
        roundTag = ScaleGraphics(roundTag, textHeight, False, True)
        roundSize = roundTag.get_size()
        roundName = pygame.transform.scale(NameTagWallpaper, (roundSize[0] + 2 * boxHorzShift, roundSize[1] + 2 * boxVertShift))
        roundName.blit(roundTag, (boxHorzShift, boxVertShift))
        roundName = ScaleGraphics(roundName, textHeight, False, True)

    # Blitting

    # Health Bars
    # Height : 15
    topCoord = int((15/350) * height)
    HorzShift = int((30/900) * width)
    Surf.blit(playerBar, (HorzShift, topCoord))
    Surf.blit(oppBar, (width - HorzShift - barWidth, topCoord))

    # Name Tag
    # Height : 5
    topCoord += int((5/350) * height) + barHeight
    nameCoord = topCoord

    # Graphics
    topCoord += int((5/350) * height) + int((textHeight + 2 * boxVertShift) / 2)
    graphicsHeight = height - topCoord
    playerGraphics = playerSprite.returnSurface(graphicsHeight)
    oppGraphics = oppSprite.returnSurface(graphicsHeight)
    graphicsShift = HorzShift + int((350/900/2) * width)
    playerRect = playerGraphics.get_rect()
    playerRect.center = (graphicsShift, topCoord + int(graphicsHeight // 2))
    oppRect = oppGraphics.get_rect()
    oppRect.center = (width - graphicsShift, topCoord + int(graphicsHeight // 2))
    if playerBool:
        Surf.blit(playerGraphics, playerRect)
    if oppBool:
        Surf.blit(oppGraphics, oppRect)

    # Name Tag
    Surf.blit(playerName, (HorzShift, nameCoord))
    if oppSprite.name:
        Surf.blit(oppName, (width - HorzShift - oppName.get_width(), nameCoord))
    if round > 0:
        tempRect = roundName.get_rect()
        tempRect.centerx = int(width // 2)
        tempRect.top = nameCoord
        Surf.blit(roundName, tempRect)

    return Surf

def HealthBar(fullHP, playerHP, dim, side): # --> Surface

    height = dim[1]
    width = dim[0]

    # Define a surface and fill in default color/image
    drawSurface = pygame.Surface(dim, pygame.SRCALPHA)

    # Heart blit at (0,0)
    # Health bars blit at height / 2, 0
    # Health bar width is width - height / 2
    # Text blits at height
    heartWidth = int(height // 2)
    barWidth = width - int(height//2)
    barHeight = int(height * 0.8)
    textHeight = int(barHeight * 11 / 13 * 0.65)

    # Correct Dimensions
    drawHeart = pygame.transform.scale(Heart, (height, height))
    drawHealthBg = pygame.transform.scale(HealthBarBackdrop, (barWidth, barHeight))
    drawHealthBar = pygame.transform.scale(HealthBarOverlay, (barWidth, barHeight))
    if side == "right":
        drawHealthBg = pygame.transform.flip(drawHealthBg, True, False)
        drawHealthBar = pygame.transform.flip(drawHealthBar, True, False)

    # Calculate dimensions
    ratio = playerHP / fullHP
    borderWidth = barWidth / 100
    healthWidth = ratio * (barWidth - 2 * borderWidth)
    if side == "left":
        healthStart = (0, 0)
        heartDim = (int(borderWidth + healthWidth), barHeight)
        newBar = Crop(drawHealthBar, healthStart, heartDim)
    else:
        healthStart = (int(barWidth - borderWidth - healthWidth), 0)
        heartDim = (int(borderWidth + healthWidth), barHeight)
        newBar = Crop(drawHealthBar, healthStart, heartDim)


    # Font and text
    text = "Health: " + str(playerHP) + "/" + str(fullHP)
    textSurf = BattleFont.render(text, 1, (35, 16, 5))
    conversionRatio = textHeight/FONTHEIGHT
    textSurf = pygame.transform.scale(textSurf, (int(textSurf.get_width() * conversionRatio), textHeight))

    # Blit the bar on the output surface
    if side == "left":
        drawSurface.blit(drawHealthBg, (heartWidth, int((height - barHeight) // 2)))
        drawSurface.blit(newBar, (heartWidth, int((height - barHeight) // 2)))
        drawSurface.blit(drawHeart, (0, 0))
        drawSurface.blit(textSurf, (int((height) // 2 + barWidth - textSurf.get_width() - 4 * borderWidth), int((height - textSurf.get_height()) // 2)))
    else:
        drawSurface.blit(drawHealthBg, (0, int((height - barHeight) // 2)))
        drawSurface.blit(newBar, (int(barWidth - healthWidth - borderWidth), int((height - barHeight) // 2)))
        drawSurface.blit(drawHeart, (width - height, 0))
        drawSurface.blit(textSurf, (int(4 * borderWidth), int((height - textSurf.get_height()) // 2)))

    return drawSurface



# Note that TestPlayer.txt is used for
# testing player data
def main2():

    import APlayer
    import ABoss

    PlayerInfo = APlayer.LoadSave("TestPlayer.txt")
    BossList = ABoss.ReadBoss("Bosses.txt")
    BossInfo = BossList[1][1]

    screen = pygame.display.set_mode((1280, 800))

    bossBattle = AdventureBattle(screen, 1, PlayerInfo, BossInfo, initHP = 1000)

    bossBattle.Main()

def main1():
    pygame.init()
    pygame.font.init()

    # Hikari = pygame.transform.flip(pygame.image.load("assets/Hikari2.png"), True, False)
    Hikari = pygame.transform.flip(pygame.image.load("assets/JPEG/Hikari2.jpg"), True, False)
    # Tairitsu = pygame.transform.flip(pygame.image.load("assets/Tairitsu2.png"), True, False)
    Tairitsu = pygame.transform.flip(pygame.image.load("assets/JPEG/Tairitsu2.jpg"), True, False)

    kitten = Hikari
    dog = Tairitsu

    playerSprite = Sprite("Kitten", 1000, kitten)
    oppSprite = Sprite("Dog", 10000, dog)

    screen = pygame.display.set_mode((1280, 680))

    '''
    battle = BattleDisplay(playerSprite, oppSprite, (900, 250))
    BattleWallpaperTemp = pygame.transform.scale(BattleWallpaper,(900, 350))
    BattleBoxTemp = pygame.transform.scale(BattleBox, (900, 250))
    '''

    # somethingevennewer = HealthBar(1000, 500, (500, 100), "right")
    # screen.blit(somethingevennewer, (0,0))

    battle = Battle(screen, 1, playerSprite, oppSprite)
    battle.Main()

    k = 1

    while True:

        LoopBundle()

        '''
        screen.blit(BattleBoxTemp, (0, 350))
        screen.blit(BattleWallpaperTemp, (0, 0))
        screen.blit(battle, (0, 0))

        LoopBundle()

        playerSprite.nowHP %= 1000
        playerSprite.nowHP += 10
        oppSprite.nowHP %= 10000
        oppSprite.nowHP += 10
        battle = BattleDisplay(playerSprite, oppSprite, (900, 250), 1000)
        '''

        '''
        k %= 1000
        k += 10
        screen.fill((0,0,0))
        somethingevennewer = HealthBar(1000, k, (500, 100), "left")
        screen.blit(somethingevennewer, (0, 0))
        LoopBundle()
        for i in pygame.event.get():

            pass

        '''

if __name__ == "__main__":
    pass
