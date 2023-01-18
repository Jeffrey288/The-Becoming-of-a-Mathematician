"""
Main_MultiplayerMode.py
"""

import re
import time

import Main_Battle as Battle
import pyMenu
import pygame
import GlobalVar
import pyAnimation
import mMultiplayerBattle
import mMultiplayerServer
import socket
import random

import multiprocessing
multiprocessing.freeze_support()

class ConnectionError(Exception):
    pass


# Tentative IP Test Plan:
"""

a Valid Data (Random)
b Extreme Data
c Illegal Data

OpenServer
1. (a) {Open a server with port 40000}
2. (a) 40000 {Open a server with port 40000}
3. (a) 80 {Open a server with port 80 (non-deterministic, since <1024 is reserved)}
4. (b) 1 {""}
5. (b) 65535 {""}
6. (c) 0, 65536 [Invalid Value] {Message appears}
7. (c) 100000 [Invalid Value] {Message appears}
8. (c) HAHA [Invalid Data Type] {No reaction}

ConnectOptions -> Manual Connection
1-5. (a, b) 192.168.1.74 & Port Number in previous test
{1-5: Connects normally (except for 3, 4)}
6,7. (c) ""
{Invalid Port Number message}
8. (c) HAHA
{Invalid IP Format}
9. (c) 192.168.1.
{Invalid IP Format}
10. (c) 333.333.333.333
{Invalid IP Format}
11. (c) 192.168.1.74192.168.1.74
{Invalid IP Format}
12. (c) 192.168.1.74:40000192.168.1.74:40000
{Invalid IP Format}
13. (c) 192.168.1.74:40000 192.168.1.74:40000
{Connects like 1}
14. (c) 192.168.1.74:40000d 192.168.1.74:40000
{Connects like 1}
15. (c) 192.168.1.74:
{Invalid IP Format}




"""


