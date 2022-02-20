from pygame import *
import json
from random import *
import time as Time
import cProfile
import sys
from Game import Main_game

init()

screen = display.set_mode((0, 0), FULLSCREEN)
middleScreen = (display.Info().current_w // 2, display.Info().current_h // 2)

if not display.Info().current_w / display.Info().current_h == 1920 / 1080:
    menuBG = transform.scale(image.load("assets\Images\menuBG.png"), (1920, 1080))
else:
    menuBG = transform.scale(image.load("assets\Images\menuBG.png"),
                             (display.Info().current_w, display.Info().current_h))

BGrect = menuBG.get_rect()
BGrect.center = (middleScreen[0], middleScreen[1])

mouse.set_visible(False)

musicList = json.load(open("assets\MusicList.json"))["musics"]
availableNoteStyles = json.load(open("assets/NoteStyles.json"))["NoteStyles"]

Font100 = font.SysFont("Comic Sans MS", 100)
FNFfont = font.Font("assets\Friday Night Funkin Font.ttf", 100)

options = json.load(open("assets\options.json"))

selectedMusic = 0
selectedOption = 0
selectedMain = 0
selectedKeybind = 0
currentMenu = "Main"

selectedSpeed = options["selectedSpeed"]
playAs = options["playAs"]
selectedNoteStyle = options["selectedNoteStyle"]
noDying = options["noDying"] == "True"

K_a = options["keybinds"][0]
K_s = options["keybinds"][1]
K_w = options["keybinds"][2]
K_d = options["keybinds"][3]
K_LEFT = options["keybinds"][4]
K_DOWN = options["keybinds"][5]
K_UP = options["keybinds"][6]
K_RIGHT = options["keybinds"][7]

menuMusic = mixer.Sound("assets\menuMusic.ogg")

preventDoubleEnter = False


def drawMusics():
    for k in range(len(musicList)):
        temp = FNFfont.render(musicList[k], 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1] + 200 * (k - selectedMusic))
        screen.blit(temp, temp1)


def drawOptions():
    tempText = ["Speed: {0}".format(selectedSpeed), "Play as: {0}".format(playAs), "No dying: {0}".format(noDying),
                "Note style: {0}".format(availableNoteStyles[selectedNoteStyle]), "Keybinds"]
    for k in range(len(tempText)):
        temp = Font100.render(tempText[k], 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1] + 200 * (k - selectedOption))
        screen.blit(temp, temp1)


def drawMain():
    tempText = ["Play", "Options"]
    for k in range(len(tempText)):
        temp = FNFfont.render(tempText[k], 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1] + 200 * (k - selectedMain))
        screen.blit(temp, temp1)


def drawKeybinds():
    tempList = [key.name(K_a), key.name(K_s), key.name(K_w), key.name(K_d), key.name(K_LEFT), key.name(K_DOWN),
                key.name(K_UP), key.name(K_RIGHT), "None"]
    for k in range(len(tempList)):
        tempList[k] = tempList[k].title()
    tempText = ["Left: {0}", "Down: {0}", "Up: {0}", "Right: {0}", "Left 2: {0}", "Down 2: {0}", "Up 2: {0}",
                "Right 2: {0}", "Reset keybinds"]
    for k in range(len(tempText)):
        tempText[k] = tempText[k].format(tempList[k])
        temp = Font100.render(tempText[k], 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1] + 200 * (k - selectedKeybind))
        screen.blit(temp, temp1)


def drawEditKeybinds():
    temp = Font100.render("Press a key to edit keybind", 1, (255, 255, 255))
    temp1 = temp.get_rect()
    temp1.midbottom = middleScreen
    screen.blit(temp, temp1)
    temp = Font100.render("(Escape to cancel)", 1, (255, 255, 255))
    temp1 = temp.get_rect()
    temp1.midtop = middleScreen
    screen.blit(temp, temp1)


def saveOptions():
    global options
    options["selectedSpeed"] = selectedSpeed
    options["playAs"] = playAs
    if noDying:
        options["noDying"] = True
    else:
        options["noDying"] = False
    options["selectedNoteStyle"] = selectedNoteStyle
    options["keybinds"] = [K_a, K_s, K_w, K_d, K_LEFT, K_DOWN, K_UP, K_RIGHT]
    json.dump(options, open("assets\options.json", "w"))


menuMusic.play(-1)

