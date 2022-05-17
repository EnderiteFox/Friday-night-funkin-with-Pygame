from pygame import *
import json
from random import *
from Game import Main_game
import os
from Offset_editor import offset_editor

init()

screen = display.set_mode((0, 0), FULLSCREEN)
middleScreen = (display.Info().current_w // 2, display.Info().current_h // 2)

if not display.Info().current_w / display.Info().current_h == 1920 / 1080:
    menuBG = transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "menuBG.png"), (1920, 1080))
else:
    menuBG = transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "menuBG.png"),
                             (display.Info().current_w, display.Info().current_h))

BGrect = menuBG.get_rect()
BGrect.center = (middleScreen[0], middleScreen[1])

mouse.set_visible(False)

musicList = json.load(open("assets" + os.path.sep + "MusicList.json"))["musics"]
availableNoteStyles = json.load(open("assets" + os.path.sep + "NoteStyles.json"))["NoteStyles"]

Font100 = font.SysFont("Comic Sans MS", 100)
Font125 = font.SysFont("Comic Sans MS", 125)
FNFfont = font.Font("assets" + os.path.sep + "Friday Night Funkin Font.ttf", 100)
FNFfont125 = font.Font("assets" + os.path.sep + "Friday Night Funkin Font.ttf", 125)


class Options:
    def __init__(self):
        self.update()

    def update(self):
        global availableNoteStyles
        global K_a, K_s, K_w, K_d
        global K_LEFT, K_DOWN, K_UP, K_RIGHT
        self.availableNoteStyles = availableNoteStyles
        self.arguments = json.load(open("assets" + os.path.sep + "options.json"))
        self.selectedSpeed = self.arguments["selectedSpeed"]
        self.playAs = self.arguments["playAs"]
        if self.arguments["selectedNoteStyle"] < len(availableNoteStyles):
            self.selectedNoteStyle = self.arguments["selectedNoteStyle"]
        else:
            self.selectedNoteStyle = 0
        self.noDying = self.arguments["noDying"] == "True"
        self.downscroll = self.arguments["downscroll"] == "True"
        self.debugMode = self.arguments["debug_mode"] == "True"
        K_a = self.arguments["keybinds"][0]
        K_s = self.arguments["keybinds"][1]
        K_w = self.arguments["keybinds"][2]
        K_d = self.arguments["keybinds"][3]
        K_LEFT = self.arguments["keybinds"][4]
        K_DOWN = self.arguments["keybinds"][5]
        K_UP = self.arguments["keybinds"][6]
        K_RIGHT = self.arguments["keybinds"][7]
        self.keybinds = [K_a, K_s, K_w, K_d, K_LEFT, K_DOWN, K_UP, K_RIGHT]
        self.healthFormat = self.arguments["health_format"]
        self.coloredInfo = self.arguments["colored_info"] == "True"

    def saveOptions(self):
        global K_a, K_s, K_w, K_d
        global K_LEFT, K_DOWN, K_UP, K_RIGHT
        self.arguments["selectedSpeed"] = self.selectedSpeed
        self.arguments["playAs"] = self.playAs
        self.arguments["noDying"] = str(self.noDying)
        self.arguments["debug_mode"] = str(self.debugMode)
        self.arguments["downscroll"] = str(self.downscroll)
        self.arguments["selectedNoteStyle"] = self.selectedNoteStyle
        self.arguments["keybinds"] = [K_a, K_s, K_w, K_d, K_LEFT, K_DOWN, K_UP, K_RIGHT]
        self.arguments["health_format"] = self.healthFormat
        self.arguments["colored_info"] = str(self.coloredInfo)
        json.dump(self.arguments, open("assets" + os.path.sep + "options.json", "w"))


options = Options()

selectedMusic = 0
selectedOption = 0
selectedMain = 0
selectedKeybind = 0
currentMenu = "Main"

menuMusic = mixer.Sound("assets" + os.path.sep + "menuMusic.ogg")

preventDoubleEnter = False


def drawMusics():
    for k in range(len(musicList)):
        if k == selectedMusic:
            temp = FNFfont125.render(musicList[k], 1, (255, 255, 255))
        else:
            temp = FNFfont.render(musicList[k], 1, (200, 200, 200))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1] + 200 * (k - selectedMusic))
        screen.blit(temp, temp1)


def drawOptions():
    tempText = ["Speed: {0}".format(options.selectedSpeed), "Play as: {0}".format(options.playAs),
                "No dying: {0}".format(options.noDying),
                "Note style: {0}".format(availableNoteStyles[options.selectedNoteStyle]),
                "Downscroll: {0}".format(options.downscroll), "Debug mode: {0}".format(options.debugMode),
                "Health: {0}".format("Health bar" if options.healthFormat == "Healthbar" else "Info bar"),
                "Colored info bar: {0}".format(options.coloredInfo), "Keybinds", "Offset editor"]
    for k in range(len(tempText)):
        if k == selectedOption:
            temp = Font125.render(tempText[k], 1, (255, 255, 255))
        else:
            temp = Font100.render(tempText[k], 1, (200, 200, 200))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1] + 200 * (k - selectedOption))
        screen.blit(temp, temp1)


