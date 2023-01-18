"""
APlayer.py
"""

import math
import json

def Initialize():

    return Player({
            "skills" : {
                        "strengthPt" : 0,
                        "defensePt" : 0,
                        "timePt" : 0,
                        "agilityPt" : 0,
                        "healthPt" : 0
                    },
            "equipment" : {
                        "chestplate" : 0,
                        "leggings" : 0,
                        "sword" : 0
                    },
            "potions" : {
                        "regenPot" : 0,
                        "attackPot" : 0,
                        "defendPot" : 0
                    },
            "level" : 1,
            "exp" : 0,
            "skillPt" : 0,
            "bal" : 0,
            "bosslevel" : 1,
            "beat" : False,
        })

def LoadSave(filename):

    try:
        file = open(filename, 'r')
        code = file.read()
        data = json.loads(code)
        return Player(data)
    except:
        print("Save file not found, initializing game with default parameters.")
        return Initialize()

def SaveFile(filename, player):

        file = open(filename, 'w')
        data = player.getDict()
        code = json.dumps(data, indent = 4)
        file.write(code)

class Player:

    SkillIndex = {
        1 : "strengthPt",
        2 : "defensePt",
        3 : "timePt",
        4 : "agilityPt",
        5 : "healthPt"
    }

    SkillName = {
        "strengthPt" : "Strength",
        "defensePt" : "Defense",
        "timePt" : "Time Dilation",
        "agilityPt" : "Agility",
        "healthPt" : "Health"
    }

    Maximum = {
        "skills": {
            "strengthPt": 200,
            "defensePt": 200,
            "timePt": 200,
            "agilityPt": 200,
            "healthPt": 200
        },
        "equipment": {
            "chestplate": 10,
            "leggings": 10,
            "sword": 10
        },
        "potions": {
            "regenPot": 0,
            "attackPot": 0,
            "defendPot": 0
        },
        "level": 101,
        "exp": 0,
        "skillPt": 0,
        "bal": 0,
        "bosslevel": 0,
        "beat": False,

    }

    def __init__(self, data):

        '''
            Reference numbers: (They may or may not be used)

            "skills": {
                "strengthPt": 1,    <- 0
                "defensePt": 1,     <- 1
                "timePt": 1,        <- 2
                "agilityPt": 1,     <- 3
                "healthPt": 1       <- 4
            },
            "equipment": {
                "chestplate": 0,    <- 0
                "leggings": 0,      <- 1
                "sword": 0          <- 2
            },
            "potions": {
                "regenPot": 0,      <- 0
                "attackPot": 0,     <- 1
                "defendPot": 0      <- 2
            },
        '''

        self.skills = data["skills"]
        self.equipment = data["equipment"]
        self.potions = data["potions"]
        self.level = data["level"]
        self.exp = data["exp"]
        self.skillPt = data["skillPt"]
        self.bal = data["bal"]
        self.bosslevel = data["bosslevel"]
        self.beat = data["beat"]

    def Skills(self, increments = {}):

        for skillName in increments.keys():
            self.skills[skillName] += increments[skillName]
        return self.skills

    def Equipment(self, increments = {}):

        for equipmentName in increments.keys():
            self.equipment[equipmentName] += increments[equipmentName]
        return self.equipment

    def Potions(self, increments = {}):

        for potionName in increments.keys():
            self.potions[potionName] += increments[potionName]
        return self.potions

    def Experience(self, increment = 0):

        def expLevel(n):
            return math.ceil(100 / (3 ** 0.04 - 1) * (3 ** ((n-1)/25) - 1))

        def expCumulative(n):
            sum = 0
            for i in range(1, n + 1):
                sum += expLevel(i)
            return sum

        def skillPt(n):
            return math.ceil(7.5 * math.e ** (-(n - 1)/150))

        levelUp = False
        self.exp += increment
        while self.exp >= expCumulative(self.level + 1) and self.level + 1 <= self.Maximum["level"]:
            levelUp = True
            self.level += 1
            self.skillPt += skillPt(self.level)

        tempDict = {}
        tempDict["exp"] = self.exp
        tempDict["level"] = self.level
        tempDict["skillPt"] = self.skillPt
        tempDict["expLevel"] = expCumulative(self.level + 1) if self.level + 1 <= self.Maximum["level"] else 0
        tempDict["expReq"] = expCumulative(self.level + 1) - self.exp if self.level + 1 <= self.Maximum["level"] else 0
        tempDict["levelUp"] = levelUp
        return tempDict

    def SkillPt(self, increment = 0):

        self.skillPt += increment
        return self.skillPt

    def getDict(self):
        return {
            "skills" : self.skills,
            "equipment" : self.equipment,
            "potions" : self.potions,
            "level" : self.level,
            "exp" : self.exp,
            "skillPt" : self.skillPt,
            "bal" : self.bal,
            "bosslevel" : self.bosslevel,
            "beat" : self.beat,
        }


    def Beated(self, increment = False):

        self.bosslevel += 1 if increment else 0
        if self.bosslevel >= 3:
            self.bosslevel = 3

        return {
            "bosslevel" : self.bosslevel,
            "beat" : self.beat
        }

    def Cash(self, increment = 0):
        self.bal += increment
        return self.bal

    def BeatFlag(self):
        self.beat = True

    def fullAP(self):
        return 650 + math.floor(11350 * self.skills["strengthPt"] / 200)
    def fullHP(self):
        return 900 + math.floor(9100 * self.skills["healthPt"] / 200)
    def defensePerc(self):
        return 0.6 * (self.skills["defensePt"] / 200) ** 1.2
    def dodgePerc(self):
        return 0.3 * (self.skills["agilityPt"] / 200)
    def timePerc(self):
        return 2.5 / (1 - math.e ** (-0.76)) * (1 - math.e ** (-0.76 * self.skills["timePt"] / 200))
    def chestPerc(self):
        return 0.3 * self.equipment["chestplate"] / 10
    def legPerc(self):
        return 0.3 * self.equipment["leggings"] / 10
    def swordPerc(self):
        return 0.4 * self.equipment["sword"] / 10


