"""
mMultiplayerServer.pygame
"""

import json
import socket
import struct
import threading
import mSprite
import pygame
import random

import mQuestions
import mQuestionRead
import pickle
import mMultiplayerObjects
import re
from mMultiplayerPackets import *
import GlobalVar

DEBUG = False

def Debug(*args):
    if DEBUG:
        message(*args)

def message(*args):
    print("Server: ", *args)
    
QuestionDict = mQuestionRead.ReadQuestion("files/Questions.json")

resendMax = 5


timeAllowance = 15
def GetQuestion(diff):

    questionObj = mQuestions.QuestionGenerator(diff, QuestionDict)
    questionObj["time"] = int((questionObj["time"]+timeAllowance)//2)
    return questionObj


def ThreadClient(player, conn, addr, gameID):

    resendCounter = 0
    
    try:

        conn.settimeout(1000)

        handShaking = True
        repos = ""

        run = True
        while run:

            try:

                # Receives new messages
                newStr = conn.recv(4096).decode()
                Debug("Received string:", newStr)

                if newStr:

                    # Appends it into the program buffer
                    repos += newStr
                    Debug("Repository (before):", repos)

                    # Isolate requests from the buffer
                    processList, repos = Receive(repos)
                    Debug("Repository (after):", repos)
                    Debug("Process List:", processList)

                    for i in processList:

                        Debug("Received Request:", i)
                        Debug("Request type:", i[TYPE])

                        if handShaking:

                            if i[TYPE] == handshaking:

                                gameList[gameID].Attendance(player)

                                data = Send(handshaking, str(player))
                                conn.send(str.encode(data))

                                name = i[DATA]
                                message("[Name] " + name)
                                message("=-=-=-=-=-=-=-=-=--=-=-=-=-=-=-=-=" + "\n")

                                if player == 1:
                                    gameList[gameID].p1.name = name
                                elif player == 2:
                                    gameList[gameID].p2.name = name

                                handShaking = False

                        else:

                            if i[TYPE] == get:

                                data = gameList[gameID]
                                sendData = str.encode(Send(get, data))
                                conn.send(sendData)

                            elif i[TYPE] == question:

                                run2 = True
                                while run2:
                                    try:
                                        diff = i[DATA]
                                        data = GetQuestion(diff)
                                        sendData = str.encode(Send(question, data))
                                        conn.send(sendData)
                                    except:
                                        pass
                                    else:
                                        run2 = False

                            elif i[TYPE] == attack:

                                resultDict = i[DATA]
                                gameList[gameID].DealDamage(player, resultDict)

                    gameList[gameID].Update()

                else:
                    run = False
                    break

            except socket.timeout as e:
                message(e)
                resendCounter += 1
                if resendCounter >= resendMax:
                    message("Server:", e)
                    run = False
                    break
            else:
                resendCounter = 0

    except socket.timeout as e:
        message(e)

    finally:
        message(str(addr) + " has lost connection.")
        gameList[gameID].Disconnected(player)
        if gameList[gameID].GameState() == "WAITING":
            global playerNo
            playerNo -= 1
        conn.close()


def mainfunc(ip="", port=""):

    Host = ip
    if port:
        Port = port
    else:
        Port = GlobalVar.DefaultPort


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP)

    global gameList
    gameList = {}

    global playerNo
    playerNo = 0

    def ResourceManagement():

        for g in gameList.keys():
            if gameList[g].GameState() in ["DISCONNECTED", "1WIN", "2WIN"]:
                del g

    gameProcessingThread = threading.Thread(target=ResourceManagement)
    gameProcessingThread.start()

    try:
        server.bind((Host, Port))
    except:
        server.bind((Host, GlobalVar.DefaultPort))


    server.listen(2)
    message("Up n' runnin'!")

    if ip:
        message("Connect to this server by: ", str(ip) + ":" + str(Port))
    else:
        message("Connect to this server by: ", socket.gethostbyname(socket.gethostname()) + ":" + str(Port))
    print()

    while True:

        conn, addr = server.accept()
        message("=-=-=-=-= New Connection =-=-=-=-=")
        message("[IP]", addr)

        gameNo = playerNo // 2
        playerNo += 1
        if playerNo % 2 == 1:
            gameList[gameNo] = mMultiplayerObjects.Game()
        gamePlayerNo = 2 if playerNo % 2 == 0 else 1


        message("[Game] " + str(gameNo))
        message("[Side] " + str(gamePlayerNo))
        message("[Player] " + str(playerNo))

        playerThread = threading.Thread(target=ThreadClient, args=(gamePlayerNo, conn, addr, gameNo))
        playerThread.start()


if __name__ == '__main__':

    ip = input("Input IP (skip for defaults):\n>>> ")
    port = input("Input port number (skip for defaults):\n>>> ")
    mainfunc()
