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
arrow1Alpha = 1
arrow2Alpha = 1
character1 = None
character2 = None
character1Alpha = 1
character2Alpha = 1


def Main_game(musicName, options):
    global Inst
    global Vocals
    global chart
    global misses
    global health
    global BG
    global opponentAnimation
    global playerAnimation
    global hasPlayedMicDrop
    global combo
    global bpm
    global arrow1Alpha
    global arrow2Alpha
    global character1
    global character2
    global character1Alpha
    global character2Alpha

    misses = 0
    health = 50
    combo = 0

    init()

    K_a = options.keybinds[0]
    K_s = options.keybinds[1]
    K_w = options.keybinds[2]
    K_d = options.keybinds[3]
    K_LEFT = options.keybinds[4]
    K_DOWN = options.keybinds[5]
    K_UP = options.keybinds[6]
    K_RIGHT = options.keybinds[7]

    # region loading
    # region screen and loading screen
    screen = display.set_mode((0, 0), FULLSCREEN)
    mouse.set_visible(False)
    middleScreen = (display.Info().current_w // 2, display.Info().current_h // 2)

    def loadingscreen(progress, maxProgress, description=None):
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
            temp = (display.Info().current_w - 200) / maxProgress
            draw.rect(screen, (255, 255, 255), Rect(100, display.Info().current_h - 150, temp * progress, 50))
        if description is not None:
            temp = font.SysFont("Comic Sans MS", 30).render(description, 1, (255, 255, 255))
            temp1 = temp.get_rect()
            temp1.midtop = (middleScreen[0], display.Info().current_h - 85)
            screen.blit(temp, temp1)

        display.flip()

    loadingscreen(0, 6, "Loading variables")
    # endregion

    # region variables
    sys.setrecursionlimit(1000000)
    useMustHitSection = False
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
    accuracyPercentList = []

    Font40 = font.SysFont("Comic Sans MS", 40)
    Font25 = font.SysFont("Comic Sans MS", 25)

    longNotesChart = []

    opponentHitTimes = [-10 for _ in range(4)]
    opponentAnimation = ["Up", -10]
    playerAnimation = ["Up", -10]

    try:
        modifications = json.load(open(
            "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))[
            "modifications"]
    except:
        modifications = []

    try:
        dynamic_modifications = json.load(open(
            "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "modchart.json"))[
            "modchart"]
    except:
        dynamic_modifications = []

    transitionValuesList = []

    hasPlayedMicDrop = False

    loadedCharacters = {}
    # endregion

    # region images loading
    # region load images
    loadingscreen(1, 6, "Loading textures")

    def getAttibuteRect(data):
        return Rect(float(data.attrib["x"]), float(data.attrib["y"]), float(data.attrib["width"]),
                    float(data.attrib["height"]))

    def loadArrows(skinName):
        skinData = json.load(open("assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(skinName) + os.path.sep + "arrowData.json"))
        XMLPath = "assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(skinName) + os.path.sep + "arrowSkin.xml"
        XMLFile = ET.parse(XMLPath).getroot()
        imagePath = "assets" + os.path.sep + "Images" + os.path.sep + "ArrowStyles" + os.path.sep + "{0}".format(skinName) + os.path.sep + "arrowSkin.png"
        skinImage = image.load(imagePath).convert_alpha()
        result = {"arrowsSkin": [None for k in range(4)], "pressedArrowsSkins": [None for k in range(4)], "greyArrow": [None for k in range(4)], "longNotesImg": [None for k in range(4)], "longNotesEnd": [None for k in range(4)]}
        tempArrows = ["purple alone0000", "blue alone0000", "green alone0000", "red alone0000"]
        tempPressed = ["left press0000", "down press0000", "up press0000", "right press0000"]
        tempGrey = ["arrowLEFT0000", "arrowDOWN0000", "arrowUP0000", "arrowRIGHT0000"]
        tempLong = ["purple hold0000", "blue hold0000", "green hold0000", "red hold0000"]
        tempLongEnd = ["purple tail0000", "blue tail0000", "green tail0000", "red tail0000"]
        for data in XMLFile:
            if data.attrib["name"] in tempArrows:
                try:
                    temp = skinData["Size"]["arrowsSkin"][tempArrows.index(data.attrib["name"])]
                except:
                    temp = 1
                tempImage = skinImage.subsurface(getAttibuteRect(data)).convert_alpha()
                tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["arrowsSkin"][tempArrows.index(data.attrib["name"])] = tempImage
            if data.attrib["name"] in tempPressed:
                try:
                    temp = skinData["Size"]["pressedArrowsSkin"][tempPressed.index(data.attrib["name"])]
                except:
                    temp = 1
                tempImage = skinImage.subsurface(getAttibuteRect(data)).convert_alpha()
                tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["pressedArrowsSkins"][tempPressed.index(data.attrib["name"])] = tempImage
            if data.attrib["name"] in tempGrey:
                try:
                    temp = skinData["Size"]["greyArrow"][tempGrey.index(data.attrib["name"])]
                except:
                    temp = 1
                tempImage = skinImage.subsurface(getAttibuteRect(data)).convert_alpha()
                tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["greyArrow"][tempGrey.index(data.attrib["name"])] = tempImage
            if data.attrib["name"] in tempLong:
                try:
                    temp = skinData["Size"]["greyArrow"][tempLong.index(data.attrib["name"])]
                except:
                    temp = 1
                tempImage = skinImage.subsurface(getAttibuteRect(data)).convert_alpha()
                tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["longNotesImg"][tempLong.index(data.attrib["name"])] = tempImage
            if data.attrib["name"] in tempLongEnd:
                try:
                    temp = skinData["Size"]["greyArrow"][tempLongEnd.index(data.attrib["name"])]
                except:
                    temp = 1
                tempImage = skinImage.subsurface(getAttibuteRect(data)).convert_alpha()
                tempImage = transform.scale(tempImage, (tempImage.get_width() * temp, tempImage.get_height() * temp))
                result["longNotesEnd"][tempLongEnd.index(data.attrib["name"])] = tempImage
        return result

    class arrowTexture:
        def __init__(self, skinName):
            temp = loadArrows(skinName)
            self.arrowsSkins = temp["arrowsSkin"]
            for k in range(4):
                if self.arrowsSkins[k] is None:
                    self.arrowsSkins[k] = Surface((0, 0))
            self.pressedArrowsSkins = temp["pressedArrowsSkins"]
            for k in range(4):
                if self.pressedArrowsSkins[k] is None:
                    self.pressedArrowsSkins[k] = Surface((0, 0))
            self.greyArrow = temp["greyArrow"]
            for k in range(4):
                if self.greyArrow[k] is None:
                    self.greyArrow[k] = Surface((0, 0))
            self.longNotesImg = temp["longNotesImg"]
            for k in range(4):
                if self.longNotesImg[k] is None:
                    self.longNotesImg[k] = Surface((0, 0))
            if options.downscroll:
                for k in range(len(self.longNotesImg)):
                    self.longNotesImg[k] = transform.flip(self.longNotesImg[k], False, True)
            self.longNotesEnd = temp["longNotesEnd"]
            for k in range(4):
                if self.longNotesEnd[k] is None:
                    self.longNotesEnd[k] = Surface((0, 0))
            if options.downscroll:
                for k in range(len(self.longNotesEnd)):
                    self.longNotesEnd[k] = transform.flip(self.longNotesEnd[k], False, True)

    loadedArrowTextures = {"Main": arrowTexture(options.availableNoteStyles[options.selectedNoteStyle])}
    loadedArrowTextures["Player"] = copy.copy(loadedArrowTextures["Main"])
    loadedArrowTextures["Opponent"] = copy.copy(loadedArrowTextures["Main"])

    accuracyIndicatorImages = [
        transform.scale(image.load(
            "assets" + os.path.sep + "Images" + os.path.sep + "Accuracy indicator" + os.path.sep + "sick.png").convert_alpha(),
                        (225, 100)),
        transform.scale(image.load(
            "assets" + os.path.sep + "Images" + os.path.sep + "Accuracy indicator" + os.path.sep + "good.png").convert_alpha(),
                        (225, 100)),
        transform.scale(image.load(
            "assets" + os.path.sep + "Images" + os.path.sep + "Accuracy indicator" + os.path.sep + "bad.png").convert_alpha(),
                        (225, 100)),
        transform.scale(image.load(
            "assets" + os.path.sep + "Images" + os.path.sep + "Accuracy indicator" + os.path.sep + "shit.png").convert_alpha(),
                        (225, 100))]

    try:
        backgroundName = json.load(open(
            "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(musicName) + os.path.sep + "songData.json"))[
            "stage"]
    except:
        backgroundName = "None"

    if backgroundName != "None":
        Background = []
        width = display.Info().current_w
        height = display.Info().current_h
        for k in range(
                json.load(open(
                    "assets" + os.path.sep + "Images" + os.path.sep + "Backgrounds" + os.path.sep + "{0}".format(
                        backgroundName) + os.path.sep + "stageData.json"))["numFrames"]):
            if not display.Info().current_w / display.Info().current_h == 1920 / 1080:
                Background.append(transform.scale(
                    image.load(
                        "assets" + os.path.sep + "Images" + os.path.sep + "Backgrounds" + os.path.sep + "{0}".format(
                            backgroundName) + os.path.sep + "Background{0}.png".format(k)),
                    (1920, 1080)).convert_alpha())
            else:
                Background.append(transform.scale(
                    image.load(
                        "assets" + os.path.sep + "Images" + os.path.sep + "Backgrounds" + os.path.sep + "{0}".format(
                            backgroundName) + os.path.sep + "Background{0}.png".format(k)),
                    (display.Info().current_w, display.Info().current_h)).convert_alpha())
            if not singlePlayer:
                for x in range(len(Background)):
                    Background[x] = transform.scale(Background[x], (width, height))
    else:
        Background = [Font40.render("", 1, (255, 255, 255))]
    BGrect = Background[0].get_rect()
    BGrect.bottomright = (display.Info().current_w, display.Info().current_h)

    BFdead = image.load(
        "assets" + os.path.sep + "Images" + os.path.sep + "Death screen" + os.path.sep + "BF dead.png").convert_alpha()

    # endregion

    # region create image rect
    accuracyIndicatorRect = accuracyIndicatorImages[0].get_rect()
    accuracyIndicatorRect.center = (middleScreen[0], middleScreen[1] - 75)

    arrowRect = loadedArrowTextures["Main"].arrowsSkins[0].get_rect()

    deathScreenRect = BFdead.get_rect()
    deathScreenRect.midbottom = (middleScreen[0], display.Info().current_h - 50)
    # endregion

    musicList = json.load(open("assets" + os.path.sep + "MusicList.json"))["musics"]

    loadingscreen(2, 6, "Loading musics")

    # endregion

    # region music and chart loading
    deathScreenMusic = mixer.Sound(
        "assets" + os.path.sep + "Images" + os.path.sep + "Death screen" + os.path.sep + "gameOver.ogg")
    deathScreenMusicEnd = mixer.Sound(
        "assets" + os.path.sep + "Images" + os.path.sep + "Death screen" + os.path.sep + "gameOverEnd.ogg")
    deathScreenMusicStart = mixer.Sound(
        "assets" + os.path.sep + "Images" + os.path.sep + "Death screen" + os.path.sep + "micDrop.ogg")

    def open_file(music):
        global Inst
        global Vocals
        global chart
        global bpm
        Inst = mixer.Sound(
            "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "Inst.ogg")
        Vocals = mixer.Sound(
            "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "Voices.ogg")
        try:
            chart = json.load(open(
                "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "chart.json"))[
                "song"]["notes"]
        except:
            print("Chart is in incorrect format, formatting it")
            chart = {"song": json.load(open(
                "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "chart.json"))}
            json.dump(chart, open(
                "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "chart.json",
                "w"))
            chart = chart["song"]["notes"]
        try:
            bpm = json.load(open(
                "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(music) + os.path.sep + "chart.json"))[
                "song"]["bpm"]
            bpm = 60000 / bpm
        except error as e:
            print("No BPM detected, using 100 bpm")
            if options.debugMode:
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

    # endregion

    # region chart managment
    loadingscreen(3, 6, "Loading chart")

    class Note:
        def __init__(self, pos, column, side, length, noteId, textureName):
            self.pos = pos
            self.column = column
            self.side = side
            self.length = length
            self.id = noteId
            self.texture = textureName

    class LongNote:
        def __init__(self, pos, column, side, isEnd, textureName):
            self.pos = pos
            self.column = column
            self.side = side
            self.isEnd = isEnd
            self.texture = textureName

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

    if options.playAs == "Player":
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
            if isinstance(note[2], int) or isinstance(note[2], float):
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
                tempTextureName = tempUser
                notesChart.append(Note(note[0], tempDirection, tempUser, note[2], tempNoteId, tempTextureName))
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

    longNotesLen = 41 // options.selectedSpeed
    for note in notesChart:
        if note.length >= longNotesLen > 0 and int(round(note.length // longNotesLen)):
            tempGroup = LongNoteGroup(note.id)
            for k in range(1, int(round(note.length // longNotesLen))):
                tempGroup.notes.append(LongNote(note.pos + k * longNotesLen, note.column, note.side, False, note.side))
            tempGroup.notes.append(
                LongNote(note.pos + (note.length // longNotesLen) * longNotesLen, note.column, note.side, True,
                         note.side))
            tempGroup.setSize()
            longNotesChart.append(tempGroup)

    longNotesChart.sort(key=lambda s: s.id)
    for element in longNotesChart:
        element.notes.sort(key=lambda s: s.pos)

    # endregion
    # endregion

    # region characters
    loadingscreen(4, 6, "Loading characters")

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
        XMLpath = "assets" + os.path.sep + "Images" + os.path.sep + "Characters" + os.path.sep + "{0}".format(
            characterName) + os.path.sep + "character.xml"
        characterImage = image.load(
            "assets" + os.path.sep + "Images" + os.path.sep + "Characters" + os.path.sep + "{0}".format(
                characterName) + os.path.sep + "character.png").convert_alpha()
        XMLfile = ET.parse(XMLpath).getroot()
        result = [[] for _ in range(5)]
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
            if tempResult != "":
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
            if getNfirstCharacters(data.attrib["name"], 9) == "NOTE DOWN" and len(data.attrib["name"]) == 13:
                result[1].append(characterImage.subsurface(getAttibuteRect(data)))
            if getNfirstCharacters(data.attrib["name"], 7) == "NOTE UP" and len(data.attrib["name"]) == 11:
                result[2].append(characterImage.subsurface(getAttibuteRect(data)))
            if getNfirstCharacters(data.attrib["name"], 10) == "NOTE RIGHT" and len(data.attrib["name"]) == 14:
                result[3].append(characterImage.subsurface(getAttibuteRect(data)))
            if getNfirstCharacters(data.attrib["name"], 10) == "idle dance" and len(data.attrib["name"]) == 14:
                result[4].append(characterImage.subsurface(getAttibuteRect(data)))
        return result

    class Character:
        def __init__(self, name, characterNum, loadedFromModchart=False):
            if name != "None":
                if options.playAs == "Opponent":
                    if characterNum == 1:
                        temp = 2
                    else:
                        temp = 1
                else:
                    temp = characterNum
                # Load size and texture
                if not loadedFromModchart:
                    self.size = \
                        json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                            musicName) + os.path.sep + "songData.json"))["character{0}".format(temp)][
                            "size"]
                else:
                    self.size = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                        musicName) + os.path.sep + "songData.json"))["modchartCharacters"][name]["size"]
                # Parse XML file and get texture based on XML indications
                self.texture = getXmlData(name)
                # Get offset
                try:
                    self.offset = json.load(open(
                        "assets" + os.path.sep + "Images" + os.path.sep + "Characters" + os.path.sep + "{0}".format(
                            name) + os.path.sep + "offset.json"))["offset"]
                except:
                    self.offset = [[] for _ in range(5)]
                    for k in range(5):
                        for x in range(len(self.texture[k])):
                            self.offset[k].append([0, 0])
                try:
                    textureDirection = json.load(open(
                        "assets" + os.path.sep + "Images" + os.path.sep + "characters" + os.path.sep + "{0}".format(
                            name) + os.path.sep + "characterData.json"))["texture_direction"]
                except:
                    textureDirection = "Right"
                # Multiply offset by size
                for k in range(len(self.offset)):
                    for x in range(len(self.offset[k])):
                        self.offset[k][x][0] *= self.size[k][0]
                        self.offset[k][x][1] *= self.size[k][1]
                # Get pos
                if not loadedFromModchart:
                    self.pos = \
                        json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                            musicName) + os.path.sep + "songData.json"))["character{0}".format(temp)][
                            "pos"]
                else:
                    self.pos = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                        musicName) + os.path.sep + "songData.json"))["modchartCharacters"][name]["pos"]
                # Handle centered character
                try:
                    if not loadedFromModchart:
                        self.isCentered = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                            musicName) + os.path.sep + "songData.json"))["character{0}".format(characterNum)][
                            "isCentered"]
                    else:
                        self.isCenterd = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                            musicName) + os.path.sep + "songData.json"))["modchartCharacters"][name]["isCentered"]
                except:
                    self.isCentered = ["False", "False"]
                if self.isCentered[0] == "True" or self.isCentered[1] == "True":
                    try:
                        if not loadedFromModchart:
                            self.centeredOffset = json.load(open(
                                "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                                    musicName) + os.path.sep + "songData.json"))["character{0}".format(characterNum)][
                                "centeredOffset"]
                        else:
                            self.centeredOffset = json.load(open(
                                "assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                                    musicName) + os.path.sep + "songData.json"))["modchartCharacters"][name][
                                "centeredOffset"]
                    except:
                        self.centeredOffset = [0, 0]
                    if characterNum == 1:
                        if self.isCentered[0] == "True":
                            self.pos[0] = display.Info().current_w / 2 + self.centeredOffset[0]
                        if self.isCentered[1] == "True":
                            self.pos[1] = display.Info().current_h / 2 + self.centeredOffset[1]
                    else:
                        if self.isCentered[0] == "True":
                            self.pos[0] = display.Info().current_w / 2 - self.centeredOffset[0]
                        if self.isCentered[1] == "True":
                            self.pos[1] = display.info().current_h / 2 + self.centeredOffset[1]
                # Invert texture and offset when necessary
                if (textureDirection == "Left" and characterNum == 1) or (
                        textureDirection == "Right" and characterNum == 2):
                    for k in range(5):
                        for x in range(len(self.offset[k])):
                            self.offset[k][x][0] *= -1
                    for k in range(5):
                        for x in range(len(self.texture[k])):
                            self.texture[k][x] = transform.flip(self.texture[k][x], True, False)
                    temp1 = self.texture[0]
                    self.texture[0] = self.texture[3]
                    self.texture[3] = temp1
                    temp1 = self.offset[0]
                    self.offset[0] = self.offset[3]
                    self.offset[3] = temp1
                # Add offset to pos
                for k in range(5):
                    for x in range(len(self.offset[k])):
                        if characterNum == 1:
                            self.offset[k][x][0] = self.pos[0] + self.offset[k][x][0]
                            self.offset[k][x][1] = self.pos[1] + self.offset[k][x][1]
                        else:
                            self.offset[k][x][0] = self.pos[0] - self.offset[k][x][0]
                            self.offset[k][x][1] = self.pos[1] + self.offset[k][x][1]
                self.pos = self.offset
                # Scale texture to size
                for k in range(5):
                    for x in range(len(self.texture[k])):
                        self.texture[k][x] = transform.scale(self.texture[k][x], (
                            int(self.texture[k][x].get_width() * self.size[k][0]),
                            int(self.texture[k][x].get_height() * self.size[k][1])))
            # Handle no character
            else:
                self.texture = [[Font40.render("", 1, (255, 255, 255))] for _ in range(5)]
                self.pos = [[[0, 0]] for _ in range(5)]

    # Load characters
    if options.playAs == "Player":
        try:
            characterName = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                musicName) + os.path.sep + "songData.json"))["character1"]["Name"]
            try:
                alias = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                    musicName) + os.path.sep + "songData.json"))["character1"]["alias"]
            except:
                alias = None
            if alias is None:
                loadedCharacters[characterName] = Character(characterName, 1)
                character1 = loadedCharacters[characterName]
            else:
                loadedCharacters[alias] = Character(characterName, 1)
                character1 = loadedCharacters[alias]
        except error as e:
            print("Opponent character loading failed, skipping loading")
            if options.debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character1 = Character("None", 1)
        try:
            characterName = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                musicName) + os.path.sep + "songData.json"))["character2"]["Name"]
            try:
                alias = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                    musicName) + os.path.sep + "songData.json"))["character2"]["alias"]
            except:
                alias = None
            if alias is None:
                loadedCharacters[characterName] = Character(characterName, 2)
                character2 = loadedCharacters[characterName]
            else:
                loadedCharacters[alias] = Character(characterName, 2)
                character2 = loadedCharacters[alias]
        except:
            print("Player character loading failed, skipping loading")
            if options.debugMode:
                print("Debug mode stopped the program, printing error:")
                print(error)
            character2 = Character("None", 2)
    else:
        try:
            characterName = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                musicName) + os.path.sep + "songData.json"))["character1"]["Name"]
            try:
                alias = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                    musicName) + os.path.sep + "songData.json"))["character1"]["alias"]
            except:
                alias = None
            if alias is None:
                loadedCharacters[characterName] = Character(characterName, 1)
                character1 = loadedCharacters[characterName]
            else:
                loadedCharacters[alias] = Character(characterName, 1)
                character1 = loadedCharacters[alias]
        except error as e:
            print("Opponent character loading failed, skipping loading")
            if options.debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character1 = Character("None", 1)
        try:
            characterName = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                musicName) + os.path.sep + "songData.json"))["character2"]["Name"]
            try:
                alias = json.load(open("assets" + os.path.sep + "Musics" + os.path.sep + "{0}".format(
                    musicName) + os.path.sep + "songData.json"))["character2"]["alias"]
            except:
                alias = None
            if alias is None:
                loadedCharacters[characterName] = Character(characterName, 2)
                character2 = loadedCharacters[characterName]
            else:
                loadedCharacters[alias] = Character(characterName, 2)
                character2 = loadedCharacters[alias]
        except error as e:
            print("Player character loading failed, skipping loading")
            if options.debugMode:
                print("Debug mode stopped the program, printing error:")
                print(e)
            character2 = Character("None", 2)

    if singlePlayer:
        print("Resolution too low to display both characters, using singleplayer mode")
        character1 = Character("None", 2)

    # endregion
    # endregion

    # region screen and notes update
    loadingscreen(5, 6, "Loading modcharts ressources")

    def drawGreyNotes():
        width = display.Info().current_w
        height = display.Info().current_h
        currentTime = Time.time() - startTime
        if "hideNotes2" not in modifications:
            if K_a in keyPressed or K_LEFT in keyPressed:
                temp = loadedArrowTextures["Player"].pressedArrowsSkins[0].get_rect()
            else:
                temp = loadedArrowTextures["Player"].greyArrow[0].get_rect()
            if not options.downscroll:
                temp.center = (width - 615, 125)
            else:
                temp.center = (width - 615, height - 125)
            if K_a in keyPressed or K_LEFT in keyPressed:
                temp1 = copy.copy(loadedArrowTextures["Player"].pressedArrowsSkins[0])
                temp1.set_alpha(arrow2Alpha * 255)
                screen.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Player"].greyArrow[0]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                screen.blit(temp1, temp)
            if K_s in keyPressed or K_DOWN in keyPressed:
                temp = loadedArrowTextures["Player"].pressedArrowsSkins[1].get_rect()
            else:
                temp = loadedArrowTextures["Player"].greyArrow[1].get_rect()
            if not options.downscroll:
                temp.center = (width - 455, 125)
            else:
                temp.center = (width - 455, height - 125)
            if K_s in keyPressed or K_DOWN in keyPressed:
                temp1 = copy.copy(loadedArrowTextures["Player"].pressedArrowsSkins[1]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                screen.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Player"].greyArrow[1]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                screen.blit(temp1, temp)
            if K_w in keyPressed or K_UP in keyPressed:
                temp = loadedArrowTextures["Player"].pressedArrowsSkins[2].get_rect()
            else:
                temp = loadedArrowTextures["Player"].greyArrow[2].get_rect()
            if not options.downscroll:
                temp.center = (width - 295, 125)
            else:
                temp.center = (width - 295, height - 125)
            if K_w in keyPressed or K_UP in keyPressed:
                temp1 = copy.copy(loadedArrowTextures["Player"].pressedArrowsSkins[2]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                screen.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Player"].greyArrow[2]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                screen.blit(temp1, temp)
            if K_d in keyPressed or K_RIGHT in keyPressed:
                temp = loadedArrowTextures["Player"].pressedArrowsSkins[3].get_rect()
            else:
                temp = loadedArrowTextures["Player"].greyArrow[3].get_rect()
            if not options.downscroll:
                temp.center = (width - 135, 125)
            else:
                temp.center = (width - 135, height - 125)
            if K_d in keyPressed or K_RIGHT in keyPressed:
                temp1 = copy.copy(loadedArrowTextures["Player"].pressedArrowsSkins[3]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                screen.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Player"].greyArrow[3]).convert_alpha()
                temp1.set_alpha(arrow2Alpha * 255)
                screen.blit(temp1, temp)
        if not singlePlayer and "hideNotes1" not in modifications:
            if currentTime - opponentHitTimes[0] > 0.15:
                temp = loadedArrowTextures["Opponent"].greyArrow[0].get_rect()
            else:
                temp = loadedArrowTextures["Opponent"].pressedArrowsSkins[0].get_rect()
            if not options.downscroll:
                temp.center = (135, 125)
            else:
                temp.center = (135, height - 125)
            if currentTime - opponentHitTimes[0] > 0.15:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].greyArrow[0]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                screen.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].pressedArrowsSkins[0]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                screen.blit(temp1, temp)
            if currentTime - opponentHitTimes[1] > 0.15:
                temp = loadedArrowTextures["Opponent"].greyArrow[1].get_rect()
            else:
                temp = loadedArrowTextures["Opponent"].pressedArrowsSkins[1].get_rect()
            if not options.downscroll:
                temp.center = (295, 125)
            else:
                temp.center = (295, height - 125)
            if currentTime - opponentHitTimes[1] > 0.15:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].greyArrow[1]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                screen.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].pressedArrowsSkins[1]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                screen.blit(temp1, temp)
            if currentTime - opponentHitTimes[2] > 0.15:
                temp = loadedArrowTextures["Opponent"].greyArrow[2].get_rect()
            else:
                temp = loadedArrowTextures["Opponent"].pressedArrowsSkins[2].get_rect()
            if not options.downscroll:
                temp.center = (455, 125)
            else:
                temp.center = (455, height - 125)
            if currentTime - opponentHitTimes[2] > 0.15:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].greyArrow[2]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                screen.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].pressedArrowsSkins[2]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                screen.blit(temp1, temp)
            if currentTime - opponentHitTimes[3] > 0.15:
                temp = loadedArrowTextures["Opponent"].greyArrow[3].get_rect()
            else:
                temp = loadedArrowTextures["Opponent"].pressedArrowsSkins[3].get_rect()
            if not options.downscroll:
                temp.center = (615, 125)
            else:
                temp.center = (615, height - 125)
            if currentTime - opponentHitTimes[3] > 0.15:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].greyArrow[3]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                screen.blit(temp1, temp)
            else:
                temp1 = copy.copy(loadedArrowTextures["Opponent"].pressedArrowsSkins[3]).convert_alpha()
                temp1.set_alpha(arrow1Alpha * 255)
                screen.blit(temp1, temp)

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
                    if health < 0:
                        health = 0
                    accuracyPercentList.append(0)
                    combo = 0
                if 50 + (note.pos - currentTime * 1000) * options.selectedSpeed < display.Info().current_h + 100:
                    if not singlePlayer and "hideNotes1" not in modifications:
                        if note.side == "Opponent" and note.column == "Down":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[1].get_rect()
                            if not options.downscroll:
                                temp.center = (295, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    295, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[1]).convert_alpha()
                            temp1.set_alpha(arrow1Alpha * 255)
                            screen.blit(temp1, temp)
                        elif note.side == "Opponent" and note.column == "Left":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[0].get_rect()
                            if not options.downscroll:
                                temp.center = (135, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    135, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[0]).convert_alpha()
                            temp1.set_alpha(arrow1Alpha * 255)
                            screen.blit(temp1, temp)
                        elif note.side == "Opponent" and note.column == "Up":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[2].get_rect()
                            if not options.downscroll:
                                temp.center = (455, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    455, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[2]).convert_alpha()
                            temp1.set_alpha(arrow1Alpha * 255)
                            screen.blit(temp1, temp)
                        elif note.side == "Opponent" and note.column == "Right":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[3].get_rect()
                            if not options.downscroll:
                                temp.center = (615, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    615, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[3]).convert_alpha()
                            temp1.set_alpha(arrow1Alpha * 255)
                            screen.blit(temp1, temp)
                    if "hideNotes2" not in modifications:
                        if note.side == "Player" and note.column == "Down":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[1].get_rect()
                            if not options.downscroll:
                                temp.center = (
                                    width - 455, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    width - 455, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[1]).convert_alpha()
                            temp1.set_alpha(arrow2Alpha * 255)
                            screen.blit(temp1, temp)
                        elif note.side == "Player" and note.column == "Left":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[0].get_rect()
                            if not options.downscroll:
                                temp.center = (
                                    width - 615, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    width - 615, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[0]).convert_alpha()
                            temp1.set_alpha(arrow2Alpha * 255)
                            screen.blit(temp1, temp)
                        elif note.side == "Player" and note.column == "Up":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[2].get_rect()
                            if not options.downscroll:
                                temp.center = (
                                    width - 295, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    width - 295, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[2]).convert_alpha()
                            temp1.set_alpha(arrow2Alpha * 255)
                            screen.blit(temp1, temp)
                        elif note.side == "Player" and note.column == "Right":
                            temp = loadedArrowTextures[note.texture].arrowsSkins[3].get_rect()
                            if not options.downscroll:
                                temp.center = (
                                    width - 135, 125 + (note.pos - currentTime * 1000) * options.selectedSpeed)
                            else:
                                temp.center = (
                                    width - 135, height - 125 - (note.pos - currentTime * 1000) * options.selectedSpeed)
                            temp1 = copy.copy(loadedArrowTextures[note.texture].arrowsSkins[3]).convert_alpha()
                            temp1.set_alpha(arrow2Alpha * 255)
                            screen.blit(temp1, temp)

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
            if run and 50 + (noteGroup.notes[0].pos - currentTime * 1000) * options.selectedSpeed < height + 100:
                for longNote in noteGroup.notes:
                    if currentTime * 1000 - 133 >= longNote.pos:
                        if longNote.side == "Player":
                            if (noteGroup.size - len(noteGroup.notes)) / noteGroup.size >= 0.75:
                                noteGroup.canDealDamage = False
                            if noteGroup.canDealDamage:
                                misses += 1
                                health -= 4
                                if health < 0:
                                    health = 0
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
                        if 50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed < height + 100:
                            if not singlePlayer and longNote.side == "Opponent" and "hideNotes1" not in modifications:
                                if longNote.column == "Down":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            220 + 125,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            220 + 125,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        temp1 = copy.copy(loadedArrowTextures[longNote.texture].longNotesEnd[1]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        screen.blit(temp1, temp)
                                    else:
                                        temp1 = copy.copy(loadedArrowTextures[longNote.texture].longNotesImg[1]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        screen.blit(temp1, temp)
                                if longNote.column == "Left":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (60 + 125, 50 + (
                                                longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            60 + 125,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        temp1 = copy.copy(loadedArrowTextures[longNote.texture].longNotesEnd[0]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        screen.blit(temp1, temp)
                                    else:
                                        temp1 = copy.copy(loadedArrowTextures[longNote.texture].longNotesImg[0]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        screen.blit(temp1, temp)
                                if longNote.column == "Up":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            380 + 125,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            380 + 125,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        temp1 = copy.copy(loadedArrowTextures[longNote.texture].longNotesEnd[2]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        screen.blit(temp1, temp)
                                    else:
                                        temp1 = copy.copy(loadedArrowTextures[longNote.texture].longNotesImg[2]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        screen.blit(temp1, temp)
                                if longNote.column == "Right":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            540 + 125,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            540 + 125,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        temp1 = copy.copy(loadedArrowTextures[longNote.texture].longNotesEnd[3]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        screen.blit(temp1, temp)
                                    else:
                                        temp1 = copy.copy(loadedArrowTextures[longNote.texture].longNotesImg[3]).convert_alpha()
                                        temp1.set_alpha(arrow1Alpha * 255)
                                        screen.blit(temp1, temp)
                            if longNote.side == "Player" and "hideNotes2" not in modifications:
                                if longNote.column == "Up":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            width - 220 - 25,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            width - 220 - 25,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        img = copy.copy(loadedArrowTextures[longNote.texture].longNotesEnd[2]).convert_alpha()
                                    else:
                                        img = copy.copy(loadedArrowTextures[longNote.texture].longNotesImg[2]).convert_alpha()
                                    if arrow2Alpha:
                                        if transparent:
                                            img.set_alpha(100)
                                    else:
                                        img.set_alpha(arrow2Alpha * 255)
                                    screen.blit(img, temp)
                                if longNote.column == "Down":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            width - 380 - 25,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            width - 380 - 25,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        img = copy.copy(loadedArrowTextures[longNote.texture].longNotesEnd[1]).convert_alpha()
                                    else:
                                        img = copy.copy(loadedArrowTextures[longNote.texture].longNotesImg[1]).convert_alpha()
                                    if arrow2Alpha == 1:
                                        if transparent:
                                            img.set_alpha(100)
                                    else:
                                        img.set_alpha(arrow2Alpha * 255)
                                    screen.blit(img, temp)
                                if longNote.column == "Left":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            width - 540 - 25,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            width - 540 - 25,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        img = copy.copy(loadedArrowTextures[longNote.texture].longNotesEnd[0]).convert_alpha()
                                    else:
                                        img = copy.copy(loadedArrowTextures[longNote.texture].longNotesImg[0]).convert_alpha()
                                    if arrow2Alpha == 1:
                                        if transparent:
                                            img.set_alpha(100)
                                    else:
                                        img.set_alpha(arrow2Alpha * 255)
                                    screen.blit(img, temp)
                                if longNote.column == "Right":
                                    temp = arrowRect
                                    if not options.downscroll:
                                        temp.center = (
                                            width - 60 - 25,
                                            50 + (longNote.pos - currentTime * 1000) * options.selectedSpeed + 100)
                                    else:
                                        temp.center = (
                                            width - 60 - 25,
                                            height - 50 - (longNote.pos - currentTime * 1000) * options.selectedSpeed)
                                    if longNote.isEnd:
                                        img = copy.copy(loadedArrowTextures[longNote.texture].longNotesEnd[3]).convert_alpha()
                                    else:
                                        img = copy.copy(loadedArrowTextures[longNote.texture].longNotesImg[3]).convert_alpha()
                                    if arrow2Alpha == 1:
                                        if transparent:
                                            img.set_alpha(100)
                                    else:
                                        img.set_alpha(arrow2Alpha * 255)
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
        if not options.downscroll:
            draw.rect(screen, (255, 255, 255), Rect(45, height - 115, width - 90, 60))
        else:
            draw.rect(screen, (255, 255, 255), Rect(45, 55, width - 90, 60))
        if health < 100:
            if not options.downscroll:
                draw.rect(screen, (255, 0, 0), Rect(50, height - 110, (width - 100) / 100 * (100 - health), 50))
            else:
                draw.rect(screen, (255, 0, 0), Rect(50, 60, (width - 100) / 100 * (100 - health), 50))
        if health > 0:
            if not options.downscroll:
                draw.rect(screen, (0, 255, 0),
                          Rect(50 + (width - 100) / 100 * (100 - health), height - 110, (width - 100) / 100 * health,
                               50))
            else:
                draw.rect(screen, (0, 255, 0),
                          Rect(50 + (width - 100) / 100 * (100 - health), 60, (width - 100) / 100 * health, 50))

    def drawCharacters():
        currentTime = Time.time() - startTime
        #   Character 1
        # Idle animation
        if currentTime - opponentAnimation[1] >= 0.75:
            animationFrame = int((((Time.time() - startTime) * 1000 / 2) % bpm) / bpm * len(character1.texture[4]))
            temp = character1.texture[4][animationFrame].get_rect()
            temp.midbottom = [character1.pos[4][animationFrame][0],
                              display.Info().current_h - character1.pos[4][animationFrame][1]]
            temp1 = copy.copy(character1.texture[4][animationFrame])
            temp1.set_alpha(character1Alpha * 255)
            screen.blit(temp1, temp)
        # Directional animation
        else:
            animationDirection = ["Left", "Down", "Up", "Right"].index(opponentAnimation[0])
            if currentTime - opponentAnimation[1] < 0.45:
                tempTime = 0.45 / len(character1.texture[animationDirection])
                numFrame = int((currentTime - opponentAnimation[1]) // tempTime)
            else:
                numFrame = len(character1.texture[animationDirection]) - 1
            temp = character1.texture[animationDirection][numFrame].get_rect()
            temp.midbottom = [character1.pos[animationDirection][numFrame][0],
                              display.Info().current_h - character1.pos[animationDirection][numFrame][1]]
            temp1 = copy.copy(character1.texture[animationDirection][numFrame])
            temp1.set_alpha(character1Alpha * 255)
            screen.blit(temp1, temp)
        #   Character 2
        # Idle animation
        if currentTime - playerAnimation[1] >= 0.75:
            animationFrame = int((((Time.time() - startTime) * 1000 / 2) % bpm) / bpm * len(character2.texture[4]))
            temp = character2.texture[4][animationFrame].get_rect()
            temp.midbottom = [display.Info().current_w - character2.pos[4][animationFrame][0],
                              display.Info().current_h - character2.pos[4][animationFrame][1]]
            temp1 = copy.copy(character2.texture[4][animationFrame])
            temp1.set_alpha(character2Alpha * 255)
            screen.blit(temp1, temp)
        # Directional animation
        else:
            animationDirection = ["Left", "Down", "Up", "Right"].index(playerAnimation[0])
            if currentTime - playerAnimation[1] < 0.45:
                tempTime = 0.45 / len(character2.texture[animationDirection])
                numFrame = int((currentTime - playerAnimation[1]) // tempTime)
            else:
                numFrame = len(character2.texture[animationDirection]) - 1
            temp = character2.texture[animationDirection][numFrame].get_rect()
            temp.midbottom = [display.Info().current_w - character2.pos[animationDirection][numFrame][0],
                              display.Info().current_h - character2.pos[animationDirection][numFrame][1]]
            temp1 = copy.copy(character2.texture[animationDirection][numFrame])
            temp1.set_alpha(character2Alpha * 255)
            screen.blit(temp1, temp)

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
        if not options.downscroll:
            draw.rect(screen, (255, 255, 255), Rect(400, 5, width - 800, 40))
            draw.rect(screen, (0, 0, 0), Rect(402, 7, width - 804, 36))
        else:
            draw.rect(screen, (255, 255, 255), Rect(400, height - 5 - 40, width - 800, 40))
            draw.rect(screen, (0, 0, 0), Rect(402, height - 7 - 36, width - 804, 36))
        temp = int(round(musicLen - (Time.time() - startTime), 0))
        if not options.downscroll:
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
        if not options.downscroll:
            temp1.midtop = (middleScreen[0], 5)
        else:
            temp1.midbottom = (middleScreen[0], height - 10)
        screen.blit(temp, temp1)

    class transitionValue:
        def __init__(self, variable, startValue, endValue, startTime1, endTime):
            self.variable = variable
            self.startValue = startValue
            self.endValue = endValue
            self.startTime = startTime1
            self.endTime = endTime
            self.isActive = True

        def update(self):
            global arrow1Alpha
            global arrow2Alpha
            global character1Alpha
            global character2Alpha
            currentTime = Time.time() - startTime
            if self.endTime >= currentTime >= self.startTime:
                vector = self.endValue - self.startValue
                progress = (currentTime - self.startTime) / (self.endTime - self.startTime)
                value = self.startValue + (vector * progress)
                if self.variable == "arrow1Alpha":
                    arrow1Alpha = value
                elif self.variable == "arrow2Alpha":
                    arrow2Alpha = value
                elif self.variable == "character1Alpha":
                    character1Alpha = value
                elif self.variable == "character2Alpha":
                    character2Alpha = value
            elif currentTime > self.endTime:
                if self.variable == "arrow1Alpha":
                    arrow1Alpha = self.endValue
                elif self.variable == "arrow2Alpha":
                    arrow2Alpha = self.endValue
                elif self.variable == "character1Alpha":
                    character1Alpha = self.endValue
                elif self.variable == "character2Alpha":
                    character2Alpha = self.endValue
                self.isActive = False

    def update_modifications(modifications, dynamic_modifications):
        global character1
        global character2
        currentTime = Time.time() - startTime
        currentTime *= 1000
        for mod in dynamic_modifications:
            if mod["type"] == "add/remove" and mod["pos"] >= currentTime:
                if mod["action"] == "add":
                    modifications.append(mod["name"])
                elif mod["action"] == "remove":
                    if mod["name"] in modifications:
                        modifications.remove(mod["name"])
                dynamic_modifications.remove(mod)
            if mod["type"] == "arrowAlphaChange":
                try:
                    temp = mod["pos"]
                except:
                    temp = 0
                if currentTime >= temp:
                    if mod["player"] == 1:
                        transitionValuesList.append(
                            transitionValue("arrow1Alpha", mod["startValue"], mod["endValue"], mod["startTime"],
                                            mod["endTime"]))
                    if mod["player"] == 2:
                        transitionValuesList.append(
                            transitionValue("arrow2Alpha", mod["startValue"], mod["endValue"], mod["startTime"],
                                            mod["endTime"]))
                    dynamic_modifications.remove(mod)
            if mod["type"] == "characterAlphaChange":
                try:
                    temp = mod["pos"]
                except:
                    temp = 0
                if currentTime >= temp:
                    if mod["player"] == 1:
                        transitionValuesList.append(
                            transitionValue("character1Alpha", mod["startValue"], mod["endValue"], mod["startTime"],
                                            mod["endTime"]))
                    if mod["player"] == 2:
                        transitionValuesList.append(
                            transitionValue("character2Alpha", mod["startValue"], mod["endValue"], mod["startTime"],
                                            mod["endTime"]))
                    dynamic_modifications.remove(mod)
            if mod["type"] == "changeCharacter":
                try:
                    temp = mod["pos"]
                except:
                    temp = 0
                if currentTime >= temp:
                    if mod["player"] == 1:
                        character1 = loadedCharacters[mod["name"]]
                    elif mod["player"] == 2:
                        character2 = loadedCharacters[mod["name"]]
                    dynamic_modifications.remove(mod)
            if mod["type"] == "changeArrowTexture":
                try:
                    temp = mod["pos"]
                except:
                    temp = 0
                if currentTime >= temp:
                    if mod["player"] == 1:
                        loadedArrowTextures["Opponent"] = loadedArrowTextures[mod["name"]]
                    elif mod["player"] == 2:
                        loadedArrowTextures["Player"] = loadedArrowTextures[mod["name"]]
                    dynamic_modifications.remove(mod)
            if mod["type"] == "Organiser":
                update_modifications(modifications, mod["modchart"])

    def update_transitionValue():
        for element in transitionValuesList:
            element.update()
            if not element.isActive:
                transitionValuesList.remove(element)

    def modchartLoading():
        for mod in dynamic_modifications:
            if mod["type"] == "characterLoading":
                try:
                    alias = mod["alias"]
                except:
                    alias = None
                if alias is None:
                    loadedCharacters[mod["name"]] = Character(mod["name"], mod["player"], True)
                else:
                    loadedCharacters[mod["alias"]] = Character(mod["name"], mod["player"], True)
            if mod["type"] == "arrowTextureLoading":
                loadedArrowTextures[mod["loadedName"]] = arrowTexture(mod["textureName"])

    modchartLoading()

    loadingscreen(6, 6, "Finishing...")
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
        if health > 100:
            health = 100
        screen.fill((0, 0, 0))
        backgroundFrameNum = int((((Time.time() - startTime) * 1000 / 2) % bpm) / bpm * len(Background))
        screen.blit(Background[backgroundFrameNum], BGrect)
        update_modifications(modifications, dynamic_modifications)
        update_transitionValue()
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
        if options.coloredInfo:
            text1 = "Combo: {0} | Misses: {1} | ".format(combo, misses)
            text2 = "Accuracy: {0}".format(tempAccuracy)
            if options.healthFormat == "Healthbar":
                text3 = ""
            else:
                text3 = " | Health: {0}%".format(round(health, 2))
            biggest_height = 0
            tmp_width = 0
            tempText1 = text1 + text2 + text3
            for k in range(len(tempText1)):
                tmp = Font40.render(tempText1[k], 1, (255, 255, 255)).get_rect()
                if tmp.height > biggest_height:
                    biggest_height = tmp.height
                tmp_width += tmp.width
            tempText = Surface((tmp_width, biggest_height), flags=SRCALPHA)
            tempText = tempText.convert_alpha()
            tempText.fill((0, 0, 0, 0))
            current_x = 0
            for k in range(len(text1)):
                tempLetter = Font40.render(text1[k], 1, (255, 255, 255))
                tempText.blit(tempLetter, (current_x, 0))
                current_x += tempLetter.get_rect().width
            if len(accuracyPercentList) == 0:
                tempColor = (255, 255, 255)
            elif round(temp * 100, 2) >= 85:
                tempColor = (0, 255, 0)
            elif 85 >= round(temp * 100, 2) > 70:
                tempColor = (210, 139, 0)
            else:
                tempColor = (255, 0, 0)
            for k in range(len(text2)):
                tempLetter = Font40.render(text2[k], 1, tempColor)
                tempText.blit(tempLetter, (current_x, 0))
                current_x += tempLetter.get_rect().width
            if health >= 75:
                tempColor = (0, 255, 0)
            elif 75 > health >= 50:
                tempColor = (210, 139, 0)
            elif health < 50:
                tempColor = (255, 0, 0)
            else:
                tempColor = (255, 255, 255)
            for k in range(len(text3)):
                if k > 1:
                    tempLetter = Font40.render(text3[k], 1, tempColor)
                else:
                    tempLetter = Font40.render(text3[k], 1, (255, 255, 255))
                tempText.blit(tempLetter, (current_x, 0))
                current_x += tempLetter.get_rect().width
            temp1 = tempText.get_rect()
            if not options.downscroll:
                temp1.midbottom = (middleScreen[0], display.Info().current_h - 5)
            else:
                temp1.midtop = (middleScreen[0], 0)
            screen.blit(tempText, temp1)
        else:
            if options.healthFormat == "Healthbar":
                temp = Font40.render("Combo: {0} | Misses: {1} | Accuracy: {2}".format(combo, misses, tempAccuracy), 1,
                                     (255, 255, 255))
            else:
                temp = Font40.render(
                    "Combo: {0} | Misses: {1} | Accuracy: {2} | Health: {3}%".format(combo, misses, tempAccuracy,
                                                                                     round(health, 2)), 1,
                    (255, 255, 255))
            temp1 = temp.get_rect()
            if not options.downscroll:
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
        if options.healthFormat == "Healthbar":
            drawHealthBar()
        # endregion
        display.flip()
        if Time.time() - startTime > musicLen:
            Inst.stop()
            Vocals.stop()
            return False
        if health <= 0 and not options.noDying:
            Inst.stop()
            Vocals.stop()
            return death()
