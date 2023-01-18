"""
ABoss.py
"""


import json
import pygame
import mSprite
import mErrors
import random

class Boss:

    __slots__ = "name", "fullHP", "graphics", "sprite", "fullAP", "rewards", "dialogue", "endDialogue"

    def __init__(self, name = "", fullHP = 0, fullAP = 0, graphics = "", rewards = {}, dialogue = [], endDialogue = []):

        self.name = name
        self.fullHP = fullHP
        self.graphics = graphics # str
        self.fullAP = fullAP
        self.rewards = rewards
        self.dialogue = dialogue
        self.endDialogue = endDialogue

    def BossInfo(self):

        tempDict = {}
        tempDict["sprite"] = mSprite.Sprite(self.name, self.fullHP, pygame.image.load(self.graphics)
        if self.graphics else pygame.Surface((1, 1), pygame.SRCALPHA))
        tempDict["fullAP"] = self.fullAP
        tempDict["rewards"] = self.rewards
        tempDict["dialogue"] = self.dialogue
        tempDict["endDialogue"] = self.endDialogue

        return tempDict

def WriteBoss(filename):

    try:
        bossFile = open(filename, 'r')
        bossSomething = json.loads(bossFile.read())
        bossList = bossSomething["Bosses"]
    except:
        bossList = []

    run = True
    while run:

        print("Please input a boss: (Insert name = -1 to end, leave Graphics as blank if no image)")
        diff = int(input(f"{'Difficulty (diff):':30} "))
        if diff == -1:
            run = False
            break
        name = input(f"{'Name (name):':30} ")
        fullHP = int(input(f"{'Full Health (fullHP)':30} "))
        fullAP = int(input(f"{'Full Attack (fullAP)':30} "))
        graphics = input(f"{'Graphics File Path (graphics)':30} ")
        print("Rewards: ")
        exp = int(input(f"{'Experience (exp)':30} "))
        cash = int(input(f"{'Cash (cash)':30} "))

        dialogue = []
        run = True
        while run:
            print("Dialogue (dialogue):")
            speaker = input(f"{'Speaker':30} ")
            if speaker == "-1":
                run = False
                break
            speech = input(f"{'Speech':30} ")
            dialogue.append([speaker, speech])

        endDialogue = []
        run = True
        while run:
            print("End Dialogue (endDialogue):")
            speaker = input(f"{'Speaker':30} ")
            if speaker == "-1":
                run = False
                break
            speech = input(f"{'Speech':30} ")
            endDialogue.append([speaker, speech])


        bossList.append({
            "diff": diff,
            "name": name,
            "fullHP": fullHP,
            "fullAP": fullAP,
            "graphics": graphics,
            "rewards": {
                "exp" : exp,
                "cash": cash
            },
            "dialogue": dialogue,
            "endDialogue": endDialogue
        })

    bossSomething = {"Bosses" : bossList}
    storeStr = json.dumps(bossSomething, indent = 4)

    bossFile = open(filename, 'w')
    bossFile.write(storeStr)

def ReadBoss(filename):

    try:
        bossFile = open(filename, 'r')
        bossJson = json.loads(bossFile.read())
        bossList = bossJson["Bosses"]
    except:
        raise mErrors.BossError
    else:
        BossDict = {}
        for i in range(1, 8):
            BossDict[i] = []
        for i in bossList:
            BossDict[i["diff"]].append(
                # !!!!勝手に何をやっているのだよお前は!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                Boss(i["name"], int(i["fullHP"]*(0.9 if i["name"] != "yandere" else 1)), i["fullAP"], #!!!!!!!!!勝手に!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                     #!!!!!!!!!!!!!!!!!!!変えるなよ!!!!!!!!!!!!!!!!おおおおおおおおおおおおい!!!!!!!!!!!!!!!!
                     i["graphics"],
                     i["rewards"], i["dialogue"], i["endDialogue"])
            )

        return BossDict

def BossFetch(diff, bossDict, index = -1):
    if index != -1:
        return bossDict[diff][int(index)]
    else:
        boss = bossDict[diff][random.randint(0, len(bossDict[diff]) - 1)]
        if boss.name == "yandere":
            if random.random() > 0.10:
                return BossFetch(diff, bossDict, index)
            else:
                return boss
        else:
            return boss


def main():

    # WriteBoss("Bosses.txt")
    ReadBoss("files/Bosses.txt")

if __name__ == "__main__":


    main()
