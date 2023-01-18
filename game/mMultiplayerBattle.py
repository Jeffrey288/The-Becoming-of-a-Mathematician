"""
mMultiplayerBattle.py
"""

import pygame

import GlobalVar
import Main_Battle as Battle
import mDebug
import mMultiplayerClient
import mQuestions
import pyImage
import pyInput
import pyMenu
import pyText
import pyTimer


class OnlineBattle(Battle.MultiplayerBattle):

    # Display Constants
    DefaultLogFontColor = pygame.Color("darkred")
    GameFPS = 60
    DefaultWaitTime = 3 # seconds
    DefaultPenaltyTime = 10 # seconds
    DefaultPastTime = 3 # seconds
    DefaultStartTime = 5 # seconds

    def __init__(self, screen, IP, port, name):

        self.DefaultPlayer1 = pygame.image.load(GlobalVar.ProfileImage)
        self.DefaultPlayer2 = pygame.image.load(GlobalVar.Player2Image)

        super().__init__(screen, BattleGraphics=GlobalVar.DefaultMultiOnline, LightName = True)

        self.logTextSize = int(self.textSize)
        self.logHeight = self.boxSpacing * 2 + self.logTextSize
        self.logWidth = int(self.width * 5 / 7)
        self.logSpacing = int(self.boxSpacing // 2)
        self.logPos = (int((self.width - self.logWidth) // 2), self.displayHeight - self.logHeight)
        self.logBox = pygame.transform.scale(GlobalVar.DefaultLogBox, (self.logWidth, self.logHeight))
        self.logFont = pygame.font.Font(GlobalVar.BlockyFont, self.logTextSize)
        self.logCenter = (int(self.width // 2), self.displayHeight - self.logSpacing - int(self.logTextSize // 2))

        self.AttackStm = ""

        self.threadGo = True
        self.displayUpdate = True
        self.state = "Game"

        self.run = True

        self.client = mMultiplayerClient.Client(IP, port, name)

        self.p = self.client.playerNo
        self.clock = pygame.time.Clock()

        self.timeOutNo = 0
        self.timeOutMax = 20

    """from memory_profiler import profile
    @profile"""
    def Main(self):

        # filename="logging" + str(self.p), , filemode="w"

        # Opening new client
        client = self.client
        p = self.p

        menu = pyMenu.FrameMenu(self.screen)
        menu.InsertText("Online Multiplayer Battle", Title=True)
        menu.InsertText("Waiting for the game to start...", Header=True)

        menu.InitiateMenu()
        menu.InsertMenu("Return")

        # Waiting for the game to start
        run = True
        while run:
            self.screen.fill(pygame.Color("white"))
            game = client.getStatus()

            if self.PendingStart(menu):
                # The player would like to quit the game.
                return

            # Testing whether the game has started
            if game.GameState() == "GAME":
                run = False
                break

        # The game has started
        # Main: retrieving the game status, terminating whenever necessary
        # Thread: displaying the game
        #   - The battle
        #   - Text box
        #   - Status bar
        # The thread is a daemon thread which will be terminated
        # when run is false. An exception can also be raised.
        # Game has started, reuse previous game
        self.playerSprite = game.p1 if p == "1" else game.p2
        self.playerSprite.graphics = self.DefaultPlayer1
        self.oppSprite = game.p2 if p == "1" else game.p1
        self.oppSprite.graphics = self.DefaultPlayer2

        self.Update(game, p)

        self.GameStart()

        self.Battling(client)
        self.counter = 0

        self.Result()

        return

    def Battling(self, client):

        # Normal procedure
        while self.run:
            diff = self.DifficultySelection()

            if diff == -1:
                self.run = False
                return

            if not self.run:
                return

            self.threadGo = False
            questionObj = client.getQuestion(diff)
            self.threadGo = True

            if not self.run:
                return

            self.threadGo = True
            resultDict = self.DisplayQuestion(questionObj)

            if not self.run:
                return

            self.threadGo = False
            client.attack(diff, resultDict, questionObj)
            self.threadGo = True

            if not(resultDict["timeLeft"] and resultDict["result"]):
                self.Penalty()

            if not self.run:
                return

    def Result(self):

        self.counter += 1
        self.counter %= 10
        if self.counter == 0:
            self.Monitor(self.client, self.p)
        self.Update(self.client.getStatus(), self.p)
        self.displayUpdate = True
        self.DisplayTextBox()

        if self.state == "Won":
            self.Dialogue("Narrator", "The Battle has ended. \n Congratulations! You have won!")
        elif self.state == "Lost":
            self.Dialogue("Narrator", "The Battle has ended. \n You have lost. Try harder next time!")
        elif self.state == "Disconnected":
            self.Dialogue("Narrator", "Your opponent has disconnected.")

    def LoopBundle(self):

        try:
            self.Monitor(self.client, self.p)
        except Exception as e:
            print(e)
            self.timeOutNo += 1
            if self.timeOutNo >= self.timeOutNo:
                raise e

        self.clock.tick(self.GameFPS)
        pygame.display.update()
        if not self.run:
            return True

    def Monitor(self, client, p):
        if self.threadGo:

            game = client.getStatus()
            tempState = game.GameState()
            self.Update(game, p)

            if tempState == "GAME":
                state = "Game"
            elif tempState == "1WIN":
                if p == "1":
                    state = "Won"
                elif p == "2":
                    state = "Lost"
                else:
                    state = "Disconnected"
            elif tempState == "2WIN":
                if p == "1":
                    state = "Lost"
                elif p == "2":
                    state = "Won"
                else:
                    state = "Disconnected"
            elif tempState == "DISCONNECTED":
                state = "Disconnected"
            else:
                state = "Disconnected"

        self.state = state
        if self.state != "Game":
            self.run = False

    def Update(self, game, p):

        if self.playerSprite.name == "Player 1" or self.oppSprite.name == "Player 2":
            self.playerSprite.name = game.p1.name if p == "1" else game.p2.name
            self.oppSprite.name = game.p2.name if p == "1" else game.p1.name

        if self.playerSprite.nowHP != game.p1HP if p == "1" or p == 1 else game.p2HP:
            self.displayUpdate = True
        elif self.oppSprite.nowHP != game.p2HP if p == "1" or p == 1 else game.p1HP:
            self.displayUpdate = True

        self.playerSprite.nowHP = game.p1HP if p == "1" or p == 1 else game.p2HP
        self.oppSprite.nowHP = game.p2HP if p == "1" or p == 1 else game.p1HP

        self.AttackStm = game.msg

    def DisplayTextBox(self):

        if self.displayUpdate:
            self.RefreshBattle()
            self.displayUpdate = False
        super().DisplayTextBox()
        self.DisplayLogBox()

    def PendingStart(self, menu):

        menu.Blit()

        for event in pygame.event.get():
            GlobalVar.Quit(event)
            counter = menu.Scrolling(event)
            if counter == 0:
                return True

        self.clock.tick(self.GameFPS)
        pygame.display.update()


    def DisplayLogBox(self):

        self.screen.blit(self.logBox, self.logPos)

        textSurf = self.logFont.render(self.AttackStm, 1, self.DefaultLogFontColor)

        if textSurf.get_width() >= self.logWidth - self.logSpacing * 2:
            textSurf = pyImage.ScaleGraphics(textSurf, self.logWidth - self.logSpacing * 2, True, False)

        textRect = textSurf.get_rect()
        textRect.center = self.logCenter
        self.screen.blit(textSurf, textRect)


    def GameStart(self):

        startPrompt = pyText.TextRender(
            pyText.TextWrap(
                "The game is starting in:",
                self.BattleFont, int(self.width * 3 / 4)
            ),
            self.BattleFont, self.boxSpacing, "center", color=pygame.Color("darkred")
        )

        startRect = startPrompt.get_rect()
        startRect.top = self.displayHeight + self.boxShift
        startRect.centerx = int(self.width // 2)

        timer = pyTimer.Timer(self.DefaultStartTime, self.clock, int(self.textSize * 3), color=pygame.Color("red"))
        timerRect = timer.Surface().get_rect()
        timerRect.top = self.displayHeight + self.boxShift + startPrompt.get_height() + self.textShift
        timerRect.centerx = int(self.width // 2)

        # Displays the pre-question prompt
        while timer.Update():

            if self.LoopBundle():
                break

            self.DisplayTextBox()
            self.screen.blit(startPrompt, startRect)
            self.screen.blit(timer.Surface(), timerRect)
            pygame.display.update()

            for event in pygame.event.get():
                GlobalVar.Quit(event)

    def Penalty(self):

        # Penalty
        startPrompt = pyText.TextRender(
            pyText.TextWrap(
                "Penalty (" + str(self.DefaultPenaltyTime) + " seconds)\n Ending in:",
                self.BattleFont, int(self.width * 3 / 4)
            ),
            self.BattleFont, self.boxSpacing, "center", color=pygame.Color("darkred")
        )

        startRect = startPrompt.get_rect()
        startRect.top = self.displayHeight + self.boxShift
        startRect.centerx = int(self.width // 2)

        timer = pyTimer.Timer(self.DefaultPenaltyTime, self.clock, int(self.textSize * 3), color=pygame.Color("red"))
        timerRect = timer.Surface().get_rect()
        timerRect.top = self.displayHeight + self.boxShift + startPrompt.get_height() + self.textShift
        timerRect.centerx = int(self.width // 2)

        # Displays the pre-question prompt
        while timer.Update():

            if self.LoopBundle():
                break

            self.DisplayTextBox()
            self.screen.blit(startPrompt, startRect)
            self.screen.blit(timer.Surface(), timerRect)
            pygame.display.update()

            for event in pygame.event.get():
                GlobalVar.Quit(event)

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
                                 (self.width - self.boxShift * 2 - timerWidth - self.textShift -
                                  timeLeftSurf.get_width(), topCoord))

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

            self.LoopBundle()

            pass

        questionObj = mDebug.EasyMode(questionObj)
        question = questionObj["question"]
        answer = questionObj["answer"]
        time = int(questionObj["time"])

        # Readies the player to answer the question
        startPrompt = pyText.TextRender(
            pyText.TextWrap(
                "You are about to answer a question.\n" + "Time limit : " + str(time)
                + "\n The question will be shown in:",
                self.BattleFont, int(self.width * 3 / 4)
            ),
            self.BattleFont, self.boxSpacing, "center", color=pygame.Color("darkred")
        )

        startRect = startPrompt.get_rect()
        startRect.top = self.displayHeight + self.boxShift
        startRect.centerx = int(self.width // 2)

        timerA = pyTimer.Timer(self.DefaultWaitTime, self.clock, int(self.textSize * 3), color=pygame.Color("red"))
        timerRect = timerA.Surface().get_rect()
        timerRect.top = self.displayHeight + self.boxShift + startPrompt.get_height() + self.textShift
        timerRect.centerx = int(self.width // 2)

        # Displays the pre-question prompt
        while timerA.Update():

            if self.LoopBundle():
                break

            self.DisplayTextBox()
            self.screen.blit(startPrompt, startRect)
            self.screen.blit(timerA.Surface(), timerRect)
            pygame.display.update()

            for event in pygame.event.get():
                GlobalVar.Quit(event)

        del timerA

        # Renders the question text
        questionLabel = self.BattleFont.render("Question", 1, pygame.Color("black"))
        questionText = pyText.TextWrap(mDebug.QuestionType(questionObj["comment"]) + question,
                                       self.MathFont, self.width - 2 * self.boxShift)
        questionSurf = pyText.TextRender(questionText, self.MathFont, int(self.boxSpacing//3))
        questionHeight = questionSurf.get_height()

        # Creates answer prompt
        answerPromptSurf = self.BattleFont.render("Input your answer: ", 1, pygame.Color("black"))
        answerPromptSurfWidth = answerPromptSurf.get_width()
        answerPromptSurfHeight = answerPromptSurf.get_height()
        questionInput = pyInput.TextInput(self.MathInputFont,
                                          self.width - 2 * self.boxShift -
                                          answerPromptSurfWidth - self.textShift, self.clock)

        # Creates a timer
        timer = pyTimer.Timer(time, self.clock, int(self.textSize * 1.5), color=pygame.Color("red"))
        timeLeftSurf = self.BattleFont.render("Time Left:", 1, pygame.Color("black"))
        timerWidth = pygame.font.Font(GlobalVar.BlockyFont, int(self.textSize * 1.5)).size("00:00.0")[0]

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

        endMessage += " Correct Answer: " + (f"{answer:.3g}" if type(answer) == type(1.1) else str(answer)) \
                      + "     ... (Wait for " + str(self.DefaultPastTime) + " seconds)"
        endSurf = self.BattleFont.render(endMessage, 1, pygame.Color("dodgerblue4"))

        timerB = pyTimer.BgTimer(self.DefaultPastTime, self.clock)

        # Stage 2: Displaying results
        while timerB.Update():

            if self.LoopBundle():
                break
            Display(2)

            for event in pygame.event.get():
                GlobalVar.Quit(event)

        mDebug.SaveState(questionObj, userInput, result, timeLeft)

        return {
            "result" : result,
            "timeLeft" : timeLeft
                }





