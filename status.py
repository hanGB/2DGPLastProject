from pico2d import *


class Player:

    def __init__(self):
        self.max_Bd = 300
        self.max_Turn = 3
        self.status = [10, 10, 10, 10, 10, 10]  # MatAtt, MindAtt, MatDef, MindDef, HitRate, AvoidRate
        self.buff = [0, 0]


class Card:

    def __init__(self):
        self.attribute = [0, 0, 0, 0, 0]  # Fer, IgAq, VentTer, Per, Lar
        self.skill = [0, 10, 11]


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


