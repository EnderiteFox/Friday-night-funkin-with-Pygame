from pygame import *
import json
from random import *
import time as Time
import sys
import copy
import xml.etree.ElementTree as ET
import os

Inst = None
Vocals = None
chart = None
misses = 0
health = 50
BG = None
opponentAnimation = ["Up", -10]
playerAnimation = ["Up", -10]
hasPlayedMicDrop = False
combo = 0
bpm = 60000 / 100


def Main_game(musicName, speed, playAs, noDying, arrowSkinID, keybinds, downscroll, debugMode):
    global Inst
    global Vocals
    global chart
    global misses
    global health
    global BG
    global opponentAnimation
    global playerAnimation
    global options
    global hasPlayedMicDrop
    global combo
    global bpm
    misses = 0
    health = 50
    combo = 0

    init()

    K_a = keybinds[0]
    K_s = keybinds[1]
    K_w = keybinds[2]
    K_d = keybinds[3]
    K_LEFT = keybinds[4]
    K_DOWN = keybinds[5]
    K_UP = keybinds[6]
    K_RIGHT = keybinds[7]

    # region loading
    # region screen and loading screen
    screen = display.set_mode((0, 0), FULLSCREEN)
    mouse.set_visible(False)
    middleScreen = (display.Info().current_w // 2, display.Info().current_h // 2)

    def loadingscreen(progress):
        screen.fill((0, 0, 0))
        temp = font.SysFont("Comic Sans MS", 100).render("Loading...", 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1])
        screen.blit(temp, temp1)

        draw.line(screen, (255, 255, 255), (95, display.Info().current_h - 95),
                  (display.Info().current_w - 95, display.Info().current_h - 95), 3)
        draw.line(screen, (255, 255, 255), (95, display.Info().current_h - 155),
                  (display.Info().current_w - 95, display.Info().current_h - 155), 3)
        draw.line(screen, (255, 255, 255), (95, display.Info().current_h - 95), (95, display.Info().current_h - 155), 3)
        draw.line(screen, (255, 255, 255), (display.Info().current_w - 95, display.Info().current_h - 95),
                  (display.Info().current_w - 95, display.Info().current_h - 155), 3)
        if progress > 0:
            temp = (display.Info().current_w - 200) / 4
            draw.rect(screen, (255, 255, 255), Rect(100, display.Info().current_h - 150, temp * progress, 50))

        display.flip()

    loadingscreen(0)
    # endregion

    # region variables
    sys.setrecursionlimit(1000000)
    useMustHitSection = False
    clock = time.Clock()
    if 690 >= display.Info().current_w - 690:
        singlePlayer = True
    else:
        singlePlayer = False

    fpsQuality = 60
    fpsList = []
    fpsTime = Time.time()

    accuracy = 0
    accuracyDisplayTime = 0
    showAccuracy = False
    accuracyIndicator = ""
    accuracyIndicatorTime = Time.time()
    accuracyPercentList = []

    Font40 = font.SysFont("Comic Sans MS", 40)
    Font25 = font.SysFont("Comic Sans MS", 25)

    longNotesChart = []

    opponentHitTimes = [-10 for k in range(4)]
    opponentAnimation = ["Up", -10]
    playerAnimation = ["Up", -10]

    try:
        modifications = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))["modifications"]
    except:
        modifications = []

    hasPlayedMicDrop = False
    # endregion

    # region images loading
    # region load images
    arrowsSkins = [
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Arrows" + os.path.sep + "left.png").convert_alpha(),
            (150, 150)),
        transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Arrows" + os.path.sep + "down.png").convert_alpha(),
                        (150, 150)),
        transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Arrows" + os.path.sep + "up.png").convert_alpha(),
                        (150, 150)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Arrows" + os.path.sep + "right.png").convert_alpha(),
            (150, 150))]

    pressedArrowsSkins = [
        transform.scale(
            image.load(
                "assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Strum lines" + os.path.sep + "Pressed" + os.path.sep + "left.png").convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load(
                "assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Strum lines" + os.path.sep + "Pressed" + os.path.sep + "down.png").convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Strum lines" + os.path.sep + "Pressed" + os.path.sep + "up.png").convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load(
                "assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Strum lines" + os.path.sep + "Pressed" + os.path.sep + "right.png").convert_alpha(),
            (150, 150))]

    accuracyIndicatorImages = [
        transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "Accuracy indicator" + os.path.sep + "sick.png").convert_alpha(), (225, 100)),
        transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "Accuracy indicator" + os.path.sep + "good.png").convert_alpha(), (225, 100)),
        transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "Accuracy indicator" + os.path.sep + "bad.png").convert_alpha(), (225, 100)),
        transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "Accuracy indicator" + os.path.sep + "shit.png").convert_alpha(), (225, 100))]

    greyArrow = [
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Strum lines" + os.path.sep + "Static" + os.path.sep + "left.png").convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Strum lines" + os.path.sep + "Static" + os.path.sep + "down.png").convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Strum lines" + os.path.sep + "Static" + os.path.sep + "up.png").convert_alpha(),
            (150, 150)),
        transform.scale(image.load(
            "assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Strum lines" + os.path.sep + "Static" + os.path.sep + "right.png").convert_alpha(),
                        (150, 150))]

    longNotesImg = [
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Long notes" + os.path.sep + "Middle" + os.path.sep + "left.png").convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Long notes" + os.path.sep + "Middle" + os.path.sep + "down.png").convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Long notes" + os.path.sep + "Middle" + os.path.sep + "up.png").convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Long notes" + os.path.sep + "Middle" + os.path.sep + "right.png").convert_alpha(),
            (52, 46))]

    if downscroll:
        for k in range(len(longNotesImg)):
            longNotesImg[k] = transform.flip(longNotesImg[k], False, True)

    longNotesEnd = [
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Long notes" + os.path.sep + "End" + os.path.sep + "left.png").convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Long notes" + os.path.sep + "End" + os.path.sep + "down.png").convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Long notes" + os.path.sep + "End" + os.path.sep + "up.png").convert_alpha(),
            (52, 46)),
        transform.scale(
            image.load("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(arrowSkinID) + os.path.sep + "Long notes" + os.path.sep + "End" + os.path.sep + "right.png").convert_alpha(),
            (52, 46))]

    if downscroll:
        for k in range(len(longNotesEnd)):
            longNotesEnd[k] = transform.flip(longNotesEnd[k], False, True)

    try:
        backgroundName = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))["stage"]
    except:
        backgroundName = "None"

    if backgroundName != "None":
        Background = []
        width = display.Info().current_w
        height = display.Info().current_h
        for k in range(
                json.load(open("assets" + os.path.sep + "Images" + os.path.sep + "Backgrounds" + os.path.sep + "{0}".format(backgroundName) + os.path.sep + "stageData.json"))["numFrames"]):
            if not display.Info().current_w / display.Info().current_h == 1920 / 1080:
                Background.append(transform.scale(
                    image.load("assets" + os.path.sep + "Images" + os.path.sep + "Backgrounds" + os.path.sep + "{0}".format(backgroundName) + os.path.sep + "Background{0}.png".format(k)),
                    (1920, 1080)).convert_alpha())
            else:
                Background.append(transform.scale(
                    image.load("assets" + os.path.sep + "Images" + os.path.sep + "Backgrounds" + os.path.sep + "{0}".format(backgroundName) + os.path.sep + "Background{0}.png".format(k)),
                    (display.Info().current_w, display.Info().current_h)).convert_alpha())
            if not singlePlayer:
                for x in range(len(Background)):
                    Background[x] = transform.scale(Background[x], (width, height))
    else:
        Background = [Font40.render("", 1, (255, 255, 255))]
    BGrect = Background[0].get_rect()
    BGrect.bottomright = (display.Info().current_w, display.Info().current_h)

    BFdead = image.load("assets" + os.path.sep + "Images" + os.path.sep + "Death screen" + os.path.sep + "BF dead.png").convert_alpha()

    # endregion

    # region create image rect
    accuracyIndicatorRect = accuracyIndicatorImages[0].get_rect()
    accuracyIndicatorRect.center = (middleScreen[0], middleScreen[1] - 75)

    arrowRect = arrowsSkins[0].get_rect()

    deathScreenRect = BFdead.get_rect()
    deathScreenRect.midbottom = (middleScreen[0], display.Info().current_h - 50)
    # endregion

    musicList = json.load(open("assets/MusicList.json"))["musics"]

    loadingscreen(1)

    # endregion

    # region music and chart loading
    deathScreenMusic = mixer.Sound("assets" + os.path.sep + "Images" + os.path.sep + "Death screen" + os.path.sep + "gameOver.ogg")
    deathScreenMusicEnd = mixer.Sound("assets" + os.path.sep + "Images" + os.path.sep + "Death screen" + os.path.sep + "gameOverEnd.ogg")
    deathScreenMusicStart = mixer.Sound("assets" + os.path.sep + "Images" + os.path.sep + "Death screen" + os.path.sep + "micDrop.ogg")

    def open_file(music):
        global Inst
        global Vocals
        global chart
        global bpm
        Inst = mixer.Sound("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "Inst.ogg")
        Vocals = mixer.Sound("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "Voices.ogg")
        try:
            chart = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "chart.json"))["song"]["notes"]
        except:
            print("Chart is in incorrect format, formatting it")
            chart = {"song": json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "chart.json"))}
            json.dump(chart, open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "chart.json", "w"))
            chart = chart["song"]["notes"]
        try:
            bpm = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "chart.json"))["song"]["bpm"]
            bpm = 60000 / bpm
        except error as e:
            print("No BPM detected, using 100 bpm")
            if debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            bpm = 60000 / 100

    def play(music=False):
        if not music:
            open_file(musicList[randint(0, len(musicList) - 1)])
        else:
            open_file(music)

    play(musicName)

    temp1 = Inst.get_length()
    temp2 = Vocals.get_length()
    if temp1 > temp2:
        musicLen = temp1
    else:
        musicLen = temp2

    loadingscreen(2)

    # endregion

    # region chart managment
    class Note:
        def __init__(self, pos, column, side, length, noteId):
            self.pos = pos
            self.column = column
            self.side = side
            self.length = length
            self.id = noteId

    class LongNote:
        def __init__(self, pos, column, side, isEnd):
            self.pos = pos
            self.column = column
            self.side = side
            self.isEnd = isEnd

    class LongNoteGroup:
        def __init__(self, groupId):
            self.id = groupId
            self.notes = []
            self.size = 0
            self.canDealDamage = True

        def setSize(self):
            self.notes.remove(self.notes[0])
            self.size = len(self.notes)

    # region tests if chart uses mustHitSection
    notesChart = []

    for section in chart:
        if not section["mustHitSection"]:
            useMustHitSection = True
    # endregion

    # region create notes
    # Column meaning:
    #   If not useMustHitSection:
    #       0 = player left
    #       1 = player down
    #       2 = player up
    #       3 = player right
    #       4 = opponent down
    #       5 = opponent left
    #       6 = opponent up
    #       7 = opponent right
    #
    #   If useMustHitSection:
    #       If mustHit:
    #           0 = player left
    #           1 = player down
    #           2 = player up
    #           3 = player right
    #           4 = opponent left
    #           5 = opponent down
    #           6 = opponent up
    #           7 = opponent right
    #       If not mustHit:
    #           0 = opponent down
    #           1 = opponent left
    #           2 = opponent up
    #           3 = opponent right
    #           4 = player left
    #           5 = player down
    #           6 = player up
    #           7 = player right

    if playAs == "Player":
        tempPlayAs = ["Player", "Opponent"]
    else:
        tempPlayAs = ["Opponent", "Player"]

    tempNoteId = 0
    for section in chart:
        if not useMustHitSection:
            tempMustHit = True
        else:
            tempMustHit = section["mustHitSection"]
        for note in section["sectionNotes"]:
            tempUser = ""
            tempDirection = ""
            if type(note[2]) == int or type(note[2]) == float:
                if not useMustHitSection:
                    if 3 >= note[1] >= 0:
                        tempUser = tempPlayAs[0]
                    elif 7 >= note[1] >= 4:
                        tempUser = tempPlayAs[1]
                    if note[1] == 0 or note[1] == 5:
                        tempDirection = "Left"
                    if note[1] == 1 or note[1] == 4:
                        tempDirection = "Down"
                    if note[1] == 2 or note[1] == 6:
                        tempDirection = "Up"
                    if note[1] == 3 or note[1] == 7:
                        tempDirection = "Right"
                if useMustHitSection:
                    if tempMustHit:
                        if 3 >= note[1] >= 0:
                            tempUser = tempPlayAs[0]
                        if 7 >= note[1] >= 4:
                            tempUser = tempPlayAs[1]
                        if note[1] == 0 or note[1] == 4:
                            tempDirection = "Left"
                        if note[1] == 1 or note[1] == 5:
                            tempDirection = "Down"
                        if note[1] == 2 or note[1] == 6:
                            tempDirection = "Up"
                        if note[1] == 3 or note[1] == 7:
                            tempDirection = "Right"
                    if not tempMustHit:
                        if 3 >= note[1] >= 0:
                            tempUser = tempPlayAs[1]
                        if 7 >= note[1] >= 4:
                            tempUser = tempPlayAs[0]
                        if note[1] == 1 or note[1] == 5:
                            tempDirection = "Down"
                        if note[1] == 0 or note[1] == 4:
                            tempDirection = "Left"
                        if note[1] == 2 or note[1] == 6:
                            tempDirection = "Up"
                        if note[1] == 3 or note[1] == 7:
                            tempDirection = "Right"
                notesChart.append(Note(note[0], tempDirection, tempUser, note[2], tempNoteId))
                tempNoteId += 1
    # endregion

    # region sort notes and create long notes and double notes fix
    notesChart.sort(key=lambda s: s.pos)

    temp = 0
    for k in range(len(notesChart)):
        if notesChart[k] is None:
            temp += 1

    for k in range(temp):
        notesChart.remove(None)

    longNotesLen = 42 // speed
    for note in notesChart:
        if note.length >= longNotesLen > 0 and int(round(note.length // longNotesLen)):
            tempGroup = LongNoteGroup(note.id)
            for k in range(1, int(round(note.length // longNotesLen))):
                tempGroup.notes.append(LongNote(note.pos + k * longNotesLen, note.column, note.side, False))
            tempGroup.notes.append(
                LongNote(note.pos + (note.length // longNotesLen) * longNotesLen, note.column, note.side, True))
            tempGroup.setSize()
            longNotesChart.append(tempGroup)

    longNotesChart.sort(key=lambda s: s.id)
    for element in longNotesChart:
        element.notes.sort(key=lambda s: s.pos)

    loadingscreen(3)

    # endregion
    # endregion

    # region characters
    def getAttibuteRect(data):
        return Rect(float(data.attrib["x"]), float(data.attrib["y"]), float(data.attrib["width"]),
                    float(data.attrib["height"]))

    def getNfirstCharacters(text, n):
        result = ""
        if n < len(text):
            for k in range(n):
                result = "{0}{1}".format(result, text[k])
            return result
        else:
            return text

    def getNlastCharacters(text, n):
        result = ""
        for k in range(n):
            result = "{1}{0}".format(result, text[-k - 1])
        return result

    def getXmlData(characterName):
        XMLpath = "assets" + os.path.sep + "Images" + os.path.sep + "Characters" + os.path.sep + "{0}".format(characterName) + os.path.sep + "character.xml"
        characterImage = image.load("assets" + os.path.sep + "Images" + os.path.sep + "Characters" + os.path.sep + "{0}".format(characterName) + os.path.sep + "character.png").convert_alpha()
        XMLfile = ET.parse(XMLpath).getroot()
        result = [[] for k in range(5)]
        offset = [[] for k in range(5)]
        for data in XMLfile:
            name = data.attrib["name"]
            tempResult = ""
            for k in range(len(name)):
                if name[k] == "_":
                    tempResult = "{0}{1}".format(tempResult, " NOTE ")
                else:
                    tempResult = "{0}{1}".format(tempResult, name[k].upper())
            data.attrib["name"] = tempResult
        for data in XMLfile:
            name = data.attrib["name"]
            tempResult = ""
            temp = False
            for k in range(len(name)):
                if temp:
                    tempResult = "{0}{1}".format(tempResult, name[k])
                if name[k] == " ":
                    temp = True
            if tempResult == "":
                tempResult = name
            else:
                data.attrib["name"] = tempResult
        for data in XMLfile:
            name = data.attrib["name"]
            if getNfirstCharacters(name, 9) == "NOTE IDLE" or getNfirstCharacters(name, 4) == "IDLE":
                name = "idle dance{0}".format(getNlastCharacters(name, 4))
            data.attrib["name"] = name
        for data in XMLfile:
            name = data.attrib["name"]
            if getNfirstCharacters(name, 10) == "IDLE DANCE":
                data.attrib["name"] = name.lower()
        for data in XMLfile:
            name = data.attrib["name"]
            if getNfirstCharacters(name, 2) == "UP":
                name = "NOTE UP{0}".format(getNlastCharacters(name, 4))
            if getNfirstCharacters(name, 4) == "DOWN":
                name = "NOTE DOWN{0}".format(getNlastCharacters(name, 4))
            if getNfirstCharacters(name, 4) == "LEFT":
                name = "NOTE LEFT{0}".format(getNlastCharacters(name, 4))
            if getNfirstCharacters(name, 5) == "RIGHT":
                name = "NOTE RIGHT{0}".format(getNlastCharacters(name, 4))
            data.attrib["name"] = name
        for data in XMLfile:
            if getNfirstCharacters(data.attrib["name"], 9) == "NOTE LEFT" and len(data.attrib["name"]) == 13:
                result[0].append(characterImage.subsurface(getAttibuteRect(data)))
                try:
                    offset[0].append([data.attrib["frameX"], data.attrib["frameY"]])
                except:
                    offset[0].append([0, 0])
            if getNfirstCharacters(data.attrib["name"], 9) == "NOTE DOWN" and len(data.attrib["name"]) == 13:
                result[1].append(characterImage.subsurface(getAttibuteRect(data)))
                try:
                    offset[1].append([data.attrib["frameX"], data.attrib["frameY"]])
                except:
                    offset[1].append([0, 0])
            if getNfirstCharacters(data.attrib["name"], 7) == "NOTE UP" and len(data.attrib["name"]) == 11:
                result[2].append(characterImage.subsurface(getAttibuteRect(data)))
                try:
                    offset[2].append([data.attrib["frameX"], data.attrib["frameY"]])
                except:
                    offset[2].append([0, 0])
            if getNfirstCharacters(data.attrib["name"], 10) == "NOTE RIGHT" and len(data.attrib["name"]) == 14:
                result[3].append(characterImage.subsurface(getAttibuteRect(data)))
                try:
                    offset[3].append([data.attrib["frameX"], data.attrib["frameY"]])
                except:
                    offset[3].append([0, 0])
            if getNfirstCharacters(data.attrib["name"], 10) == "idle dance" and len(data.attrib["name"]) == 14:
                result[4].append(characterImage.subsurface(getAttibuteRect(data)))
                try:
                    offset[4].append([data.attrib["frameX"], data.attrib["frameY"]])
                except:
                    offset[4].append([0, 0])
        for k in range(len(offset)):
            for x in range(len(offset[k])):
                offset[k][x][0] = int(offset[k][x][0])
                offset[k][x][1] = int(offset[k][x][1])
        return result, offset

    class Character:
        def __init__(self, name, characterNum):
            if name != "None":
                if playAs == "Opponent":
                    if characterNum == 1:
                        temp = 2
                    else:
                        temp = 1
                else:
                    temp = characterNum
                self.size = \
                    json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))["character{0}".format(temp)][
                        "size"]
                temp1 = getXmlData(name)
                self.texture = temp1[0]
                self.offset = temp1[1]
                for k in range(5):
                    for x in range(len(self.offset[k])):
                        self.offset[k][x][0] *= self.size[k][0]
                        self.offset[k][x][1] *= self.size[k][1]
                self.pos = \
                    json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))["character{0}".format(temp)][
                        "pos"]
                try:
                    self.isCentered = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))["isCentered"]
                except:
                    self.isCentered = False
                if self.isCentered == "True":
                    if characterNum == 1:
                        self.pos[0] = display.Info().current_w / 2 + self.pos[0]
                        self.pos[1] = display.Info().current_h / 2 + self.pos[1]
                    else:
                        self.pos[0] = display.Info().current_w / 2 - self.pos[0]
                        self.pos[1] = display.info().current_h / 2 + self.pos[1]
                for k in range(5):
                    for x in range(len(self.offset[k])):
                        if characterNum == 1:
                            self.offset[k][x][0] = self.pos[0] + self.offset[k][x][0]
                            self.offset[k][x][1] = self.pos[1] + self.offset[k][x][1]
                        else:
                            self.offset[k][x][0] = self.pos[0] - self.offset[k][x][0]
                            self.offset[k][x][1] = self.pos[1] + self.offset[k][x][1]
                self.pos = self.offset
                for k in range(5):
                    for x in range(len(self.texture[k])):
                        self.texture[k][x] = transform.scale(self.texture[k][x], (
                            int(self.texture[k][x].get_width() * self.size[k][0]),
                            int(self.texture[k][x].get_height() * self.size[k][1])))
                try:
                    dontFlip = json.load(open("assets" + os.path.sep + "Images" + os.path.sep + "Characters" + os.path.sep + "{0}".format(name) + os.path.sep + "characterData.json"))[
                        "dont_flip"]
                except:
                    dontFlip = "False"
                if (characterNum == 2 and dontFlip == "False") or (characterNum == 1 and dontFlip == "True"):
                    for k in range(5):
                        for x in range(len(self.texture[k])):
                            self.texture[k][x] = transform.flip(self.texture[k][x], True, False)
                    temp1 = self.texture[0]
                    self.texture[0] = self.texture[3]
                    self.texture[3] = temp1
                if characterNum == 1:
                    temp1 = self.pos[0]
                    self.pos[0] = self.pos[3]
                    self.pos[3] = temp1
            else:
                self.texture = [[Font40.render("", 1, (255, 255, 255))] for k in range(5)]
                self.pos = [[[0, 0]] for k in range(5)]

    if playAs == "Player":
        try:
            character1 = Character(
                json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))["character1"]["Name"], 1)
        except error as e:
            print("Opponent character loading failed, skipping loading")
            if debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character1 = Character("None", 1)
        try:
            character2 = Character(
                json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))["character2"]["Name"], 2)
        except error as e:
            print("Player character loading failed, skipping loading")
            if debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character2 = Character("None", 2)
    else:
        try:
            character1 = Character(
                json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))["character2"]["Name"], 1)
        except error as e:
            print("Opponent character loading failed, skipping loading")
            if debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character1 = Character("None", 1)
        try:
            character2 = Character(
                json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))["character1"]["Name"], 2)
        except error as e:
            print("Player character loading failed, skipping loading")
            if debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character2 = Character("None", 2)

    if singlePlayer:
        print("Resolution too low to display both characters, using singleplayer mode")
        character1 = Character("None", 2)

    print(character2.pos[4])

    # endregion
    # endregion

    # region screen and notes update
    def drawGreyNotes():
        width = display.Info().current_w
        height = display.Info().current_h
        currentTime = Time.time() - startTime
        if "hideNotes2" not in modifications:
            temp = arrowRect
            if not downscroll:
                temp.topright = (width - 540, 50)
            else:
                temp.bottomright = (width - 540, height - 50)
            if K_a in keyPressed or K_LEFT in keyPressed:
                screen.blit(pressedArrowsSkins[0], temp)
            else:
                screen.blit(greyArrow[0], temp)
            temp = arrowRect
            if not downscroll:
                temp.topright = (width - 380, 50)
            else:
                temp.bottomright = (width - 380, height - 50)
            if K_s in keyPressed or K_DOWN in keyPressed:
                screen.blit(pressedArrowsSkins[1], temp)
            else:
                screen.blit(greyArrow[1], temp)
            temp = arrowRect
            if not downscroll:
                temp.topright = (width - 220, 50)
            else:
                temp.bottomright = (width - 220, height - 50)
            if K_w in keyPressed or K_UP in keyPressed:
                screen.blit(pressedArrowsSkins[2], temp)
            else:
                screen.blit(greyArrow[2], temp)
            temp = arrowRect
            if not downscroll:
                temp.topright = (width - 60, 50)
            else:
                temp.bottomright = (width - 60, height - 50)
            if K_d in keyPressed or K_RIGHT in keyPressed:
                screen.blit(pressedArrowsSkins[3], temp)
            else:
                screen.blit(greyArrow[3], temp)
        if not singlePlayer and "hideNotes1" not in modifications:
            temp = arrowRect
            if not downscroll:
                temp.topleft = (60, 50)
            else:
                temp.bottomleft = (60, height - 50)
            if currentTime - opponentHitTimes[0] > 0.15:
                screen.blit(greyArrow[0], temp)
            else:
                screen.blit(pressedArrowsSkins[0], temp)
            temp = arrowRect
            if not downscroll:
                temp.topleft = (220, 50)
            else:
                temp.bottomleft = (220, height - 50)
            if currentTime - opponentHitTimes[1] > 0.15:
                screen.blit(greyArrow[1], temp)
            else:
                screen.blit(pressedArrowsSkins[1], temp)
            temp = arrowRect
            if not downscroll:
                temp.topleft = (380, 50)
            else:
                temp.bottomleft = (380, height - 50)
            if currentTime - opponentHitTimes[2] > 0.15:
                screen.blit(greyArrow[2], temp)
            else:
                screen.blit(pressedArrowsSkins[2], temp)
            temp = arrowRect
            if not downscroll:
                temp.topleft = (540, 50)
            else:
                temp.bottomleft = (540, height - 50)
            if currentTime - opponentHitTimes[3] > 0.15:
                screen.blit(greyArrow[3], temp)
            else:
                screen.blit(pressedArrowsSkins[3], temp)

    def drawNotes():
        global misses
        global health
        global opponentAnimation
        global combo
        currentTime = Time.time() - startTime
        width = display.Info().current_w
        height = display.Info().current_h
        renderNotes = True
        for note in notesChart:
            if renderNotes:
                if note.side == "Opponent" and currentTime * 1000 >= note.pos:
                    opponentAnimation = [note.column, currentTime]
                    opponentHitTimes[["Left", "Down", "Up", "Right"].index(note.column)] = currentTime
                    notesChart.remove(note)
                if currentTime * 1000 - 133 >= note.pos and note.side == "Player" and note.column in ["Left", "Down",
                                                                                                      "Up",
                                                                                                      "Right"]:
                    for noteGroup in longNotesChart:
                        if noteGroup.id == note.id:
                            noteGroup.canDealDamage = False
                            break
                    notesChart.remove(note)
                    misses += 1
                    health -= 4
                    accuracyPercentList.append(0)
                    combo = 0
                if 50 + (note.pos - currentTime * 1000) * speed < display.Info().current_h + 100:
                    if not singlePlayer and "hideNotes1" not in modifications:
                        if note.side == "Opponent" and note.column == "Down":
                            temp = arrowRect
                            if not downscroll:
                                temp.topleft = (220, 50 + (note.pos - currentTime * 1000) * speed)
                            else:
                                temp.bottomleft = (220, height - 50 - (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[1], temp)
                        elif note.side == "Opponent" and note.column == "Left":
                            temp = arrowRect
                            if not downscroll:
                                temp.topleft = (60, 50 + (note.pos - currentTime * 1000) * speed)
                            else:
                                temp.bottomleft = (60, height - 50 - (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[0], temp)
                        elif note.side == "Opponent" and note.column == "Up":
                            temp = arrowRect
                            if not downscroll:
                                temp.topleft = (380, 50 + (note.pos - currentTime * 1000) * speed)
                            else:
                                temp.bottomleft = (380, height - 50 - (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[2], temp)
                        elif note.side == "Opponent" and note.column == "Right":
                            temp = arrowRect
                            if not downscroll:
                                temp.topleft = (540, 50 + (note.pos - currentTime * 1000) * speed)
                            else:
                                temp.bottomleft = (540, height - 50 - (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[3], temp)
                    if "hideNotes2" not in modifications:
                        if note.side == "Player" and note.column == "Down":
                            temp = arrowRect
                            if not downscroll:
                                temp.topright = (width - 380, 50 + (note.pos - currentTime * 1000) * speed)
                            else:
                                temp.bottomright = (width - 380, height - 50 - (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[1], temp)
                        elif note.side == "Player" and note.column == "Left":
                            temp = arrowRect
                            if not downscroll:
                                temp.topright = (width - 540, 50 + (note.pos - currentTime * 1000) * speed)
                            else:
                                temp.bottomright = (width - 540, height - 50 - (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[0], temp)
                        elif note.side == "Player" and note.column == "Up":
                            temp = arrowRect
                            if not downscroll:
                                temp.topright = (width - 220, 50 + (note.pos - currentTime * 1000) * speed)
                            else:
                                temp.bottomright = (width - 220, height - 50 - (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[2], temp)
                        elif note.side == "Player" and note.column == "Right":
                            temp = arrowRect
                            if not downscroll:
                                temp.topright = (width - 60, 50 + (note.pos - currentTime * 1000) * speed)
                            else:
                                temp.bottomright = (width - 60, height - 50 - (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[3], temp)

                else:
                    renderNotes = False

    def drawLongNotes():
        global opponentAnimation
        global playerAnimation
        global misses
        global health
        global combo
        currentTime = Time.time() - startTime
        width = display.Info().current_w
        height = display.Info().current_h
        deleteList = []
        for noteGroup in longNotesChart:
            deleteGroup = False
            run = True
            if len(noteGroup.notes) == 0:
                run = False
                deleteGroup = True
            if run and 50 + (noteGroup.notes[0].pos - currentTime * 1000) * speed < height + 100:
                for longNote in noteGroup.notes:
                    transparent = False
                    if currentTime * 1000 - 133 >= longNote.pos:
                        if longNote.side == "Player":
                            if (noteGroup.size - len(noteGroup.notes)) / noteGroup.size >= 0.75:
                                noteGroup.canDealDamage = False
                            if noteGroup.canDealDamage:
                                misses += 1
                                health -= 4
                                accuracyPercentList.append(0)
                                combo = 0
                                noteGroup.canDealDamage = False
                            noteGroup.notes.remove(longNote)
                    else:
                        if noteGroup.canDealDamage:
                            transparent = False
                        else:
                            transparent = True
                        if longNote.side == "Opponent" and currentTime * 1000 >= longNote.pos:
                            if currentTime - opponentAnimation[1] > 0.7:
                                opponentAnimation = [longNote.column, currentTime]
                            opponentHitTimes[["Left", "Down", "Up", "Right"].index(longNote.column)] = currentTime
                            noteGroup.notes.remove(longNote)
                        if longNote.side == "Player" and currentTime * 1000 >= longNote.pos and longNote.column in [
                            "Left",
                            "Down",
                            "Up",
                            "Right"]:
                            if ((K_LEFT in keyPressed or K_a in keyPressed) and longNote.column == "Left") or (
                                    (K_DOWN in keyPressed or K_s in keyPressed) and longNote.column == "Down") or (
                                    (K_UP in keyPressed or K_w in keyPressed) and longNote.column == "Up") or (
                                    (K_RIGHT in keyPressed or K_d in keyPressed) and longNote.column == "Right"):
                                if currentTime - playerAnimation[1] > 0.7:
                                    playerAnimation = [longNote.column, currentTime]
                                noteGroup.notes.remove(longNote)
                        if 50 + (longNote.pos - currentTime * 1000) * speed < height + 100:
                            if not singlePlayer and longNote.side == "Opponent" and "hideNotes1" not in modifications:
                                if longNote.column == "Down":
                                    temp = arrowRect
                                    if not downscroll:
                                        temp.center = (
                                            220 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                    else:
                                        temp.center = (
                                            220 + 125, height - 50 - (longNote.pos - currentTime * 1000) * speed)
                                    if longNote.isEnd:
                                        screen.blit(longNotesEnd[1], temp)
                                    else:
                                        screen.blit(longNotesImg[1], temp)
                                if longNote.column == "Left":
                                    temp = arrowRect
                                    if not downscroll:
                                        temp.center = (60 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                    else:
                                        temp.center = (
                                            60 + 125, height - 50 - (longNote.pos - currentTime * 1000) * speed)
                                    if longNote.isEnd:
                                        screen.blit(longNotesEnd[0], temp)
                                    else:
                                        screen.blit(longNotesImg[0], temp)
                                if longNote.column == "Up":
                                    temp = arrowRect
                                    if not downscroll:
                                        temp.center = (
                                            380 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                    else:
                                        temp.center = (
                                            380 + 125, height - 50 - (longNote.pos - currentTime * 1000) * speed)
                                    if longNote.isEnd:
                                        screen.blit(longNotesEnd[2], temp)
                                    else:
                                        screen.blit(longNotesImg[2], temp)
                                if longNote.column == "Right":
                                    temp = arrowRect
                                    if not downscroll:
                                        temp.center = (
                                            540 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                    else:
                                        temp.center = (
                                            540 + 125, height - 50 - (longNote.pos - currentTime * 1000) * speed)
                                    if longNote.isEnd:
                                        screen.blit(longNotesEnd[3], temp)
                                    else:
                                        screen.blit(longNotesImg[3], temp)
                            if longNote.side == "Player" and "hideNotes2" not in modifications:
                                if longNote.column == "Up":
                                    temp = arrowRect
                                    if not downscroll:
                                        temp.center = (
                                            width - 220 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                    else:
                                        temp.center = (
                                            width - 220 - 25, height - 50 - (longNote.pos - currentTime * 1000) * speed)
                                    if longNote.isEnd:
                                        img = copy.copy(longNotesEnd[2])
                                    else:
                                        img = copy.copy(longNotesImg[2])
                                    if transparent:
                                        img.set_alpha(100)
                                    screen.blit(img, temp)
                                if longNote.column == "Down":
                                    temp = arrowRect
                                    if not downscroll:
                                        temp.center = (
                                            width - 380 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                    else:
                                        temp.center = (
                                            width - 380 - 25, height - 50 - (longNote.pos - currentTime * 1000) * speed)
                                    if longNote.isEnd:
                                        img = copy.copy(longNotesEnd[1])
                                    else:
                                        img = copy.copy(longNotesImg[1])
                                    if transparent:
                                        img.set_alpha(100)
                                    screen.blit(img, temp)
                                if longNote.column == "Left":
                                    temp = arrowRect
                                    if not downscroll:
                                        temp.center = (
                                            width - 540 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                    else:
                                        temp.center = (
                                            width - 540 - 25, height - 50 - (longNote.pos - currentTime * 1000) * speed)
                                    if longNote.isEnd:
                                        img = copy.copy(longNotesEnd[0])
                                    else:
                                        img = copy.copy(longNotesImg[0])
                                    if transparent:
                                        img.set_alpha(100)
                                    screen.blit(img, temp)
                                if longNote.column == "Right":
                                    temp = arrowRect
                                    if not downscroll:
                                        temp.center = (
                                            width - 60 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                                    else:
                                        temp.center = (
                                            width - 60 - 25, height - 50 - (longNote.pos - currentTime * 1000) * speed)
                                    if longNote.isEnd:
                                        img = copy.copy(longNotesEnd[3])
                                    else:
                                        img = copy.copy(longNotesImg[3])
                                    if transparent:
                                        img.set_alpha(100)
                                    screen.blit(img, temp)
            if deleteGroup:
                deleteList.append(noteGroup.id)
        for element in longNotesChart:
            if element.id in deleteList:
                deleteList.remove(element.id)
                longNotesChart.remove(element)
            if len(deleteList) == 0:
                break

    def drawHealthBar():
        global health
        if health > 100:
            health = 100
        if health < 0:
            health = 0
        width = display.Info().current_w
        height = display.Info().current_h
        if not downscroll:
            draw.rect(screen, (255, 255, 255), Rect(45, height - 115, width - 90, 60))
        else:
            draw.rect(screen, (255, 255, 255), Rect(45, 55, width - 90, 60))
        if health < 100:
            if not downscroll:
                draw.rect(screen, (255, 0, 0), Rect(50, height - 110, (width - 100) / 100 * (100 - health), 50))
            else:
                draw.rect(screen, (255, 0, 0), Rect(50, 60, (width - 100) / 100 * (100 - health), 50))
        if health > 0:
            if not downscroll:
                draw.rect(screen, (0, 255, 0),
                          Rect(50 + (width - 100) / 100 * (100 - health), height - 110, (width - 100) / 100 * health,
                               50))
            else:
                draw.rect(screen, (0, 255, 0),
                          Rect(50 + (width - 100) / 100 * (100 - health), 60, (width - 100) / 100 * health, 50))

    def drawCharacters():
        currentTime = Time.time() - startTime
        if currentTime - opponentAnimation[1] >= 0.75:
            animationFrame = int((((Time.time() - startTime) * 1000 / 2) % bpm) / bpm * len(character1.texture[4]))
            temp = character1.texture[4][animationFrame].get_rect()
            temp.center = [character1.pos[4][animationFrame][0],
                              display.Info().current_h - character1.pos[4][animationFrame][1]]
            screen.blit(character1.texture[4][animationFrame], temp)
        else:
            animationDirection = ["Left", "Down", "Up", "Right"].index(opponentAnimation[0])
            if currentTime - opponentAnimation[1] < 0.45:
                tempTime = 0.45 / len(character1.texture[animationDirection])
                numFrame = int((currentTime - opponentAnimation[1]) // tempTime)
            else:
                numFrame = len(character1.texture[animationDirection]) - 1
            temp = character1.texture[animationDirection][numFrame].get_rect()
            temp.center = [character1.pos[animationDirection][numFrame][0],
                              display.Info().current_h - character1.pos[animationDirection][numFrame][1]]
            screen.blit(character1.texture[animationDirection][numFrame], temp)
        if currentTime - playerAnimation[1] >= 0.75:
            animationFrame = int((((Time.time() - startTime) * 1000 / 2) % bpm) / bpm * len(character2.texture[4]))
            temp = character2.texture[4][animationFrame].get_rect()
            temp.center = [display.Info().current_w - character2.pos[4][animationFrame][0],
                              display.Info().current_h - character2.pos[4][animationFrame][1]]
            screen.blit(character2.texture[4][animationFrame], temp)
        else:
            animationDirection = ["Left", "Down", "Up", "Right"].index(playerAnimation[0])
            if currentTime - playerAnimation[1] < 0.45:
                tempTime = 0.45 / len(character2.texture[animationDirection])
                numFrame = int((currentTime - playerAnimation[1]) // tempTime)
            else:
                numFrame = len(character2.texture[animationDirection]) - 1
            temp = character2.texture[animationDirection][numFrame].get_rect()
            temp.center = [display.Info().current_w - character2.pos[animationDirection][numFrame][0],
                              display.Info().current_h - character2.pos[animationDirection][numFrame][1]]
            screen.blit(character2.texture[animationDirection][numFrame], temp)

    # endregion

    # region death screen
    def death():
        global hasPlayedMicDrop
        startDeathTime = Time.time()
        deathScreenMusicStart.play()
        while True:
            for events in event.get():
                if events.type == QUIT:
                    deathScreenMusic.stop()
                    deathScreenMusicEnd.stop()
                    quit()
                    exit()
                if events.type == KEYDOWN:
                    if events.key == K_ESCAPE or events.key == K_BACKSPACE:
                        deathScreenMusic.stop()
                        return False
                    if events.key == K_SPACE or events.key == K_RETURN:
                        deathScreenMusic.stop()
                        deathScreenMusicEnd.play()
                        Time.sleep(deathScreenMusicEnd.get_length() - 2.5)
                        deathScreenMusicEnd.stop()
                        return True
            screen.fill((0, 0, 0))
            if Time.time() - startDeathTime > deathScreenMusicStart.get_length() - 1.5 and not hasPlayedMicDrop:
                deathScreenMusic.play(-1)
                hasPlayedMicDrop = True
            screen.blit(BFdead, deathScreenRect)
            display.flip()

    # endregion

    # region song progress bar
    def drawProgressBar():
        currentTime = Time.time() - startTime
        width = display.Info().current_w
        height = display.Info().current_h
        if not downscroll:
            draw.rect(screen, (255, 255, 255), Rect(400, 5, width - 800, 40))
            draw.rect(screen, (0, 0, 0), Rect(402, 7, width - 804, 36))
        else:
            draw.rect(screen, (255, 255, 255), Rect(400, height - 5 - 40, width - 800, 40))
            draw.rect(screen, (0, 0, 0), Rect(402, height - 7 - 36, width - 804, 36))
        temp = int(round(musicLen - (Time.time() - startTime), 0))
        if not downscroll:
            draw.rect(screen, (170, 170, 170), Rect(405, 10, (width - 810) / musicLen * currentTime, 30))
        else:
            draw.rect(screen, (170, 170, 170), Rect(405, height - 10 - 30, (width - 810) / musicLen * currentTime, 30))
        tempMinutes = temp // 60
        tempSeconds = temp - (60 * tempMinutes)
        if tempSeconds < 10:
            temp1 = "0"
        else:
            temp1 = ""
        temp = Font25.render("{0}  {1}:{2}{3}".format(musicName, tempMinutes, temp1, tempSeconds), 1, (255, 255, 255))
        temp1 = temp.get_rect()
        if not downscroll:
            temp1.midtop = (middleScreen[0], 5)
        else:
            temp1.midbottom = (middleScreen[0], height - 10)
        screen.blit(temp, temp1)

    loadingscreen(4)
    # endregion

    keyPressed = []

    Inst.play()
    Vocals.play()

    startTime = Time.time()
    while True:
        notesToClear = [[], [], [], []]
        for events in event.get():
            if events.type == QUIT:
                quit()
                exit()
            if events.type == KEYDOWN and events.key == K_ESCAPE:
                Inst.stop()
                Vocals.stop()
                return False
            if events.type == KEYDOWN:
                keyPressed.append(events.key)
            if events.type == KEYDOWN and events.key == K_SPACE:
                print("Debug: Current song position: {0}".format((Time.time() - startTime) * 1000))
            if events.type == KEYUP and events.key in keyPressed:
                keyPressed.remove(events.key)
            if events.type == KEYDOWN:
                currentTime = Time.time() - startTime
                testNotes = True
                for note in notesChart:
                    if testNotes:
                        if note.pos <= currentTime * 1000 + 133:
                            if note.side == "Player" and currentTime * 1000 - 133 <= note.pos <= currentTime * 1000 + 133 and note.column in [
                                "Left", "Down", "Up", "Right"]:
                                if (events.key == K_a or events.key == K_LEFT) and note.column == "Left":
                                    notesToClear[0].append(note)
                                if (events.key == K_s or events.key == K_DOWN) and note.column == "Down":
                                    notesToClear[1].append(note)
                                if (events.key == K_w or events.key == K_UP) and note.column == "Up":
                                    notesToClear[2].append(note)
                                if (events.key == K_d or events.key == K_RIGHT) and note.column == "Right":
                                    notesToClear[3].append(note)
                        else:
                            testNotes = False
        currentTime = Time.time() - startTime
        for k in range(4):
            if len(notesToClear[k]) > 0:
                min = notesToClear[k][0].pos
                minX = 0
                x = 0
                for element in notesToClear[k]:
                    if element.pos < min:
                        min = element.pos
                        minX = x
                    x += 1
                accuracy = str(round(notesToClear[k][minX].pos - currentTime * 1000, 2))
                showAccuracy = True
                accuracyDisplayTime = Time.time()
                # region Accuracy timings info
                # Sick: <= 47
                # Good: <= 79
                # Bad: <= 109
                # Shit: <= 133
                # endregion
                if currentTime * 1000 + 47 >= notesToClear[k][minX].pos >= currentTime * 1000 - 47:
                    accuracyIndicator = accuracyIndicatorImages[0]
                    accuracyPercentList.append(1)
                    health += 2.3
                    combo += 1
                elif currentTime * 1000 + 79 >= notesToClear[k][minX].pos >= currentTime * 1000 - 79:
                    accuracyIndicator = accuracyIndicatorImages[1]
                    accuracyPercentList.append(0.75)
                    health += 0.4
                    combo += 1
                elif currentTime * 1000 + 109 >= notesToClear[k][minX].pos >= currentTime * 1000 - 109:
                    accuracyIndicator = accuracyIndicatorImages[2]
                    accuracyPercentList.append(0.5)
                    health += 0.4
                    combo += 1
                else:
                    accuracyIndicator = accuracyIndicatorImages[3]
                    accuracyPercentList.append(-1)
                    misses += 1
                    health -= 4
                    combo = 0
                playerAnimation = [notesToClear[k][minX].column, currentTime]
                notesChart.remove(notesToClear[k][minX])
        screen.fill((0, 0, 0))
        backgroundFrameNum = int((((Time.time() - startTime) * 1000 / 2) % bpm) / bpm * len(Background))
        screen.blit(Background[backgroundFrameNum], BGrect)
        drawCharacters()
        drawGreyNotes()
        drawLongNotes()
        drawNotes()
        drawProgressBar()
        # region draw bottom info bar
        if len(accuracyPercentList) == 0:
            tempAccuracy = "NA"
        else:
            temp = 0
            for element in accuracyPercentList:
                temp += element
            temp /= len(accuracyPercentList)
            tempAccuracy = "{0}%".format(round(temp * 100, 2))
        temp = Font40.render("Combo: {0} | Misses: {1} | Accuracy: {2}".format(combo, misses, tempAccuracy), 1,
                             (255, 255, 255))
        temp1 = temp.get_rect()
        if not downscroll:
            temp1.midbottom = (middleScreen[0], display.Info().current_h - 5)
        else:
            temp1.midtop = (middleScreen[0], 0)
        screen.blit(temp, temp1)
        # endregion
        # region accuracy display
        if Time.time() - accuracyDisplayTime > 0.5:
            showAccuracy = False
        if showAccuracy:
            temp = Font40.render(accuracy, 1, (255, 255, 255))
            temp1 = temp.get_rect()
            temp1.center = (middleScreen[0], middleScreen[1])
            screen.blit(temp, temp1)

            screen.blit(accuracyIndicator, accuracyIndicatorRect)
        # endregion
        # region FPS
        fps = 1 / (Time.time() - fpsTime)
        fpsTime = Time.time()
        fpsList.append(fps)
        temp = 0
        for element in fpsList:
            temp += element
        temp /= len(fpsList)
        while len(fpsList) > fpsQuality:
            fpsList.remove(fpsList[0])
        screen.blit(Font40.render(str(round(temp, 2)), 1, (255, 255, 255)), Rect(5, 0, 0, 0))
        # endregion
        # region health bar
        drawHealthBar()
        # endregion
        display.flip()
        if Time.time() - startTime > musicLen:
            Inst.stop()
            Vocals.stop()
            return False
        if health <= 0 and not noDying:
            Inst.stop()
            Vocals.stop()
            return death()
