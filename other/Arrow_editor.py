import tkinter
from tkinter.filedialog import askdirectory
from pygame import *
import xml.etree.ElementTree as ET
import json
import os
import time as Time
import copy


def arrow_editor():
    root = tkinter.Tk()
    root.withdraw()
    root.attributes("-topmost", True)

    init()

    screen = display.set_mode((0, 0), FULLSCREEN)

    if not display.Info().current_w / display.Info().current_h == 1920 / 1080:
        BG = transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "menuBG.png"), (1920, 1080))
    else:
        BG = transform.scale(image.load("assets" + os.path.sep + "Images" + os.path.sep + "menuBG.png"),
                             (display.Info().current_w, display.Info().current_h))

    BGtype = 0

    Font30 = font.SysFont("Comic Sans MS", 30)

    temp = Font30.render("Click to open folder", 1, (0, 0, 0))
    temp1 = temp.get_rect()
    clickHitboxWidth = temp1.width + 5
    clickHitboxHeight = temp1.height

    folderPath = None
    arrowSkin = None
