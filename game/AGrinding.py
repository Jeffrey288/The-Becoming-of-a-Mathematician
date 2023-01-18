"""
AGrinding.py
"""

import Main_Battle as Battle
import pygame
import random
import ABoss
from GlobalVar import *
import pyAnimation

def a_DoGrinding(screen, playerInfo):

    # Difficulty
    diff = playerInfo.Beated(False)["bosslevel"]

    # Counter for the boss
    BattleClass = Battle.AdventureBattle(screen, diff, playerInfo, ABoss.Boss(),
                                         BattleGraphics=DefaultGrindWallpaper)

    pyAnimation.EnterFade(screen, BattleClass.Fade, CentralClock, GameFPS)

    BattleClass.Dialogue("Narrator", "'Practice makes perfect.'\n" +
                                     "You mumbled these words as you bravely approached a stranger, picking them for a fight.")


    # Initiate bossInfo, Pass in boss information
    playerInfoDict = playerInfo.Beated(False)
    if playerInfoDict["beat"]:
        randomDiff = 7
    else:
        randomDiff = diff+3
    bossInfo = ABoss.BossFetch(randomDiff, BossDatabase)
    BattleClass.Reinitialize(bossInfo, randomDiff)

    # Display boss
    BattleClass.BossAppears()
    BattleClass.StartDialogue()

    # Loop for incrementing the boss
    cont = True
    while cont:

        # Battle sequence
        battleResults = BattleClass.Main()

        if battleResults == "escape":
            return
        elif battleResults == "lose":
            return
        elif battleResults == "draw":
            BattleClass.FightContinues()
        elif battleResults == "win":
            # Rewards of previous boss
            BattleClass.EndDialogue()
            BattleClass.Rewards()

            cont = BattleClass.PromptContinue()
            if cont:

                # Pass in new boss info
                if playerInfoDict["beat"]:
                    randomDiff = 7
                else:
                    randomDiff = diff + 3
                print(randomDiff)
                bossInfo = ABoss.BossFetch(randomDiff, BossDatabase)

                BattleClass.Dialogue("Narrator", "You took a short rest before facing your next opponent.")

                BattleClass.Reinitialize(bossInfo, randomDiff, initHP=playerInfo.fullHP())

                # Display boss
                BattleClass.BossAppears()
                BattleClass.StartDialogue()
            else:
                break

def main():
    import pygame
    import APlayer
    screen = pygame.display.set_mode((1280, 800))
    playerInfo = APlayer.LoadSave("TestPlayer.txt")
    a_DoGrinding(screen, playerInfo)

if __name__ == "__main__":
    main()