def m_MultiplayerMode(screen):

    ip_address = socket.gethostbyname(socket.gethostname())
    myPort = GlobalVar.DefaultPort

    serverThread = multiprocessing.Process(target=mMultiplayerServer.mainfunc, args=(ip_address,))

    def OpenServer(screen):

        menu = pyMenu.FrameMenu(screen)

        menu.InsertText("Online Multiplayer Battle", Title=True)
        menu.InsertText("Please enter a port number to open your server on.", Header=True)
        menu.InsertText("(Type nothing to set default.)", Header=True)

        menu.InsertText("", Enter=True)

        input = menu.InsertInput(">> ", inputColor=pyMenu.Color("blue"), Header=True)

        menu.InsertText("", Enter=True)

        failed = False

        confirmed = False
        while not confirmed:
            screen.fill(pygame.Color("white"))
            menu.Blit()
            menu.UpdateCursor()
            for event in pygame.event.get():
                GlobalVar.Quit(event)
                counter = menu.Scrolling(event)
                menu.Typing(event)
                if counter == input:
                    theText = menu.Text()
                    try:
                        portNo = int(theText)
                        if 0 < portNo <= 65535:
                            return portNo
                        else:
                            if not failed:
                                failed = True
                                menu.InsertText("Accepted Range: 0 < Port Number <= 65535", Text=True, color=(255, 0, 0))
                            raise ConnectionError("Invalid Port Number.")
                    except:
                        if not theText:
                            return GlobalVar.DefaultPort
                        else:
                            pass
            GlobalVar.LoopBundle()

    def IPAddress(screenSurf):

        screen = pyMenu.FrameMenu(screenSurf)

        screen.InsertText("Online Multiplayer Battle", Title=True)
        screen.InsertText("Please enter an IP address to connect to.", Header=True)

        screen.InsertText("", Enter=True)

        input = screen.InsertInput(">> ", inputColor=pyMenu.Color("blue"), Header=True)

        screen.InsertText("", Enter=True)

        screen.InitiateMenu()
        rtn = screen.InsertMenu("Return")

        confirmed = False
        while not confirmed:
            screenSurf.fill(pygame.Color("white"))
            screen.Blit()
            screen.UpdateCursor()
            for event in pygame.event.get():
                GlobalVar.Quit(event)
                counter = screen.Scrolling(event)
                screen.Typing(event)
                if counter == rtn:
                    return None
                elif counter == input:
                    try:
                        userInput = screen.Text()
                        if re.fullmatch("\d+\.\d+\.\d+\.\d+:\d+|\d+\.\d+\.\d+\.\d+", userInput):
                            pass
                        else:
                            raise ConnectionError("Invalid IP Format. Format: XX.XX.XX.XX:PortNo."
                                                  " Do not use hostnames.")
                        ipList = re.split(":", userInput)
                        no = re.split('\.', ipList[0])
                        for i in no:
                            if not 0 <= int(i) <= 255:
                                raise ConnectionError("Invalid IP Format. Octets must lie between 0 to 255.")
                        if len(ipList) == 1:
                            ip = ipList[0]
                            port = GlobalVar.DefaultPort
                        elif len(ipList) == 2:
                            ip = ipList[0]
                            port = int(ipList[1])
                            if not 0 < port <= 65535:
                                raise ConnectionError("Invalid Port Number.")
                        return ip, port
                    except ConnectionError as e:
                        raise e
                    except Exception as e:
                        raise ConnectionError("Invalid IP Format: " + str(e))
            GlobalVar.LoopBundle()



    def Name(screen):
        menu = pyMenu.FrameMenu(screen, GlobalVar.CentralClock)

        menu.InsertText("Online Multiplayer Battle", Title=True)
        menu.InsertText("Please enter your name.", Header=True)
        menu.InitiateMenu()

        menu.InsertText("", Enter=True)

        input = menu.InsertInput(">> ", inputColor=pyMenu.Color("blue"), Header=True)

        menu.InsertText("", Enter=True)

        rtn = menu.InsertMenu("Return")

        confirmed = False
        while not confirmed:
            screen.fill(pygame.Color("white"))
            menu.Blit()
            menu.UpdateCursor()
            for event in pygame.event.get():
                GlobalVar.Quit(event)
                counter = menu.Scrolling(event)
                menu.Typing(event)
                if counter == rtn:
                    confirmed = False
                    return
                elif counter == input:
                    if menu.Text():
                        if len(menu.Text()) > 16:
                            return menu.Text()[:16]
                        else:
                            return menu.Text()
                        confirmed = True
            GlobalVar.LoopBundle()

    def ConnectionFailed(screen, e):

        menu = pyMenu.FrameMenu(screen, GlobalVar.CentralClock)

        menu.InsertText("Online Multiplayer Battle", Title=True)
        menu.InsertText("Connection has failed! ", Header=True)
        menu.InsertText("Please check if the server has been turned on at that IP address, ", Text=True)
        menu.InsertText("or if the IP address you entered is valid.", Text=True)

        menu.TextWrap("Error code: " + str(e), Text=True, color=pygame.Color("gray30"))

        menu.InsertText("", Enter=True)

        menu.InitiateMenu()
        menu.InsertMenu("Troubleshoot")
        menu.InsertMenu("Return")

        confirmed = False
        while not confirmed:
            screen.fill(pygame.Color("white"))
            menu.Blit()
            for event in pygame.event.get():
                GlobalVar.Quit(event)
                counter = menu.Scrolling(event)
                if counter == 1:
                    confirmed = True
                    return None
                elif counter == 0:
                    TroubleShoot(screen)

            GlobalVar.LoopBundle()

    def OfflineMulti(screen):

        battle = Battle.OfflineBattle(screen)

        pyAnimation.EnterFade(screen, battle.Fade, GlobalVar.CentralClock, GlobalVar.GameFPS)

        battle.Main()

    def ConnectOption(screen):

        menu = pyMenu.FrameMenu(screen, GlobalVar.CentralClock)

        menu.InsertText("Online Multiplayer Battle", Title=True)
        menu.InsertText("Please select a connection option.", Header=True)

        menu.InsertText("", Enter=True)
        menu.InitiateMenu()

        doAuto = menu.InsertMenu("Open a Server")
        menu.InsertText("Enter the server that you have opened (in the Multiplayer "
                        "Mode menu). It may fail if you enter too soon.",
                        Explanation=True)

        doIp = menu.InsertMenu("Manual Connection")
        menu.InsertText("Manually input an IP address. (Please ensure the server is up and running)", Explanation=True)

        menu.InsertText("", Enter=True)

        rtn = menu.InsertMenu("Return")

        confirmed = False
        while not confirmed:
            screen.fill(pygame.Color("white"))
            menu.Blit()
            for event in pygame.event.get():
                GlobalVar.Quit(event)
                counter = menu.Scrolling(event)
                if counter == rtn:
                    confirmed = False
                    return None
                elif counter == doIp:
                    confirmed = False
                    return IPAddress(screen)
                elif counter == doAuto:
                    confirmed = False
                    return ip_address, myPort

            GlobalVar.LoopBundle()



    def OnlineMulti(screen):

        name = Name(screen)
        if name == None:
            return
        returnList = ConnectOption(screen)
        if not returnList:
            return
        else:
            ip, port = returnList
        m = mMultiplayerBattle.OnlineBattle(screen = screen, IP = ip, port = port, name = name)
        m.Main()

    def TroubleShoot(screen):

        menu = pyMenu.FrameMenu(screen)

        menu.InsertText("Connection Errors", Title=True)

        menu.InsertText("[Errno 10057] ...", Text=True)
        menu.TextWrap("I told you to wait... But if the problem persists, please contact "
                      "the game developer as this is an unsolved issue.", Explanation=True)
        menu.InsertText("", Explanation=True)

        menu.InsertText("[Errno 11004] getaddrinfo failed", Text=True)
        menu.TextWrap("The IP address you have entered is invalid. Please enter IP"
                      + " addresses, not host names (hostnames have nondeterministic behavior).", Explanation=True)
        menu.InsertText("", Explanation=True)

        menu.TextWrap("[WinError 10054] An existing connection was forcibly closed by the remote host", Text=True)
        menu.TextWrap("The server has closed. Consult the server host.", Explanation=True)
        menu.InsertText("", Explanation=True)

        menu.InsertText("Timed out", Text=True)
        menu.TextWrap("It may happen because the connection is bad. "
                      + "If the error repeatedly occurs, please contact the game developer.", Explanation=True)

        menu.InsertText("", Enter=True)

        menu.InitiateMenu()
        menu.InsertMenu("Return")

        confirmed = False
        while not confirmed:

            screen.fill(pygame.Color("white"))
            menu.Blit()
            for e in pygame.event.get():
                counter = menu.Scrolling(e)
                if counter == 0:
                    return
            GlobalVar.LoopBundle()

    # *************************************************************************************************
    # ********************End of subprogram definition***********************************************
    # *************************************************************************************************

    mainMenu = pyMenu.FrameMenu(screen, GlobalVar.CentralClock)

    # Wallpaper
    if random.random() > 0.95:
        mainMenu.AddGraphics(GlobalVar.DefaultMultiplayerWallpaperRare)
    else:
        mainMenu.AddGraphics(GlobalVar.DefaultMultiplayerWallpaper)

    mainMenu.InsertText("Multiplayer Mode", Title = True)

    mainMenu.InitiateMenu()
    mainMenu.InsertMenu("Offline Game")
    mainMenu.InsertMenu("Online Game")
    mainMenu.TextWrap("For insturctions on the online Multiplayer Mode, please read the "
                      "\"Multiplayer Manual\" in the \"Game Settings\" Folder", Text=True)

    mainMenu.InsertText("", Text=True)
    sava = mainMenu.InsertMenu("Open a Server")
    mainMenu.TextWrap("Please wait around 1 minute for the server to start up. "
                      "A message will appear in the console when the server is ready.", Text=True)

    mainMenu.InsertText("", Text=True)
    exi = mainMenu.InsertMenu("Return to Main Menu")

    def displayFunction():

        screen.fill(GlobalVar.color.white)
        mainMenu.Blit()

    displayFunctionSurf = mainMenu.DisplayFunctionSurf()
    def display2Function():
        screen.blit(displayFunctionSurf, (0, 0))

    pyAnimation.EnterFade(screen, display2Function, GlobalVar.CentralClock, GlobalVar.GameFPS)

    exitFlag = False

    while not exitFlag:

        displayFunction()

        for event in pygame.event.get():
            GlobalVar.Quit(event)

            counter = mainMenu.Scrolling(event)

            if counter == 0:
                OfflineMulti(screen)
                GlobalVar.audio.FeedAudio(GlobalVar.MenuMusic)
            elif counter == 1:
                try:
                    OnlineMulti(screen)
                    GlobalVar.audio.FeedAudio(GlobalVar.MenuMusic)
                except Exception as e:
                    ConnectionFailed(screen, e)
            elif counter == sava:
                try:
                    if not serverThread.is_alive():
                        port = OpenServer(screen)
                        myPort = port
                        serverThread = multiprocessing.Process(target=mMultiplayerServer.mainfunc,
                                                               args=(ip_address, port))
                        serverThread.start()
                except:
                    pass
            elif counter == exi:
                exitFlag = True

            if counter not in [None, sava]:
                pyAnimation.FadeOut(screen, GlobalVar.CentralClock, GlobalVar.GameFPS)

        GlobalVar.LoopBundle()

    if serverThread.is_alive():
        try:
            serverThread.terminate()
        except:
            pass


if __name__ == '__main__':

    import warnings

    warnings.filterwarnings('error', message='libpng warning: iCCP: known incorrect sRGB profile.*')

    m_MultiplayerMode(pygame.display.set_mode((int(1280//1.5), int(800//1.5))))
