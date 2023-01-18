"""
Main_GameSettings.py
"""

import re

def GameSettings(filename):

    try:
        file = open(filename, "r")
    except:
        open(filename, "w")
    else:
        lines = file.readlines()

        settingDict = {
            'Resolution' : "(1200,800)",
            'Unicode' : '1',
            'Debug' : '0',
            'EasyMode' : '0',
            'Music' : '1'
        }

        for line in lines:

            if '#' in line:
                continue
            else:
                line = line.replace(" ", "")
                segments = re.split("[:\n]", line)
                if segments[0] in settingDict.keys():
                    settingDict[segments[0]] = segments[1]

        ResolutionList = re.split("[()\]\[,]", settingDict["Resolution"])
        tempList = []
        for i in ResolutionList:
            if i:
                tempList.append(int(i))
        settingDict["Resolution"] = tempList

        def Set(item):
            settingDict[item] = True if settingDict[item].lower() in ["true", "1"] else False

        Set("Unicode")
        Set('Debug')
        Set('EasyMode')
        Set('Music')
        
        file.close()
        return settingDict
