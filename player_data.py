from pico2d import *
import status

class Player:
    bar = None
    BdBar = None
    MdBar = None
    pattern = None
    item_number = None
    item_sign = None

    def __init__(self, p, Bd, Md, stat):

        if Player.bar is None:
            Player.bar = load_image("2BdMdBar.png")

        if Player.BdBar is None:
            Player.BdBar = load_image("2BdBar.png")

        if Player.MdBar is None:
            Player.MdBar = load_image("2MdBar.png")

        if Player.pattern is None:
            Player.pattern = load_image("2pattern.png")

        self.pat = p
        self.max_Bd = Bd
        self.max_Md = Md
        self.max_Turn = 3
        self.stat = stat  # MatAtt, MindAtt, MatDef, MindDef, HitRate, AvoidRate
        self.buff = [0, 0]
        self.Bd = self.max_Bd
        self.Md = self.max_Md
        self.card = status.Card(1)

        if self.pat == 0:
            if Player.item_number is None:
                Player.item_number = load_image("2itemNum.png")
            if Player.item_sign is None:
                Player.item_sign = load_image("2itemSign.png")
            self.item = [3, 0, 0, 2, 0, 0, 0]

    def getBd(self):
        return self.Bd

    def setBd(self, Bd):
        self.Bd = Bd

    def getMd(self):
        return self.Md

    def setMd(self, Md):
        self.Md = Md

    def getTurn(self):
        return self.max_Turn

    def draw(self, slt):
        BdRate = self.Bd / self.max_Bd
        MdRate = self.Md / self.max_Md

        Player.bar.draw(1060, 200 - slt * 50)
        Player.BdBar.draw(972 - (1 - BdRate) * 72, 200 - slt * 50, 150 * BdRate, 20)
        Player.MdBar.draw(1143 - (1 - MdRate) * 72, 200 - slt * 50, 150 * MdRate, 20)
        Player.pattern.clip_draw(self.pat * 30, 0, 30, 30, 880, 200 - slt * 50)

    def draw_item_number(self, number):
        if self.pat == 0:
            for i in range(7):
                Player.item_number.clip_draw(20 * self.item[i], 0, 20, 30, 375, 275 - 30 * i)
                if i == number:
                    Player.item_sign.draw(315, 278 - 30 * i)
