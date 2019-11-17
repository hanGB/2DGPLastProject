from pico2d import *
import status_data
import game_framework

TIME_PER_SHOW = 0.5
SHOW_PER_TIME = 1.0 / TIME_PER_SHOW
FRAMES_PER_SHOW = 1


class Enemy:
    target = None
    BdBar = None
    name = None
    attribute = None
    down_fall = None
    show_hit = None

    def __init__(self, type):
        if Enemy.target is None:
            Enemy.target = load_image("resource/interface/target.png")

        if Enemy.BdBar is None:
            Enemy.BdBar = load_image("resource/interface/targetBd.png")

        if Enemy.name is None:
            Enemy.name = load_image("resource/interface/enemyName.png")

        if Enemy.attribute is None:
            Enemy.attribute = load_image("resource/interface/analWeakness.png")

        if Enemy.down_fall is None:
            Enemy.down_fall = load_image("resource/interface/enemyDownFall.png")

        if Enemy.show_hit is None:
            Enemy.show_hit = load_image("resource/interface/attackWeakness.png")

        self.type = type

        if type == 0:
            self.image = load_image("resource/enemy/0alice.png")
            self.max_Bd = 2000
            self.stat = [35, 35, 35, 35, 35, 35]
            self.max_turn = 5

        elif type == 1:
            self.image = load_image("resource/enemy/1slame.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 1

        elif type == 2:
            self.image = load_image("resource/enemy/2jack_o_lantern.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 1

        elif type == 3:
            self.image = load_image("resource/enemy/3jack_frost.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 2

        elif type == 4:
            self.image = load_image("resource/enemy/4loa.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 2

        elif type == 5:
            self.image = load_image("resource/enemy/5high_pixie.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 2

        elif type == 6:
            self.image = load_image("resource/enemy/6kaiwan.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 3

        elif type == 7:
            self.image = load_image("resource/enemy/7legion.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 3

        elif type == 8:
            self.image = load_image("resource/enemy/8naga.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 3

        elif type == 9:
            self.image = load_image("resource/enemy/9dol.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 3

        elif type == 10:
            self.image = load_image("resource/enemy/10surt.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 4

        elif type == 11:
            self.image = load_image("resource/enemy/11norn.png")
            self.max_Bd = 100
            self.stat = [10, 10, 10, 10, 10, 10]
            self.max_turn = 4

        elif type == 12:
            self.image = load_image("resource/enemy/12lucipel.png")
            self.max_Bd = 5000
            self.stat = [50, 50, 50, 50, 50, 50]
            self.max_turn = 5

        elif type == 13:
            self.image = load_image("resource/enemy/13luciper.png")
            self.max_Bd = 9999
            self.stat = [99, 99, 99, 99, 99, 99]
            self.max_turn = 9

        self.Bd = self.max_Bd
        self.buff = [0, 0]
        self.turn = self.max_turn
        self.down_level = 0
        self.card = status_data.Card(self.type)
        self.Md = 9999
        self.hit_weakness = -1
        self.time_to_show_hit = 0

    def get_Bd(self):
        return self.Bd

    def set_Bd(self, Bd):
        self.Bd = Bd

    def get_Md(self):
        return self.Md

    def set_Md(self, Md):
        self.Md = Md

    def get_max_turn(self):
        return self.max_turn

    def get_turn(self):
        return self.turn

    def set_turn(self, turn):
        self.turn = turn

    def get_type(self):
        return self.type

    def get_attribute(self):
        return self.card.get_attribute()

    def get_down_level(self):
        return self.down_level

    def set_down_level(self, down_level):
        self.down_level = down_level

    def get_buff(self):
        return self.buff

    def set_buff(self, buff):
        self.buff = buff

    def get_stat(self):
        return self.stat

    def get_card(self):
        return self.card

    def set_hit_weakness(self, hit_weakness):
        self.hit_weakness = hit_weakness

    def draw(self, position, slt):
        if self.type == 1:
            self.image.draw(200 + position * 200, 255)
        else:
            self.image.draw(200 + position * 200, 300)

        Bd_rate = self.Bd / self.max_Bd

        if self.type == 1:
            if slt == 0:
                Enemy.target.draw(230 + position * 200 + 100, 240)
                Enemy.BdBar.draw(241 + position * 200 - (1 - Bd_rate) * 30 + 100, 256, Bd_rate * 60, 10)
            if self.down_level != 0:
                Enemy.down_fall.clip_draw((self.down_level - 1) * 100, 0, 100, 30, 230 + position * 200 + 155, 235)

            if self.hit_weakness != -1:
                Enemy.show_hit.clip_draw(self.hit_weakness * 200, 0, 200, 50, 230 + position * 200 + 180, 260)
                self.time_to_show_hit += game_framework.frame_time * FRAMES_PER_SHOW * SHOW_PER_TIME

                if self.time_to_show_hit > 1:
                    self.hit_weakness = -1
                    self.time_to_show_hit = 0

        elif self.type == 2 or self.type == 3 or self.type == 4 or self.type == 6:
            if slt == 0:
                Enemy.target.draw(230 + position * 200 + 100, 310)
                Enemy.BdBar.draw(241 + position * 200 - (1 - Bd_rate) * 30 + 100, 326, Bd_rate * 60, 10)
            if self.down_level != 0:
                Enemy.down_fall.clip_draw((self.down_level - 1) * 100, 0, 100, 30, 230 + position * 200 + 155, 305)

            if self.hit_weakness != -1:
                Enemy.show_hit.clip_draw(self.hit_weakness * 200, 0, 200, 50, 230 + position * 200 + 180, 330)
                self.time_to_show_hit += game_framework.frame_time * FRAMES_PER_SHOW * SHOW_PER_TIME

                if self.time_to_show_hit > 1:
                    self.hit_weakness = -1
                    self.time_to_show_hit = 0

        else:
            if slt == 0:
                Enemy.target.draw(230 + position * 200 + 100, 340)
                Enemy.BdBar.draw(241 + position * 200 - (1 - Bd_rate) * 30 + 100, 356, Bd_rate * 60, 10)
            if self.down_level != 0:
                Enemy.down_fall.clip_draw((self.down_level - 1) * 100, 0, 100, 30, 230 + position * 200 + 155, 335)

            if self.hit_weakness != -1:
                Enemy.show_hit.clip_draw(self.hit_weakness * 200, 0, 200, 50, 230 + position * 200 + 180, 360)
                self.time_to_show_hit += game_framework.frame_time * FRAMES_PER_SHOW * SHOW_PER_TIME

                if self.time_to_show_hit > 1:
                    self.hit_weakness = -1
                    self.time_to_show_hit = 0

    def draw_attribute_data(self):
        Enemy.name.clip_draw(0, 400 - self.type * 30, 250, 30, 200, 235)
        for n in range(8):
            if self.card.attribute[n] != 0:
                if n < 4:
                    Enemy.attribute.clip_draw((self.card.attribute[n] - 1) * 60, 0, 60, 20, 90 + 67 * n, 145)
                else:
                    Enemy.attribute.clip_draw((self.card.attribute[n] - 1) * 60, 0, 60, 20, 90 + 67 * (n - 4), 64)