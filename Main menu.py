from pygame import *
import json
from random import *
import time as Time
import cProfile
import sys
from Game import Main_game

init()

screen = display.set_mode((0,0), FULLSCREEN)
middleScreen = (display.Info().current_w // 2, display.Info().current_h // 2)

musicList = json.load(open("assets\MusicList.json"))["musics"]

Font100 = font.SysFont("Comic Sans MS", 100)

selectedMusic = 0

def drawMusics():
    for k in range(len(musicList)):
        temp = Font100.render(musicList[k], 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.center = (middleScreen[0], middleScreen[1] + 200 * (k - selectedMusic))
        screen.blit(temp, temp1)

while True:
    for events in event.get():
        if events.type == QUIT or (events.type == KEYDOWN and events.key == K_ESCAPE):
            quit()
            exit()
        if events.type == KEYDOWN and events.key == K_RETURN:
            Inst = None
            Vocals = None
            chart = None
            misses = 0
            Main_game(musicList[selectedMusic], 1.8)
        if events.type == KEYDOWN:
            if events.key == K_w or events.key == K_UP and selectedMusic > 0:
                selectedMusic -= 1
            if events.key == K_s or events.key == K_DOWN and selectedMusic < len(musicList) - 1:
                selectedMusic += 1
    screen.fill((0,0,0))
    drawMusics()
    display.flip()