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

selectedMusic = 0
selectedOption = 0
selectedMain = 0
currentMenu = "Main"

selectedSpeed = 1.6
playAs = "Player"
noDying = False
selectedNoteStyle = 0


def drawMusics():
    for k in range(len(musicList)):
        temp = FNFfont.render(musicList[k], 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1] + 200 * (k - selectedMusic))
        screen.blit(temp, temp1)


def drawOptions():
    tempText = ["Speed: {0}".format(selectedSpeed), "Play as: {0}".format(playAs), "No dying: {0}".format(noDying), "Note style: {0}".format(availableNoteStyles[selectedNoteStyle])]
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


while True:
    for events in event.get():
        if events.type == QUIT or (events.type == KEYDOWN and events.key == K_ESCAPE):
            if currentMenu == "Main":
                quit()
                exit()
            else:
                currentMenu = "Main"
        if events.type == KEYDOWN and events.key == K_RETURN:
            if currentMenu == "Select music":
                Inst = None
                Vocals = None
                chart = None
                misses = 0
                health = 50
                BG = None
                cProfile.run("Main_game(musicList[selectedMusic], selectedSpeed, playAs, noDying, availableNoteStyles[selectedNoteStyle])")
            if currentMenu == "Main":
                if selectedMain == 0:
                    currentMenu = "Select music"
                if selectedMain == 1:
                    currentMenu = "Options"
        if events.type == KEYDOWN:
            if currentMenu == "Select music":
                if (events.key == K_w or events.key == K_UP) and selectedMusic > 0:
                    selectedMusic -= 1
                if (events.key == K_s or events.key == K_DOWN) and selectedMusic < len(musicList) - 1:
                    selectedMusic += 1
            if currentMenu == "Options":
                if (events.key == K_w or events.key == K_UP) and selectedOption > 0:
                    selectedOption -= 1
                if (events.key == K_s or events.key == K_DOWN) and selectedOption < 3:
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
                    if (events.key == K_d or events.key == K_RIGHT) and selectedNoteStyle < len(availableNoteStyles) - 1:
                        selectedNoteStyle += 1
            if currentMenu == "Main":
                if (events.key == K_w or events.key == K_UP) and selectedMain > 0:
                    selectedMain -= 1
                if (events.key == K_s or events.key == K_DOWN) and selectedMain < 1:
                    selectedMain += 1
    screen.fill((0, 0, 0))
    screen.blit(menuBG, BGrect)
    if currentMenu == "Select music":
        drawMusics()
    elif currentMenu == "Options":
        drawOptions()
    elif currentMenu == "Main":
        drawMain()
    display.flip()
