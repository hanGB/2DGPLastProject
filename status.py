from pico2d import *


class Card:
    def __init__(self, type):
        self.attribute = [0, 0, 0, 0, 0, 0, 0, 0]
        if type == 0:
            self.attribute = [0, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 1:
            self.attribute = [1, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

        elif type == 2:
            self.attribute = [2, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 3:
            self.attribute = [3, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 4:
            self.attribute = [4, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 5:
            self.attribute = [5, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 6:
            self.attribute = [6, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 7:
            self.attribute = [1, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 8:
            self.attribute = [2, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 9:
            self.attribute = [0, 0, 3, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 10:
            self.attribute = [0, 0, 0, 4, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 11:
            self.attribute = [0, 0, 4, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 12:
            self.attribute = [0, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 13:
            self.attribute = [3, 3, 3, 3, 3, 3, 3, 3]
            self.skill = [11, 12, 12, 31, 21]

    def getAttribute(self):
        return self.attribute

    def getSkill(self):
        return self.skill


class Skill:
    space_bar = None

    def __init__(self, number):
        # type에 따라 damage가 어디에 적용되는 지 달라진다.
        if Skill.space_bar is None:
            Skill.space_bar = load_image("2space.png")
        self.number = number

        if (self.number / 10) < 1:
            self.image = load_image("3ig.png")
            if (self.number % 10) == 3:
                self.attribute = 4
                self.turn = 1
                self.damage = 50
                self.rate = 95
            elif (self.number % 10) == 2:
                self.attribute = 4
                self.turn = 2
                self.damage = 200
                self.rate = 95
            elif (self.number % 10) == 1:
                self.attribute = 4
                self.turn = 3
                self.damage = 350
                self.rate = 95
            elif (self.number % 10) == 0:
                self.attribute = 4
                self.turn = 4
                self.damage = 499
                self.rate = 95

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

        self.type = type

    def draw(self, locate, slt):
        self.image.clip_draw(0, self.number % 10 * 50, 200, 50, 360 + slt * 70, 270 - locate * 50)
        if slt == 1:
            Skill.space_bar.draw(280, 270 - locate * 50)


