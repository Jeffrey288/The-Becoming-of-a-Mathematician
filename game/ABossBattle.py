"""
ABossBattle.py
"""

import Main_Battle as Battle
import pygame
from GlobalVar import *
import pyAnimation
import ATextBox
import ASequence

def a_DoBoss(screen, playerInfo):

    # Difficulty
    diff = playerInfo.Beated(False)["bosslevel"]

    # Counter for the boss
    counter = -1
    battleResults = "win"

    if diff == 3:
        LightName = True
    else:
        LightName = False

    # Initiate bossInfo, Pass in boss information
    bossInfo = ABoss.Boss()
    BattleClass = Battle.AdventureBattle(screen, diff,
                                         playerInfo, bossInfo, BattleGraphics=DefaultBattleWallpaper[diff],
                                         LightName = LightName)

    pyAnimation.EnterFade(screen, BattleClass.Fade, CentralClock, GameFPS)

    BattleClass.Dialogue("Narrator", "You travelled through the world to beat Mathematicians\n" +
                         "Here and now, you will face the man of your dreams.")

    # Loop for incrementing the boss
    while counter <= 2:

        if battleResults == "escape":
            return
        elif battleResults == "lose":
            return
        elif battleResults == "draw":
            BattleClass.FightContinues()
        elif battleResults == "win":
            if counter != -1:
                BattleClass.EndDialogue()
            if counter + 1 <= 1:
                # Increment counter
                counter += 1

                # Pass in new boss info
                bossInfo = BossDatabase[diff][counter]
                BattleClass.Reinitialize(bossInfo, diff = diff + (3 if counter == 1 else 0), round = counter + 1)

                # Display boss
                BattleClass.BossAppears("Final Boss" if counter == 1 else "Mathematician")
                BattleClass.StartDialogue()
            else:
                break

        # Battle sequence
        battleResults = BattleClass.Main()



    # Reads player info
    playerInfoDict = playerInfo.Beated(0)

    # Rewards will not be given if the player has beaten the boss once before
    if playerInfoDict["beat"]:

        # Asks whether the player would like to watch the epilogue again
        popUp = ATextBox.PopUp(screen)
        popUp.TextBox.InsertText("Would you like to watch the Epilogue again?", "center", True)
        nah = popUp.TextBox.InsertMenu("No")
        ya = popUp.TextBox.InsertMenu("Yes")
        popUp.TextBox.Finalize()

        popUp.Start()

        run = True
        while run:

            for event in pygame.event.get():
                Quit(event)
                result = popUp.TextBox.Event(event, popUp.Offset())
                if result == nah:
                    epilogue = False
                    run = False
                elif result == ya:
                    epilogue = True
                    run = False

            popUp.Blit()
            LoopBundle()
    # If the player hasn't beat the boss before
    else:
        BattleClass.Rewards()
        if playerInfoDict["bosslevel"] == 3:
            epilogue = True
        else:
            epilogue = False

    playerInfo.Beated(1)

    # The player has defeated all three bosses
    if epilogue:
        playerInfo.BeatFlag()
        return ASequence.Epilogue(screen)
    else:
        return False

def main():
    import APlayer
    screen = pygame.display.set_mode((1280, 800))
    playerInfo = APlayer.LoadSave("TestPlayer.txt")
    a_DoBoss(screen, playerInfo)

if __name__ == "__main__":
    main()


