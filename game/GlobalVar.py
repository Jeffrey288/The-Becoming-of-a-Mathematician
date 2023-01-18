"""
GlobalVar.pyaudio
"""

from pygame.locals import *

import pygame

import Main_GameSettings as GameSettings
import mQuestionRead
import time
import ABoss

import sys


bool = False
def Debug(msg):
    if bool:
        print(msg)
        time.sleep(0.5)

pygame.font.init()

GameFPS = 60

# Player Profile Picture
try:
    k = pygame.image.load("Game Settings/ProfilePicture.png")
    del k
except:
    try:
        k = pygame.image.load("Game Settings/ProfilePicture.jpg")
        del k
    except:
        ProfileImage = "assets/PlayerImage/ProfilePicture.png"
    else:
        ProfileImage = "Game Settings/ProfilePicture.jpg"
else:
    ProfileImage = "Game Settings/ProfilePicture.png"

Player2Image = "assets/PlayerImage/Player2Picture.png"

# Essentials
DefaultTextBox = pygame.image.load("assets/BattleImage/BattleTextBox.png")

# Wallpapers
DefaultVillageWallpaper = "assets/Wallpapers/VillageWallpaper.png"
DefaultMultiplayerWallpaper = "assets/Wallpapers/MultiplayerWallpaper.png"
DefaultMultiplayerWallpaperRare = "assets/Wallpapers/MultiplayerWallpaper_Rare.png"

DefaultBattleWallpaper = {
    0: "assets/BattleImage/BattleFault.jpg",
    1: "assets/BattleImage/BattleOne.jpg",
    2: "assets/BattleImage/BattleTwo.jpg",
    3: "assets/BattleImage/BattleThree.jpg"
}

DefaultGrindWallpaper = "assets/BattleImage/BattleGrind.jpg"
DefaultMultiOnline = "assets/BattleImage/BattleMultiOnline.jpg"
DefaultMultiOffline = "assets/BattleImage/BattleMultiOffline.jpg"

# Battle Related
DefaultBattleBox = DefaultTextBox
DefaultBattleNameTagStr = "assets/BattleImage/BattleNameTag.png"
DefaultBattleNameTag = pygame.image.load(DefaultBattleNameTagStr)

# Health Bar (Images are loaded in as surfaces as they are small enough.)
HeartStr = "assets/HealthBarImage/Heart.png"
HealthBarBackdropStr = "assets/HealthBarImage/HealthBarGrayed.png"
HealthBarOverlayStr = "assets/HealthBarImage/HealthBarEnlarged.png"

Heart = pygame.image.load(HeartStr)
HealthBarBackdrop = pygame.image.load(HealthBarBackdropStr)
HealthBarOverlay = pygame.image.load(HealthBarOverlayStr)

# Shop
DefaultChestplate = "assets/ShopImage/Chestplate.png"
DefaultLeggings = "assets/ShopImage/Leggings.png"
DefaultSword = "assets/ShopImage/Sword.png"
DefaultShirt = "assets/ShopImage/Shirt.png"
DefaultTrunks = "assets/ShopImage/Trunks.png"
DefaultTwig = "assets/ShopImage/Twig.png"
DefaultPotion1 = "assets/ShopImage/Potion1.png"
DefaultPotion2 = "assets/ShopImage/Potion2.png"
DefaultPotion3 = "assets/ShopImage/Potion3.png"
DefaultPotion4 = "assets/ShopImage/Potion4.png"

DefaultSkills = "assets/ShopImage/Skills.png"

DefaultShopTextboxWallpaper = DefaultTextBox
DefaultShopSoldOut = "assets/ShopImage/SoldOut.png"

# Game Statistics
DefaultMenuStatOne = "assets/StatsImage/MenuStat1.png"
DefaultMenuStatTwo = DefaultSkills
DefaultMenuStatThree = DefaultSword
DefaultMenuStatFour = DefaultPotion2

# Menus (loaded in because they are frequently used.
MenuArrow = pygame.image.load("assets/MenuImage/Arrow.png")
FloaterArrow = pygame.image.load("assets/MenuImage/PressEnter.png")
DefaultMenuBackground = pygame.image.load("assets/MenuImage/MenuTag.png")
DefaultMenuSelectBackground = pygame.image.load("assets/MenuImage/MenuSelectTag.png")

DefaultMenuScroller = MenuArrow

DefaultShopTextboxFloater = FloaterArrow
DefaultShopScroller = pygame.image.load("assets/ShopImage/Scroller.png")

MenuIcon = 'assets/MainImage/Icon.png'
# https://en.wikipedia.org/wiki/List_of_mathematical_symbols

Floppy = "assets/MenuImage/Floppy.png"
Settings = "assets/MenuImage/Settings.png"

# Multiplayer
DefaultLogBox = DefaultTextBox

# Fonts
GameFont = "assets/Fonts/GameFont.ttf"
BlockyFont = "assets/Fonts/BlockyFont.ttf"
MathFont = "assets/Fonts/MathFont.ttf"
ExplanationFont = "assets/Fonts/ExplanationFont.ttf"
InputFont = "assets/Fonts/InputFont.ttf"
MathInputFont = InputFont

