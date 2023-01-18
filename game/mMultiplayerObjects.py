"""
mMultiplayerObject.py
"""


import mSprite
import pygame
import random
import GlobalVar


class ResultObj:

    __slots__ = "diff", "resultDict", "questionDict"

    def __init__(self, diff, resultDict, questionDict):
        self.diff = diff
        self.resultDict = resultDict
        self.questionDict = questionDict


class Game:

    PlayerHP = GlobalVar.PlayerHP
    PlayerAP = GlobalVar.AttackDmg
    RandomRange = 0.05
    TimerRange = 1 / 3

    def __init__(self):

        self.p1 = mSprite.Sprite("Player 1", self.PlayerHP, None)
        self.p2 = mSprite.Sprite("Player 2", self.PlayerHP, None)
        self.p3 = 0

        self.p1HP = self.PlayerHP
        self.p2HP = self.PlayerHP

        self.p1Ready = False
        self.p2Ready = False

        self.p1Alive = True
        self.p2Alive = True

        self.msg = ""
        self.state = "WAITING"
        # WAITING: waiting for another player to join
        # GAMESTART: the game has started
        # GAME: the game is in progress
        # 1WIN: player 1 has won
        # 2WIN: player 2 has won
        # DISCONNECTED: the other player has disconnected

    def Init(self, p):

        if self.p3 == 0:
            self.p3 = p
        elif self.p3 == 1:
            if p == 2:
                self.p1 = None
                self.p2 = None
        elif self.p3 == 2:
            if p == 1:
                self.p1 = None
                self.p2 = None

    def Attendance(self, p):

        if p == 1:
            self.p1Ready = True
        elif p == 2:
            self.p2Ready = True

    def Disconnected(self, p):
        if self.state == "GAME":
            self.state = "DISCONNECTED"
        else:
            if p == 1:
                self.p1Ready = False
            elif p == 2:
                self.p2Ready = False

    def Update(self):
        if self.state == "GAME":
            if self.p1Alive and self.p2Alive:
                return
            elif self.p1Alive and not self.p2Alive:
                self.state = "1WIN"
            elif not self.p1Alive and self.p2Alive:
                self.state = "2WIN"
        elif self.p1Ready and self.p2Ready and self.state == "WAITING":
            self.state = "GAME"

    def DealDamage(self, player, resultObj):

        diff = resultObj.diff
        resultDict = resultObj.resultDict
        questionObj = resultObj.questionDict
        AP = self.CalculateAP(diff, resultDict, questionObj)
        if AP:
            self.msg = (self.p1.name if player == 1 else self.p2.name) + " has dealt " \
                       + str(AP) + " damage on " + (self.p1.name if player == 2 else self.p2.name) + "."
            if player == 1:
                self.p2HP -= AP
                if self.p2HP <= 0:
                    self.p2HP = 0
                    self.p2Alive = False
            elif player == 2:
                self.p1HP -= AP
                if self.p1HP <= 0:
                    self.p1HP = 0
                    self.p1Alive = False

    def CalculateAP(self, diff, resultDict, questionDict):

        result = resultDict["result"]
        timeLeft = resultDict["timeLeft"]
        diffPt = questionDict["diffPt"]
        timeLimit = questionDict["time"]

        if result and timeLeft:
            dmg = self.PlayerAP[diff]
            dmg *= 1 - self.RandomRange / 2 + self.RandomRange * random.random()
            dmg *= (1 - self.TimerRange) + self.TimerRange * timeLeft / timeLimit
            dmg *= 1 + diffPt
            dmg *= 1 + diffPt
            return int(dmg)
        else:
            return 0

    def GameState(self):
        return self.state


