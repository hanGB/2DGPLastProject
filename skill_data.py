from pico2d import *


class Skill:
    space_bar = None

    def __init__(self, number):
        if Skill.space_bar is None:
            Skill.space_bar = load_image("resource/interface/space.png")
        self.number = number

        if (self.number / 10) < 1:
            self.image = load_image("resource/skill/ig.png")
            if (self.number % 10) == 3:
                self.pattern = 3
                self.turn = 1
                self.damage = 50
                self.rate = 95
                self.Md = 4

            elif (self.number % 10) == 2:
                self.pattern = 3
                self.turn = 2
                self.damage = 200
                self.rate = 95
                self.Md = 8

            elif (self.number % 10) == 1:
                self.pattern = 3
                self.turn = 3
                self.damage = 350
                self.rate = 95
                self.Md = 16

            elif (self.number % 10) == 0:
                self.pattern = 3
                self.turn = 4
                self.damage = 499
                self.rate = 95
                self.Md = 32

        elif (self.number / 10) < 2:
            self.image = load_image("resource/skill/aq.png")

        elif (self.number / 10) < 3:
            self.image = load_image("resource/skill/ter.png")

        elif (self.number / 10) < 4:
            self.image = load_image("resource/skill/vent.png")

        elif (self.number / 10) < 5:
            self.image = load_image("resource/skill/per.png")

        elif (self.number / 10) < 6:
            self.image = load_image("resource/skill/fat.png")

        elif (self.number / 10) < 7:
            self.image = load_image("resource/skill/met.png")

        elif (self.number / 10) < 8:
            self.image = load_image("resource/skill/cura.png")

        elif (self.number / 10) < 9:
            self.image = load_image("resource/skill/sana.png")

        elif (self.number / 10) < 10:
            self.image = load_image("resource/interface/sdInBattle.png")
            if (self.number % 10) == 1:
                self.pattern = 1
                self.turn = 1
                self.damage = 25
                self.rate = 95
                self.Md = 0

            elif (self.number % 10) == 0:
                self.pattern = 7
                self.turn = 1
                self.damage = 25
                self.rate = 95
                self.Md = 1

    def get_number(self):
        return self.number

    def get_pattern(self):
        return self.pattern

    def get_turn(self):
        return self.turn

    def get_damage(self):
        return self.damage

    def get_rate(self):
        return self.rate

    def get_Md(self):
        return self.Md

    def draw(self, locate, selected):
        self.image.clip_draw(0, self.number % 10 * 50, 200, 50, 360 + selected * 70, 270 - locate * 50)
        if selected == 1:
            Skill.space_bar.draw(280, 270 - locate * 50)