def main():

    myPlayer = LoadSave("TestPlayer.txt")
    myDict = {
            "skills" : {
                        "strengthPt" : myPlayer.skills["strengthPt"],
                        "defensePt" : myPlayer.skills["defensePt"],
                        "timePt" : myPlayer.skills["timePt"],
                        "agilityPt" : myPlayer.skills["agilityPt"],
                        "healthPt" : myPlayer.skills["healthPt"]
                    },
            "skillPerc" : {
                        "strengthPt": myPlayer.fullAP(),
                        "defensePt": myPlayer.defensePerc(),
                        "timePt": myPlayer.timePerc(),
                        "agilityPt": myPlayer.dodgePerc(),
                        "healthPt": myPlayer.fullHP()
                    },
            "equipment" : {
                        "chestplate" : myPlayer.equipment["chestplate"],
                        "leggings" : myPlayer.equipment["leggings"],
                        "sword" : myPlayer.equipment["sword"]
                    },
            "equipmentPerc": {
                        "chestplate": myPlayer.chestPerc(),
                        "leggings": myPlayer.legPerc(),
                        "sword": myPlayer.swordPerc()
                    },
            "potions" : {
                        "regenPot" : myPlayer.potions["regenPot"],
                        "attackPot" : myPlayer.potions["attackPot"],
                        "defendPot" : myPlayer.potions["defendPot"]
                    },
            "level" : myPlayer.level,
            "exp" : myPlayer.exp,
            "skillPt" : myPlayer.skillPt,
            "bal" : myPlayer.bal,
            "bosslevel" : myPlayer.bosslevel,
            "beat" : myPlayer.beat,
        }
    for i in myDict.keys():
        print(myDict[i])

    SaveFile("TestPlayer.txt", myPlayer)

if __name__ == "__main__":
    main()