def drawMain():
    tempText = ["Play", "Options"]
    for k in range(len(tempText)):
        if k == selectedMain:
            temp = FNFfont125.render(tempText[k], 1, (255, 255, 255))
        else:
            temp = FNFfont.render(tempText[k], 1, (200, 200, 200))
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
        if k == selectedKeybind:
            temp = Font125.render(tempText[k], 1, (255, 255, 255))
        else:
            temp = Font100.render(tempText[k], 1, (200, 200, 200))
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


menuMusic.play(-1)

while True:
    for events in event.get():
        if events.type == QUIT or (events.type == KEYDOWN and events.key == K_ESCAPE):
            if currentMenu == "Main":
                options.saveOptions()
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
                    options.saveOptions()
                    options.update()
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
                    restart = Main_game(musicList[selectedMusic], options)
                menuMusic.play(-1)
            if currentMenu == "Main":
                if selectedMain == 0:
                    currentMenu = "Select music"
                if selectedMain == 1:
                    currentMenu = "Options"
                    preventDoubleEnter = True
        if events.type == KEYDOWN:
            if currentMenu == "Select music":
                if (events.key == K_w or ((events.key == K_UP and K_UP != 1073741906 and K_DOWN != 1073741906) or (
                        events.key == 1073741906))) and selectedMusic > 0:
                    selectedMusic -= 1
                if (events.key == K_s or ((events.key == K_DOWN and K_DOWN != 1073741905 and K_UP != 1073741905) or (
                        events.key == 1073741905))) and selectedMusic < len(musicList) - 1:
                    selectedMusic += 1
            if currentMenu == "Options":
                if (events.key == K_w or ((events.key == K_UP and K_UP != 1073741906 and K_DOWN != 1073741906) or (
                        events.key == 1073741906))) and selectedOption > 0:
                    selectedOption -= 1
                if (events.key == K_s or ((events.key == K_DOWN and K_DOWN != 1073741905 and K_UP != 1073741905) or (
                        events.key == 1073741905))) and selectedOption < 9:
                    selectedOption += 1
                if selectedOption == 0:
                    if (events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904))) and options.selectedSpeed > 0.1:
                        options.selectedSpeed -= 0.1
                        options.selectedSpeed = round(options.selectedSpeed, 1)
                    if events.key == K_d or (
                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                            events.key == 1073741903)):
                        options.selectedSpeed += 0.1
                        options.selectedSpeed = round(options.selectedSpeed, 1)
                if selectedOption == 1:
                    if events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904)) or events.key == K_d or events.key == K_RIGHT:
                        if options.playAs == "Player":
                            options.playAs = "Opponent"
                        else:
                            options.playAs = "Player"
                if selectedOption == 2:
                    if events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904)) or events.key == K_d or events.key == K_RIGHT:
                        if options.noDying:
                            options.noDying = False
                        else:
                            options.noDying = True
                if selectedOption == 3:
                    if (events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904))) and options.selectedNoteStyle > 0:
                        options.selectedNoteStyle -= 1
                    if (events.key == K_d or (
                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                            events.key == 1073741903))) and options.selectedNoteStyle < len(
                            availableNoteStyles) - 1:
                        options.selectedNoteStyle += 1
                if selectedOption == 4:
                    if (events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904))) or (events.key == K_d or (
                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                            events.key == 1073741903))):
                        options.downscroll = not options.downscroll
                if selectedOption == 5:
                    if (events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904))) or (events.key == K_d or (
                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                            events.key == 1073741903))):
                        options.debugMode = not options.debugMode
                if selectedOption == 6:
                    if (events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904))) or (events.key == K_d or (
                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                            events.key == 1073741903))):
                        if options.healthFormat == "Healthbar":
                            options.healthFormat = "Infobar"
                        else:
                            options.healthFormat = "Healthbar"
                if selectedOption == 7:
                    if (events.key == K_a or (
                            (events.key == K_LEFT and K_LEFT != 1073741904 and K_RIGHT != 1073741904) or (
                            events.key == 1073741904))) or (events.key == K_d or (
                            (events.key == K_RIGHT and K_RIGHT != 1073741903 and K_LEFT != 1073741903) or (
                            events.key == 1073741903))):
                        options.coloredInfo = not options.coloredInfo
                if selectedOption == 8:
                    if events.key == K_RETURN and not preventDoubleEnter:
                        currentMenu = "Keybinds"
                        preventDoubleEnter = True
                if selectedOption == 9:
                    if events.key == K_RETURN and not preventDoubleEnter:
                        options.saveOptions()
                        mouse.set_visible(True)
                        offset_editor()
                        options.update()
                        mouse.set_visible(False)
            if currentMenu == "Main":
                if (events.key == K_w or ((events.key == K_UP and K_UP != 1073741906 and K_DOWN != 1073741906) or (
                        events.key == 1073741906))) and selectedMain > 0:
                    selectedMain -= 1
                if (events.key == K_s or ((events.key == K_DOWN and K_DOWN != 1073741905 and K_UP != 1073741905) or (
                        events.key == 1073741905))) and selectedMain < 1:
                    selectedMain += 1
            if currentMenu == "Keybinds":
                if (events.key == K_w or ((events.key == K_UP and K_UP != 1073741906 and K_DOWN != 1073741906) or (
                        events.key == 1073741906))) and selectedKeybind > 0:
                    selectedKeybind -= 1
                if (events.key == K_s or ((events.key == K_DOWN and K_DOWN != 1073741905 and K_UP != 1073741905) or (
                        events.key == 1073741905))) and selectedKeybind < 8:
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
