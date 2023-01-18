"""
mMultiplayerClient.py
"""

import json
import socket
import pickle
import time
import struct

import mMultiplayerObjects
from mMultiplayerPackets import *

DEBUG = False

def Debug(*args):
    if DEBUG:
        print(*args)

class Client:

    def __init__(self, IP, port, name):
        self.timeOutMax = 5
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.playerNo = self.connect(IP, port, name)
        self.client.settimeout(10)
        self.timeOutNo = 0
        self.tempGame = None

    def connect(self, IP, port, name):

        # Problem: in 'Open Server',
        # The server can start, the client can connect, but
        # the client crashes

        # Hypothesis:
        # The server is not prepared to accept connections when
        # the client is connected

        # Solutions:
        # - Place server binding as close to connection as possible
        # - Use exception handling to deal with disconnections

        LargeRetryNo = 0

        connected = False
        while not connected:

            try:

                print("Connecting to: " + IP + ":" + str(port))

                run = True
                RetryNo = 0
                while run:
                    try:
                        self.client.connect_ex((IP, port))
                    except Exception as e:
                        RetryNo += 1
                        if RetryNo > 10:
                            raise e
                    else:
                        run = False
                        break

                Debug("Handshaking: sening name.")
                self.client.send(str.encode(Send(handshaking, name)))
                Debug("Handshaking: sent name.")
                Debug("Handshaking: receiving data.")
                recvData = self.client.recv(4096)
                Debug("Handshaking: received data.")
                List, recvData = Receive(recvData.decode())
                data = List[0][DATA]
                Debug("Handshaking: returning data: ", data)

                return data

            except Exception as e:
                print(e)
                raise e

    def getQuestion(self, diff):
        time.sleep(0.3)

        sendDict = Send(question, diff)

        self.client.send(str.encode(sendDict))

        recvData = self.client.recv(4096)
        List, recvData = Receive(recvData.decode())
        if List[0][TYPE] == question:
            data = List[0][DATA]
            return data
        else:
            self.getQuestion(diff)

    def getStatus(self):

        for i in range(self.timeOutMax):
            try:
                sendDict = Send(get)

                Debug("Get: sending request: ", sendDict)
                self.client.send(str.encode(sendDict))
                Debug("Get: sent request.")

                Debug("Get: receiving data.")
                recvData = self.client.recv(4096)
                Debug("Get: received data.")
                List, recvData = Receive(recvData.decode())
                Debug("Get: unpacking: ", List, recvData)
                if List[0][TYPE] == get:
                    data = List[0][DATA]
                    Debug("Get: returning data: ", data)
                    return data
                else:
                    self.getStatus()
            except Exception as e:
                print("Get: exception: ", e)
                raise e
                time.sleep(0.5)

    def attack(self, diff, resultDict, questionObj):

        reply = mMultiplayerObjects.ResultObj(diff, resultDict, questionObj)
        sendDict = Send(attack, reply)
        self.client.send(str.encode(sendDict))




