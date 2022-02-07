from pygame import *
import json
from random import *
import time as Time
import cProfile
import sys

Inst = None
Vocals = None
chart = None
misses = 0

def Main_game(musicName, speed):
    global Inst
    global Vocals
    global chart
    global misses
    misses = 0

    init()

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
            temp = (display.Info().current_w - 200) / 3
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

    fpsQuality = 100
    fpsList = []
    fpsTime = Time.time()

    accuracy = 0
    accuracyDisplayTime = 0
    showAccuracy = False
    accuracyIndicator = ""
    accuracyIndicatorTime = Time.time()

    Font40 = font.SysFont("Comic Sans MS", 40)

    arrowSkinID = "Basic"

    longNotesChart = []
    # endregion

    # region images loading
    # region load images
    arrowsSkins = [
        transform.scale(image.load("assets\Images\Arrows\{0}\Purple left arrow.png".format(arrowSkinID)).convert_alpha(),
                        (150, 150)),
        transform.scale(image.load("assets\Images\Arrows\{0}\Blue down arrow.png".format(arrowSkinID)).convert_alpha(),
                        (150, 150)),
        transform.scale(image.load("assets\Images\Arrows\{0}\Green up arrow.png".format(arrowSkinID)).convert_alpha(),
                        (150, 150)),
        transform.scale(image.load("assets\Images\Arrows\{0}\Red right arrow.png".format(arrowSkinID)).convert_alpha(),
                        (150, 150))]

    pressedArrowsSkins = [
        transform.scale(image.load("assets\Images\Arrows\{0}\left pressed arrow.png".format(arrowSkinID)).convert_alpha(),
                        (150, 150)),
        transform.scale(image.load("assets\Images\Arrows\{0}\down pressed arrow.png".format(arrowSkinID)).convert_alpha(),
                        (150, 150)),
        transform.scale(
            image.load("assets\Images\Arrows\{0}/up pressed arrow.png".format(arrowSkinID)).convert_alpha(),
            (150, 150)),
        transform.scale(
            image.load("assets\Images\Arrows\{0}/right pressed arrow.png".format(arrowSkinID)).convert_alpha(),
            (150, 150))]

    accuracyIndicatorImages = [
        transform.scale(image.load("assets\Images\Accuracy indicator\sick.png").convert_alpha(), (225, 100)),
        transform.scale(image.load("assets\Images\Accuracy indicator\good.png").convert_alpha(), (225, 100)),
        transform.scale(image.load("assets\Images\Accuracy indicator/bad.png").convert_alpha(), (225, 100)),
        transform.scale(image.load("assets\Images\Accuracy indicator\shit.png").convert_alpha(), (225, 100))]

    greyArrow = transform.scale(
        image.load("assets\Images\Arrows\{0}\Strum line arrow modified.png".format(arrowSkinID)).convert_alpha(),
        (150, 150))
    greyArrow = [transform.rotate(greyArrow, 90), transform.rotate(greyArrow, 180), greyArrow,
                 transform.rotate(greyArrow, -90)]

    longNotesImg = [
        transform.scale(image.load("assets\Images\Long notes\{0}\Middle\left.png".format(arrowSkinID)).convert_alpha(),
                        (52, 46)),
        transform.scale(image.load("assets\Images\Long notes\{0}\Middle\down.png".format(arrowSkinID)).convert_alpha(),
                        (52, 46)),
        transform.scale(image.load("assets\Images\Long notes\{0}\Middle/up.png".format(arrowSkinID)).convert_alpha(),
                        (52, 46)),
        transform.scale(image.load("assets\Images\Long notes\{0}\Middle/right.png".format(arrowSkinID)).convert_alpha(),
                        (52, 46))]

    longNotesEnd = [
        transform.scale(image.load("assets\Images\Long notes\{0}\End\left.png".format(arrowSkinID)).convert_alpha(),
                        (52, 46)),
        transform.scale(image.load("assets\Images\Long notes\{0}\End\down.png".format(arrowSkinID)).convert_alpha(),
                        (52, 46)),
        transform.scale(image.load("assets\Images\Long notes\{0}\End/up.png".format(arrowSkinID)).convert_alpha(),
                        (52, 46)),
        transform.scale(image.load("assets\Images\Long notes\{0}\End/right.png".format(arrowSkinID)).convert_alpha(),
                        (52, 46))]

    # endregion

    # region create image rect
    accuracyIndicatorRect = accuracyIndicatorImages[0].get_rect()
    accuracyIndicatorRect.center = (middleScreen[0], middleScreen[1] - 75)

    arrowRect = arrowsSkins[0].get_rect()
    # endregion

    musicList = json.load(open("assets/MusicList.json"))["musics"]

    loadingscreen(1)


    # endregion

    # region music and chart loading
    def open_file(music):
        global Inst
        global Vocals
        global chart
        Inst = mixer.Sound("assets\Musics\{0}\Inst.ogg".format(music))
        Vocals = mixer.Sound("assets\Musics\{0}\Voices.ogg".format(music))
        chart = json.load(open("assets\Musics\{0}\chart.json".format(music)))["song"]["notes"]


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
    class Note:
        def __init__(self, pos, column, side, length):
            self.pos = pos
            self.column = column
            self.side = side
            self.length = length


    class LongNote:
        def __init__(self, pos, column, side, isEnd):
            self.pos = pos
            self.column = column
            self.side = side
            self.isEnd = isEnd


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
    #       If not mustHit:
    #           0 = opponent down
    #           1 = opponent left
    #           2 = opponent up
    #           3 = opponent right
    #           4 = player left
    #           5 = player down
    #           6 = player up
    #           7 = player right

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
                        tempUser = "Player"
                    elif 7 >= note[1] >= 4:
                        tempUser = "Opponent"
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
                            tempUser = "Player"
                        if 7 >= note[1] >= 4:
                            tempUser = "Opponent"
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
                            tempUser = "Opponent"
                        if 7 >= note[1] >= 4:
                            tempUser = "Player"
                        if note[1] == 1 or note[1] == 5:
                            tempDirection = "Down"
                        if note[1] == 0 or note[1] == 4:
                            tempDirection = "Left"
                        if note[1] == 2 or note[1] == 6:
                            tempDirection = "Up"
                        if note[1] == 3 or note[1] == 7:
                            tempDirection = "Right"
                notesChart.append(Note(note[0], tempDirection, tempUser, note[2]))
    # endregion


    # region sort notes and create long notes
    temp = notesChart
    notesChart = []

    for k in range(len(temp)):
        min = temp[0].pos
        minX = 0
        for x in range(len(temp)):
            if temp[x].pos < min:
                min = temp[x].pos
                minX = x
        notesChart.append(temp[minX])
        temp.remove(temp[minX])

    longNotesLen = 42 // speed
    for note in notesChart:
        if note.length >= longNotesLen:
            for k in range(1, int(round(note.length // longNotesLen))):
                longNotesChart.append(LongNote(note.pos + k * longNotesLen, note.column, note.side, False))
            longNotesChart.append(LongNote(note.pos + (note.length // longNotesLen) * longNotesLen, note.column, note.side, True))

    print(len(longNotesChart))

    loadingscreen(2)



    def quicksort(T):
        if T==[]:
            return []
        else:
            pivot=T[0]
            T1=[]
            T2=[]
        for k in T[1:]:
            if k.pos < pivot.pos:
                T1.append(k)
            else:
                T2.append(k)
        return quicksort(T1)+[pivot]+quicksort(T2)

    longNotesChart = quicksort(longNotesChart)

    loadingscreen(3)


    # endregion
    # endregion
    # endregion

    # region screen and notes update
    def drawGreyNotes():
        width = display.Info().current_w
        temp = arrowRect
        temp.topright = (width - 540, 50)
        if K_a in keyPressed or K_LEFT in keyPressed:
            screen.blit(pressedArrowsSkins[0], temp)
        else:
            screen.blit(greyArrow[0], temp)
        temp = arrowRect
        temp.topright = (width - 380, 50)
        if K_s in keyPressed or K_DOWN in keyPressed:
            screen.blit(pressedArrowsSkins[1], temp)
        else:
            screen.blit(greyArrow[1], temp)
        temp = arrowRect
        temp.topright = (width - 220, 50)
        if K_w in keyPressed or K_UP in keyPressed:
            screen.blit(pressedArrowsSkins[2], temp)
        else:
            screen.blit(greyArrow[2], temp)
        temp = arrowRect
        temp.topright = (width - 60, 50)
        if K_d in keyPressed or K_RIGHT in keyPressed:
            screen.blit(pressedArrowsSkins[3], temp)
        else:
            screen.blit(greyArrow[3], temp)
        if not singlePlayer:
            temp = arrowRect
            temp.topleft = (60, 50)
            screen.blit(greyArrow[0], temp)
            temp = arrowRect
            temp.topleft = (220, 50)
            screen.blit(greyArrow[1], temp)
            temp = arrowRect
            temp.topleft = (380, 50)
            screen.blit(greyArrow[2], temp)
            temp = arrowRect
            temp.topleft = (540, 50)
            screen.blit(greyArrow[3], temp)


    def drawNotes():
        global misses
        currentTime = Time.time() - startTime
        width = display.Info().current_w
        renderNotes = True
        for note in notesChart:
            if renderNotes:
                if note.side == "Opponent" and currentTime * 1000 >= note.pos:
                    notesChart.remove(note)
                if currentTime * 1000 - 133 >= note.pos and note.side == "Player" and note.column in ["Left", "Down", "Up",
                                                                                                      "Right"]:
                    notesChart.remove(note)
                    misses += 1
                if 50 + (note.pos - currentTime * 1000) * speed < display.Info().current_h + 100:
                    if not singlePlayer:
                        if note.side == "Opponent" and note.column == "Down":
                            temp = arrowRect
                            temp.topleft = (220, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[1], temp)
                        elif note.side == "Opponent" and note.column == "Left":
                            temp = arrowRect
                            temp.topleft = (60, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[0], temp)
                        elif note.side == "Opponent" and note.column == "Up":
                            temp = arrowRect
                            temp.topleft = (380, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[2], temp)
                        elif note.side == "Opponent" and note.column == "Right":
                            temp = arrowRect
                            temp.topleft = (540, 50 + (note.pos - currentTime * 1000) * speed)
                            screen.blit(arrowsSkins[3], temp)
                    if note.side == "Player" and note.column == "Down":
                        temp = arrowRect
                        temp.topright = (width - 380, 50 + (note.pos - currentTime * 1000) * speed)
                        screen.blit(arrowsSkins[1], temp)
                    elif note.side == "Player" and note.column == "Left":
                        temp = arrowRect
                        temp.topright = (width - 540, 50 + (note.pos - currentTime * 1000) * speed)
                        screen.blit(arrowsSkins[0], temp)
                    elif note.side == "Player" and note.column == "Up":
                        temp = arrowRect
                        temp.topright = (width - 220, 50 + (note.pos - currentTime * 1000) * speed)
                        screen.blit(arrowsSkins[2], temp)
                    elif note.side == "Player" and note.column == "Right":
                        temp = arrowRect
                        temp.topright = (width - 60, 50 + (note.pos - currentTime * 1000) * speed)
                        screen.blit(arrowsSkins[3], temp)

                else:
                    renderNotes = False


    def drawLongNotes():
        currentTime = Time.time() - startTime
        width = display.Info().current_w
        run = True
        for longNote in longNotesChart:
            if run:
                if longNote.side == "Opponent" and currentTime * 1000 >= longNote.pos:
                    longNotesChart.remove(longNote)
                if longNote.side == "Player" and currentTime * 1000 >= longNote.pos and longNote.column in ["Left", "Down",
                                                                                                            "Up", "Right"]:
                    if ((K_LEFT in keyPressed or K_a in keyPressed) and longNote.column == "Left") or (
                            (K_DOWN in keyPressed or K_s in keyPressed) and longNote.column == "Down") or (
                            (K_UP in keyPressed or K_w in keyPressed) and longNote.column == "Up") or (
                            (K_RIGHT in keyPressed or K_d in keyPressed) and longNote.column == "Right"):
                        longNotesChart.remove(longNote)
                if 50 + (longNote.pos - currentTime * 1000) * speed < display.Info().current_h + 100:
                    if not singlePlayer and longNote.side == "Opponent":
                        if longNote.column == "Down":
                            temp = arrowRect
                            temp.center = (220 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                            if longNote.isEnd:
                                screen.blit(longNotesEnd[1], temp)
                            else:
                                screen.blit(longNotesImg[1], temp)
                        if longNote.column == "Left":
                            temp = arrowRect
                            temp.center = (60 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                            if longNote.isEnd:
                                screen.blit(longNotesEnd[0], temp)
                            else:
                                screen.blit(longNotesImg[0], temp)
                        if longNote.column == "Up":
                            temp = arrowRect
                            temp.center = (380 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                            if longNote.isEnd:
                                screen.blit(longNotesEnd[2], temp)
                            else:
                                screen.blit(longNotesImg[2], temp)
                        if longNote.column == "Right":
                            temp = arrowRect
                            temp.center = (540 + 125, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                            if longNote.isEnd:
                                screen.blit(longNotesEnd[3], temp)
                            else:
                                screen.blit(longNotesImg[3], temp)
                    if longNote.side == "Player":
                        if longNote.column == "Up":
                            temp = arrowRect
                            temp.center = (width - 220 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                            if longNote.isEnd:
                                screen.blit(longNotesEnd[2], temp)
                            else:
                                screen.blit(longNotesImg[2], temp)
                        if longNote.column == "Down":
                            temp = arrowRect
                            temp.center = (width - 380 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                            if longNote.isEnd:
                                screen.blit(longNotesEnd[1], temp)
                            else:
                                screen.blit(longNotesImg[1], temp)
                        if longNote.column == "Left":
                            temp = arrowRect
                            temp.center = (width - 540 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                            if longNote.isEnd:
                                screen.blit(longNotesEnd[0], temp)
                            else:
                                screen.blit(longNotesImg[0], temp)
                        if longNote.column == "Right":
                            temp = arrowRect
                            temp.center = (width - 60 - 25, 50 + (longNote.pos - currentTime * 1000) * speed + 100)
                            if longNote.isEnd:
                                screen.blit(longNotesEnd[3], temp)
                            else:
                                screen.blit(longNotesImg[3], temp)
                else:
                    run = False


    # endregion


    keyPressed = []

    Inst.play()
    Vocals.play()

    startTime = Time.time()

    while True:
        notesToClear = [[], [], [], []]
        for events in event.get():
            if events.type == QUIT or (events.type == KEYDOWN and events.key == K_ESCAPE):
                Inst.stop()
                Vocals.stop()
                return None
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
                            if note.side == "Player" and currentTime * 1000 - 133 <= note.pos <= currentTime * 1000 + 133:
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
                elif currentTime * 1000 + 79 >= notesToClear[k][minX].pos >= currentTime * 1000 - 79:
                    accuracyIndicator = accuracyIndicatorImages[1]
                elif currentTime * 1000 + 109 >= notesToClear[k][minX].pos >= currentTime * 1000 - 109:
                    accuracyIndicator = accuracyIndicatorImages[2]
                else:
                    accuracyIndicator = accuracyIndicatorImages[3]
                notesChart.remove(notesToClear[k][minX])
        screen.fill((0, 0, 0))
        drawGreyNotes()
        drawLongNotes()
        drawNotes()
        # region draw bottom info bar
        temp = Font40.render("Misses: {0}".format(misses), 1, (255, 255, 255))
        temp1 = temp.get_rect()
        temp1.midbottom = (middleScreen[0], display.Info().current_h - 5)
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
        display.flip()
        if Time.time() - startTime > musicLen:
            Inst.stop()
            Vocals.stop()
            return None