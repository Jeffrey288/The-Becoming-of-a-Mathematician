"""
ATutor.py
"""


import os
import GlobalVar

def a_tutor(playerInfo):
    diff = playerInfo.Beated(False)["bosslevel"] - 1
    beat = playerInfo.Beated(False)["beat"]

    if beat:
        os.startfile(os.path.abspath(GlobalVar.GuidePath))
    else:
        os.startfile(os.path.abspath(GlobalVar.GuideFilename[diff]))