BattleFontString = GameFont

# Pre-loaded
FONTHEIGHT = 100
BattleFont = pygame.font.Font(BlockyFont, FONTHEIGHT)
DefaultShopTextboxTextFontString = GameFont
DefaultShopTextboxInputFontString = InputFont
DefaultShopTitleFontString = GameFont
DefaultShopBalanceFontString = GameFont
DefaultShopFontString = GameFont
DefaultInputFontString = InputFont
DefaultMenuTitleFontString = GameFont
DefaultMenuHeaderFontString = GameFont
DefaultMenuTextFontString = GameFont
DefaultMenuExplanationFontString = ExplanationFont
DefaultMenuMenuFontString = GameFont

# Files
QuestionDatabase = mQuestionRead.ReadQuestion("files/Questions.json")
BossDatabase = ABoss.ReadBoss("files/Bosses.txt")
PlayerDataFileName = "files/PlayerData.txt"
SettingDict = GameSettings.GameSettings("Game Settings/GameSettings.txt")
ErrorFileName = "files/ErrorFile.txt"
DebugFile = "files/DebugInfo.txt"
GuideFilename = ["files/Guide/One.txt", "files/Guide/Two.txt", "files/Guide/Three.txt"]
GuidePath = "files/Guide"

LevelNames = {
    1 : "Quadratic Equations and Graphs",
    2 : "Arithmetic Sequence",
    3 : "Geomtrtic Sequences and Polynomials"
}

PlayerHP = 100000
AttackDmg = {1: 15000, 2: 16500, 3: 18000}

# Battle
DefendPotionPerc = 0.05
AttackPotionPerc = 0.05
HealthPotionPerc = 0.03

# Global
CentralClock = pygame.time.Clock()

def LoopBundle():
    pygame.display.update()
    CentralClock.tick(30)

class QuitError(Exception):
    pass

def Quit(event):
    if event.type == QUIT:
        pygame.quit()
        raise QuitError

class Color:

    def __init__(self):
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)

color = Color()

PlayMusic = True


DefaultPort = 40000

# Sound effects
import simpleaudio
ButtonClick = simpleaudio.WaveObject.from_wave_file("assets/SoundEffects/ButtonEF.wav")

BattleMusic1 = "assets/SoundEffects/Karstenholymoly_-_Battle_of_the_Titans.wav"
BattleMusic2 = "assets/SoundEffects/ramblinglibrarian_-_Dawn_s_Battle_(Instrumental).wav"
BattleMusic3 = "assets/SoundEffects/stab_-_Android_Battles.wav"
BattleMusic = [BattleMusic1, BattleMusic2, BattleMusic3]
MenuMusic = "assets/SoundEffects/MenuBG.wav"
VillageMusic = "assets/SoundEffects/Vidian_-_the_Morning.wav"
AmbientMusic = "assets/SoundEffects/airtone_-_resonance.wav"
ShopMusic = "assets/SoundEffects/audio_hero_Revolving-Door_SIPML_C-1005.wav"

import wave
import pyaudio
import threading

PYAUDIO = pyaudio.PyAudio()

class AudioClass(threading.Thread) :

    CHUNK = 44100

    def __init__(self):
        super(AudioClass, self).__init__(daemon=True)
        self.AUDIO = None
        self.replayAudio = None

    def FeedAudio(self, aud):
        self.AUDIO = aud
        self.replayAudio = aud

    def run(self):
        while True:
            if self.AUDIO:
                fileobj = wave.open(self.AUDIO, 'rb')
                self.AUDIO = None

                stream = PYAUDIO.open(format = PYAUDIO.get_format_from_width(fileobj.getsampwidth()),
                                        channels = fileobj.getnchannels(),
                                        rate = fileobj.getframerate(),
                                        output = True)

                data = fileobj.readframes(self.CHUNK)
                while data and not self.AUDIO:
                    stream.write(data)
                    data = fileobj.readframes(self.CHUNK)

                stream.stop_stream()
                del stream
                del fileobj

                self.AUDIO = self.replayAudio


# A version that is not working and the reason may be the following:
# OSError: [Errno -9985] Device unavailable
# The accidental looping of generating a stream causes the
# device to dysfunction
"""
def run(self):
    while True:
        if self.AUDIO:
            # Load
            fileobj = wave.open(self.AUDIO, 'rb')
            stream = PYAUDIO.open(format=PYAUDIO.get_format_from_width(fileobj.getsampwidth()),
                                  channels=fileobj.getnchannels(),
                                  rate=fileobj.getframerate(),
                                  output=True)
            # Play
            data = fileobj.readframes(self.CHUNKS)
            while data != "" and [[[not self.AUDIO]]]:
                stream.write(data)
                data = fileobj.readframes(self.CHUNKS)
"""

audio = AudioClass()
if SettingDict["Music"]:
    audio.start()
