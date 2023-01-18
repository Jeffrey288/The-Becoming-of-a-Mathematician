'''
Main_AdventureMode.py
'''

import ALoad
import AVillage
import ASequence

def m_AdventureMode(screen):

    playerInfo, tutorialSequence, cont = ALoad.LoadOptions(screen)

    if cont:
        # Tutorial Sequence
        if tutorialSequence:
            ASequence.AdventureModeSequence(screen)

        # Start the game
        AVillage.a_Village(screen, playerInfo, tutorialSequence)


