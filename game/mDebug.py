"""
mDebug.py
"""

import json
import GlobalVar
import APlayer
from pygame.locals import *

GLOBALDEBUG = GlobalVar.SettingDict["Debug"]
EASYMODE = GlobalVar.SettingDict["EasyMode"]
DEBUGDAMAGE = 0
RAISECODE = -1

def ReloadPlayer(event):
    if GLOBALDEBUG:
        if event.type == KEYDOWN:
            if event.key == K_F12:
                playerInfo = APlayer.LoadSave(GlobalVar.PlayerDataFileName)
                return playerInfo

def Damage(dmg):

    if DEBUGDAMAGE:
        print(dmg)

def EasyMode(questionObj):

    if EASYMODE:
        return {
            "comment": "Easy Mode.",
            "diffPt": 0,
            "time": 3,
            "question": "Easy Mode: The answer is 1.",
            "answer": 1
        }
    else:
        return questionObj


def RaiseError(e, code = 0):

    if GLOBALDEBUG and RAISECODE != -1:
        if RAISECODE == 0:
            raise e
        elif code == RAISECODE:
            raise e


def SaveState(questionObj, answer, correct, timeUsed):

    if GLOBALDEBUG:

        print(correct, timeUsed, questionObj)

        try:
            file = open(GlobalVar.DebugFile, "r")
            obj = json.loads(file.read())
        except Exception as e:
            obj = {}

        try:
            obj[questionObj["comment"]].append([timeUsed, questionObj, answer, correct])
        except Exception as e:
            obj[questionObj["comment"]] = [timeUsed, questionObj, answer, correct]

        file = open(GlobalVar.DebugFile, "w")
        file.write(json.dumps(obj, indent=4))
        file.close()


def QuestionType(comment):

    if GLOBALDEBUG:
        return "(" + comment + ") "
    else:
        return ""

