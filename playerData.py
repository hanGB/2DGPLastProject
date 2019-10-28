from pico2d import *


class Player:
    bar = None
    BdBar = None
    MdBar = None
    pattern = None

    def __init__(self, p, Bd, Md, status):

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
        self.status = status  # MatAtt, MindAtt, MatDef, MindDef, HitRate, AvoidRate
        self.buff = [0, 0]
        self.Bd = self.max_Bd
        self.Md = self.max_Md

    def getBd(self):
        return self.Bd

    def setBd(self, Bd):
        self.Bd = Bd

    def getMd(self):
        return self.Md

    def setMd(self, Md):
        self.Md = Md

    def draw(self, slt):
        BdRate = self.Bd / self.max_Bd
        MdRate = self.Md / self.max_Md

        Player.bar.draw(1060, 200 - slt * 50)
        Player.BdBar.draw(972 - (1 - BdRate) * 72, 200 - slt * 50, 150 * BdRate, 20)
        Player.MdBar.draw(1143 - (1 - MdRate) * 72, 200 - slt * 50, 150 * MdRate, 20)
        Player.pattern.clip_draw(self.pat * 30, 0, 30, 30, 880, 200 - slt * 50)
