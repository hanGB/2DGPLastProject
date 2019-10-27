from pico2d import *


class Player:

    def __init__(self):
        self.max_Bd = 300
        self.max_Md = 200
        self.max_Turn = 3
        self.status = [10, 10, 10, 10, 10, 10]  # MatAtt, MindAtt, MatDef, MindDef, HitRate, AvoidRate
        self.buff = [0, 0]
        self.now_Bd = self.max_Bd
        self.now_Md = self.max_Md


class Card:
    def __init__(self, attribute, skill):
        self.attribute = attribute  # BS, RS, BD, RD, BH, RH, BC, RC
        self.skill = skill


class Enemy:
    target = None

    def __init__(self, type):
        if Enemy.target is None:
            Enemy.target = load_image("2target.png")

        self.type = type

        if type == 0:
            self.image = load_image("4-0alice.png")
            self.max_Bd = 2000
            self.status = [35, 35, 35, 35, 35]
            self.max_turn = 5

        elif type == 1:
            self.image = load_image("4-1slame.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 1

        elif type == 2:
            self.image = load_image("4-2jack_o_lantern.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 1

        elif type == 3:
            self.image = load_image("4-3jack_frost.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 2

        elif type == 4:
            self.image = load_image("4-4loa.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 2

        elif type == 5:
            self.image = load_image("4-5high_pixie.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 2

        elif type == 6:
            self.image = load_image("4-6kaiwan.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 3

        elif type == 7:
            self.image = load_image("4-7legion.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 3

        elif type == 8:
            self.image = load_image("4-8naga.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 3

        elif type == 9:
            self.image = load_image("4-9dol.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 3

        elif type == 10:
            self.image = load_image("4-10surt.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 4

        elif type == 11:
            self.image = load_image("4-11norn.png")
            self.max_Bd = 100
            self.status = [10, 10, 10, 10, 10]
            self.max_turn = 4

        elif type == 12:
            self.image = load_image("4-12rucipel.png")
            self.max_Bd = 5000
            self.status = [50, 50, 50, 50, 50]
            self.max_turn = 5

        elif type == 13:
            self.image = load_image("4-13ruciper.png")
            self.max_Bd = 9999
            self.status = [99, 99, 19, 19, 19]
            self.max_turn = 9

        self.Bd = self.max_Bd
        self.buf = [0, 0]
        self.turn = self.max_turn
        self.down = 0

    def getBd(self):
        return self.Bd

    def setBd(self, Bd):
        self.Bd = Bd

    def getMd(self):
        return self.Md

    def setMd(self, Md):
        self.Md = Md

    def draw(self, position, slt):
        self.image.draw(200 + position * 200, 300)
        if slt == 0:
            if self.type == 1:
                Enemy.target.draw(200 + position * 200 + 100, 250)
            else:
                Enemy.target.draw(200 + position * 200 + 100, 300)


class Skill:
    space_bar = None

    def __init__(self, number, attribute, turn, type, damage, rate):
        # type에 따라 damage가 어디에 적용되는 지 달라진다.
        if Skill.space_bar is None:
            Skill.space_bar = load_image("2space.png")
        self.number = number

        if (self.number / 10) < 1:
            self.image = load_image("3ig.png")
        elif (self.number / 10) < 2:
            self.image = load_image("3aq.png")
        elif (self.number / 10) < 3:
            self.image = load_image("3ter.png")
        elif (self.number / 10) < 4:
            self.image = load_image("3vent.png")
        elif (self.number / 10) < 5:
            self.image = load_image("3per.png")
        elif (self.number / 10) < 6:
            self.image = load_image("3fat.png")
        elif (self.number / 10) < 7:
            self.image = load_image("3met.png")
        elif (self.number / 10) < 8:
            self.image = load_image("3cura.png")
        elif (self.number / 10) < 9:
            self.image = load_image("3sana.png")

        self.attribute = attribute
        self.turn = turn
        self.type = type
        self.damage = damage
        self.rate = rate

    def draw(self, locate, slt):
        self.image.clip_draw(0, (self.number % 10) * 50, 200, 50, 360 + slt * 70, 270 - locate * 50)
        if slt == 1:
            Skill.space_bar.draw(280, 270 - locate * 50)


