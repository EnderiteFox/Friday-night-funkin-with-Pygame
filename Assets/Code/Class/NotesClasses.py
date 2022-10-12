class Note:
    def __init__(self, pos, column, side, length, noteId, textureName, behaviour=None):
        self.pos = pos
        self.column = column
        self.side = side
        self.length = length
        self.id = noteId
        self.texture = textureName
        self.behaviour = behaviour
        self.columnid = -1
        self.columnid2 = -1
        self.columnid3 = -1
        self.bigHealthBoost = 2.3
        self.smallHealthBoost = 0.4
        self.healthPenalty = -4
        self.mustAvoid = False
        self.hitModchart = []
        self.missModchart = []


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