while True:
    for events in event.get():
        if events.type == QUIT or (events.type == KEYDOWN and events.key == K_ESCAPE):
            if currentMenu == "Main":
                saveOptions()
                quit()
                exit()
            else:
                if currentMenu == "Keybinds":
                    currentMenu = "Options"
                elif currentMenu == "Edit keybind":
                    currentMenu = "Keybinds"
                else:
                    currentMenu = "Main"
        if events.type == KEYDOWN and events.key == K_RETURN:
            if currentMenu == "Select music":
                menuMusic.stop()
                restart = True
                while restart:
                    Inst = None
                    Vocals = None
                    chart = None
                    misses = 0
                    health = 50
                    BG = None
                    opponentAnimation = ["Up", -10]
                    playerAnimation = ["Up", -10]
                    hasPlayedMicDrop = False
                    restart = Main_game(musicList[selectedMusic], selectedSpeed, playAs, noDying,
                                        availableNoteStyles[selectedNoteStyle],
                                        [K_a, K_s, K_w, K_d, K_LEFT, K_DOWN, K_UP, K_RIGHT])
                menuMusic.play(-1)
            if currentMenu == "Main":
                if selectedMain == 0:
                    currentMenu = "Select music"
                if selectedMain == 1:
                    currentMenu = "Options"
                    preventDoubleEnter = True
        if events.type == KEYDOWN:
            if currentMenu == "Select music":
                if (events.key == K_w or events.key == K_UP) and selectedMusic > 0:
                    selectedMusic -= 1
                if (events.key == K_s or events.key == K_DOWN) and selectedMusic < len(musicList) - 1:
                    selectedMusic += 1
            if currentMenu == "Options":
                if (events.key == K_w or events.key == K_UP) and selectedOption > 0:
                    selectedOption -= 1
                if (events.key == K_s or events.key == K_DOWN) and selectedOption < 4:
                    selectedOption += 1
                if selectedOption == 0:
                    if (events.key == K_a or events.key == K_LEFT) and selectedSpeed > 0.1:
                        selectedSpeed -= 0.1
                        selectedSpeed = round(selectedSpeed, 1)
                    if events.key == K_d or events.key == K_RIGHT:
                        selectedSpeed += 0.1
                        selectedSpeed = round(selectedSpeed, 1)
                if selectedOption == 1:
                    if events.key == K_a or events.key == K_LEFT or events.key == K_d or events.key == K_RIGHT:
                        if playAs == "Player":
                            playAs = "Opponent"
                        else:
                            playAs = "Player"
                if selectedOption == 2:
                    if events.key == K_a or events.key == K_LEFT or events.key == K_d or events.key == K_RIGHT:
                        if noDying:
                            noDying = False
                        else:
                            noDying = True
                if selectedOption == 3:
                    if (events.key == K_a or events.key == K_LEFT) and selectedNoteStyle > 0:
                        selectedNoteStyle -= 1
                    if (events.key == K_d or events.key == K_RIGHT) and selectedNoteStyle < len(
                            availableNoteStyles) - 1:
                        selectedNoteStyle += 1
                if selectedOption == 4:
                    if events.key == K_RETURN and not preventDoubleEnter:
                        currentMenu = "Keybinds"
                        preventDoubleEnter = True
            if currentMenu == "Main":
                if (events.key == K_w or events.key == K_UP) and selectedMain > 0:
                    selectedMain -= 1
                if (events.key == K_s or events.key == K_DOWN) and selectedMain < 1:
                    selectedMain += 1
            if currentMenu == "Keybinds":
                if (events.key == K_w or events.key == K_UP) and selectedKeybind > 0:
                    selectedKeybind -= 1
                if (events.key == K_s or events.key == K_DOWN) and selectedKeybind < 8:
                    selectedKeybind += 1
                if events.key == K_RETURN and not preventDoubleEnter and selectedKeybind < 8:
                    currentMenu = "Edit keybind"
                if events.key == K_RETURN and not preventDoubleEnter and selectedKeybind == 8:
                    K_a = 97
                    K_s = 115
                    K_w = 119
                    K_d = 100
                    K_LEFT = 1073741904
                    K_DOWN = 1073741905
                    K_UP = 1073741906
                    K_RIGHT = 1073741903
            if currentMenu == "Edit keybind":
                if events.key == K_ESCAPE:
                    currentMenu = "Keybinds"
                elif events.key not in [K_RETURN, K_BACKSPACE, K_ESCAPE, K_SPACE, KMOD_SHIFT, KMOD_CTRL, KMOD_ALT,
                                        KMOD_CAPS] and events.key not in [K_a, K_s, K_w, K_d, K_LEFT, K_DOWN, K_UP,
                                                                          K_RIGHT]:
                    temp = False
                    if selectedKeybind == 0:
                        K_a = events.key
                        temp = True
                    if selectedKeybind == 1:
                        K_s = events.key
                        temp = True
                    if selectedKeybind == 2:
                        K_w = events.key
                        temp = True
                    if selectedKeybind == 3:
                        K_d = events.key
                        temp = True
                    if selectedKeybind == 4:
                        K_LEFT = events.key
                        temp = True
                    if selectedKeybind == 5:
                        K_DOWN = events.key
                        temp = True
                    if selectedKeybind == 6:
                        K_UP = events.key
                        temp = True
                    if selectedKeybind == 7:
                        K_RIGHT = events.key
                        temp = True
                    if temp:
                        currentMenu = "Keybinds"
        preventDoubleEnter = False
    screen.fill((0, 0, 0))
    screen.blit(menuBG, BGrect)
    if currentMenu == "Select music":
        drawMusics()
    elif currentMenu == "Options":
        drawOptions()
    elif currentMenu == "Main":
        drawMain()
    elif currentMenu == "Keybinds":
        drawKeybinds()
    elif currentMenu == "Edit keybind":
        drawEditKeybinds()
    display.flip()
