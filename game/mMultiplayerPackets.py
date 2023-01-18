"""
mMultiplayerPackets.py
"""


"""
Packet Format:
type
data
"""

import json
import pickle
import base64

handshaking = "HANDSHAKING"
get = "GET"
question = "QUESTION"
attack = "ATTACK"

TYPE = 'type'
DATA = 'data'

def Send(type, data = None):

    sendData = str(base64.b32encode(pickle.dumps(data)))
    sendDict = {TYPE: type,
                DATA: sendData}

    return json.dumps(sendDict)


def Receive(repos):

    counter = 0
    inside = False
    insideString = False
    stringCounter = 0
    returnList = []
    tempIndex = 0

    for index, character in enumerate(repos):

        if character == "{":
            counter += 1
            inside = True
        if character == "}":
            counter -= 1
            if inside and counter == 0:
                inside = False

                jsonDict = json.loads(repos[tempIndex:index+1])

                jsonDict[DATA]= jsonDict[DATA].strip("\'b")
                loadData = bytes(base64.b32decode(jsonDict[DATA]))
                jsonDict[DATA] = pickle.loads(loadData)

                returnList.append(jsonDict)
                tempIndex = index+1

    return returnList, repos[tempIndex:]