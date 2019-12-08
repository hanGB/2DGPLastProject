from pico2d import *


class Skill:
    space_bar = None

    def __init__(self, number):
        if Skill.space_bar is None:
            Skill.space_bar = load_image("resource/interface/space.png")
        self.number = number

        if (self.number / 10) < 1:
            self.image = load_image("resource/skill/ig.png")
            self.animation = load_image("resource/animation/igAni.png")
            if (self.number % 10) == 3:
                self.pattern = 3
                self.turn = 1
                self.damage = 45
                self.rate = 95
                self.Md = 4
                self.ally_target = False
                self.all_targets = False

            elif (self.number % 10) == 2:
                self.pattern = 3
                self.turn = 2
                self.damage = 125
                self.rate = 95
                self.Md = 8
                self.ally_target = False
                self.all_targets = False

            elif (self.number % 10) == 1:
                self.pattern = 3
                self.turn = 3
                self.damage = 325
                self.rate = 95
                self.Md = 16
                self.ally_target = False
                self.all_targets = False

            elif (self.number % 10) == 0:
                self.pattern = 3
                self.turn = 4
                self.damage = 499
                self.rate = 95
                self.Md = 32
                self.ally_target = False
                self.all_targets = False

        elif (self.number / 10) < 2:
            self.image = load_image("resource/skill/aq.png")
            self.animation = load_image("resource/animation/aqAni.png")
            if (self.number % 10) == 3:
                self.pattern = 3
                self.turn = 1
                self.damage = 50
                self.rate = 93
                self.Md = 8
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 2:
                self.pattern = 3
                self.turn = 2
                self.damage = 140
                self.rate = 93
                self.Md = 16
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 1:
                self.pattern = 3
                self.turn = 3
                self.damage = 305
                self.rate = 93
                self.Md = 32
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 0:
                self.pattern = 3
                self.turn = 4
                self.damage = 500
                self.rate = 93
                self.Md = 64
                self.ally_target = False
                self.all_targets = True

        elif (self.number / 10) < 3:
            self.image = load_image("resource/skill/ter.png")
            self.animation = load_image("resource/animation/swordAni.png")
            if (self.number % 10) == 3:
                self.pattern = 2
                self.turn = 1
                self.damage = 48
                self.rate = 91
                self.Md = 6
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 2:
                self.pattern = 2
                self.turn = 2
                self.damage = 125
                self.rate = 91
                self.Md = 12
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 1:
                self.pattern = 2
                self.turn = 3
                self.damage = 375
                self.rate = 90
                self.Md = 24
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 0:
                self.pattern = 2
                self.turn = 4
                self.damage = 575
                self.rate = 90
                self.Md = 48
                self.ally_target = False
                self.all_targets = True

        elif (self.number / 10) < 4:
            self.image = load_image("resource/skill/vent.png")
            self.animation = load_image("resource/animation/swordAni.png")
            if (self.number % 10) == 3:
                self.pattern = 2
                self.turn = 1
                self.damage = 50
                self.rate = 90
                self.Md = 3
                self.ally_target = False
                self.all_targets = False

            elif (self.number % 10) == 2:
                self.pattern = 2
                self.turn = 2
                self.damage = 125
                self.rate = 90
                self.Md = 6
                self.ally_target = False
                self.all_targets = False

            elif (self.number % 10) == 1:
                self.pattern = 2
                self.turn = 3
                self.damage = 350
                self.rate = 90
                self.Md = 12
                self.ally_target = False
                self.all_targets = False

            elif (self.number % 10) == 0:
                self.pattern = 2
                self.turn = 4
                self.damage = 450
                self.rate = 90
                self.Md = 24
                self.ally_target = False
                self.all_targets = False

        elif (self.number / 10) < 5:
            self.image = load_image("resource/skill/per.png")
            self.animation = load_image("resource/animation/swordAni.png")
            if (self.number % 10) == 3:
                self.pattern = 5
                self.turn = 1
                self.damage = 40
                self.rate = 96
                self.Md = 6
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 2:
                self.pattern = 5
                self.turn = 2
                self.damage = 140
                self.rate = 96
                self.Md = 12
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 1:
                self.pattern = 5
                self.turn = 3
                self.damage = 340
                self.rate = 96
                self.Md = 24
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 0:
                self.pattern = 5
                self.turn = 4
                self.damage = 640
                self.rate = 95
                self.Md = 50
                self.ally_target = False
                self.all_targets = True

        elif (self.number / 10) < 6:
            self.image = load_image("resource/skill/fat.png")
            self.animation = load_image("resource/animation/swordAni.png")
            if (self.number % 10) == 4:
                self.pattern = 4
                self.turn = 1
                self.Md = 5
                self.damage = 2
                self.buff_type = 0
                self.ally_target = True
                self.all_targets = False

            elif (self.number % 10) == 3:
                self.pattern = 4
                self.turn = 1
                self.Md = 5
                self.damage = 2
                self.buff_type = 1
                self.ally_target = True
                self.all_targets = False

            elif (self.number % 10) == 2:
                self.pattern = 4
                self.turn = 2
                self.Md = 10
                self.damage = 2
                self.buff_type = 0
                self.ally_target = True
                self.all_targets = True

            elif (self.number % 10) == 1:
                self.pattern = 4
                self.turn = 2
                self.Md = 10
                self.damage = 2
                self.buff_type = 1
                self.ally_target = True
                self.all_targets = True

            elif (self.number % 10) == 0:
                self.pattern = 4
                self.turn = 4
                self.Md = 30
                self.damage = 3
                self.buff_type = 2
                self.ally_target = True
                self.all_targets = True

        elif (self.number / 10) < 7:
            self.image = load_image("resource/skill/met.png")
            self.animation = load_image("resource/animation/swordAni.png")
            if (self.number % 10) == 4:
                self.pattern = 4
                self.turn = 1
                self.Md = 5
                self.damage = -2
                self.buff_type = 0
                self.ally_target = False
                self.all_targets = False

            elif (self.number % 10) == 3:
                self.pattern = 4
                self.turn = 1
                self.Md = 5
                self.damage = -2
                self.buff_type = 1
                self.ally_target = False
                self.all_targets = False

            elif (self.number % 10) == 2:
                self.pattern = 4
                self.turn = 2
                self.Md = 10
                self.damage = -2
                self.buff_type = 0
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 1:
                self.pattern = 4
                self.turn = 2
                self.Md = 10
                self.damage = -2
                self.buff_type = 1
                self.ally_target = False
                self.all_targets = True

            elif (self.number % 10) == 0:
                self.pattern = 4
                self.turn = 4
                self.Md = 30
                self.damage = -3
                self.buff_type = 2
                self.ally_target = False
                self.all_targets = True

        elif (self.number / 10) < 8:
            self.image = load_image("resource/skill/cura.png")
            self.animation = load_image("resource/animation/swordAni.png")
            if (self.number % 10) == 2:
                self.pattern = 8
                self.turn = 1
                self.Md = 5
                self.damage = 75
                self.ally_target = True
                self.all_targets = False

            elif (self.number % 10) == 1:
                self.pattern = 8
                self.turn = 2
                self.Md = 15
                self.damage = 350
                self.ally_target = True
                self.all_targets = False

            elif (self.number % 10) == 0:
                self.pattern = 8
                self.turn = 3
                self.Md = 35
                self.damage = 999
                self.ally_target = True
                self.all_targets = False

        elif (self.number / 10) < 9:
            self.image = load_image("resource/skill/sana.png")
            self.animation = load_image("resource/animation/swordAni.png")
            if (self.number % 10) == 2:
                self.pattern = 8
                self.turn = 1
                self.Md = 10
                self.damage = 75
                self.ally_target = True
                self.all_targets = True

            elif (self.number % 10) == 1:
                self.pattern = 8
                self.turn = 2
                self.Md = 30
                self.damage = 350
                self.ally_target = True
                self.all_targets = True

            elif (self.number % 10) == 0:
                self.pattern = 8
                self.turn = 3
                self.Md = 70
                self.damage = 999
                self.ally_target = True
                self.all_targets = True

        elif (self.number / 10) < 10:
            self.image = load_image("resource/interface/sdInBattle.png")
            if (self.number % 10) == 1:
                self.pattern = 1
                self.turn = 1
                self.damage = 25
                self.rate = 95
                self.Md = 0
                self.ally_target = False
                self.all_targets = False
                self.animation = load_image("resource/animation/swordAni.png")

            elif (self.number % 10) == 0:
                self.pattern = 7
                self.turn = 1
                self.damage = 25
                self.rate = 95
                self.Md = 1
                self.ally_target = False
                self.all_targets = False
                self.animation = load_image("resource/animation/triggerAni.png")

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

    def get_buff_type(self):
        return self.buff_type

    def get_ally_target(self):
        return self.ally_target

    def get_all_targets(self):
        return self.all_targets

    def draw(self, locate, selected):
        self.image.clip_draw(0, self.number % 10 * 50, 200, 50, 360 + selected * 70, 270 - locate * 50)
        if selected == 1:
            Skill.space_bar.draw(280, 270 - locate * 50)

    def draw_before_use(self):
        if self.number == 90 or self.number == 91:
            self.image.clip_draw(50, 50 + self.number % 10 * 50, 200, 50, 600, 500)

        else:
            self.image.clip_draw(0, self.number % 10 * 50, 200, 50, 600, 500)

    def draw_animation(self, frame):
        self.animation.clip_draw(500 * int(frame), 0, 500, 500, 640, 460)
