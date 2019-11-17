from pico2d import *
import status_data


class Player:
    bar = None
    Bd_bar = None
    Md_bar = None
    pattern_image = None
    item_number = None
    item_sign = None
    down_fall = None

    def __init__(self, pattern, Bd, Md, stat):

        if Player.bar is None:
            Player.bar = load_image("resource/interface/BdMdBar.png")

        if Player.Bd_bar is None:
            Player.Bd_bar = load_image("resource/interface/BdBar.png")

        if Player.Md_bar is None:
            Player.Md_bar = load_image("resource/interface/MdBar.png")

        if Player.pattern_image is None:
            Player.pattern_image = load_image("resource/interface/pattern.png")

        if Player.down_fall is None:
            Player.down_fall = load_image("resource/interface/playerDownFall.png")

        self.pattern = pattern
        self.max_Bd = Bd
        self.max_Md = Md
        self.max_turn = 3
        self.stat = stat  # MatAtt, MindAtt, MatDef, MindDef, HitRate, AvoidRate
        self.buff = [0, 0]
        self.Bd = self.max_Bd
        self.Md = self.max_Md
        self.card = status_data.Card(1)
        self.down_level = 0
        self.turn = self.max_turn
        if self.pattern == 0:
            if Player.item_number is None:
                Player.item_number = load_image("resource/interface/itemNum.png")
            if Player.item_sign is None:
                Player.item_sign = load_image("resource/interface/itemSign.png")
            self.item = [3, 0, 0, 2, 0, 0, 0]

    def get_Bd(self):
        return self.Bd

    def set_Bd(self, Bd):
        self.Bd = Bd

    def get_Md(self):
        return self.Md

    def set_Md(self, Md):
        self.Md = Md

    def get_turn(self):
        return self.turn

    def set_turn(self, turn):
        self.turn = turn

    def get_card(self):
        return self.card

    def get_attribute(self):
        return self.card.getAttribute()

    def get_stat(self):
        return self.stat

    def get_down_level(self):
        return self.down_level

    def set_down_level(self, down_level):
        self.down_level = down_level

    def draw_bar(self, sit):
        Bd_rate = self.Bd / self.max_Bd
        Md_rate = self.Md / self.max_Md

        Player.bar.draw(1060, 200 - sit * 50)
        Player.Bd_bar.draw(972 - (1 - Bd_rate) * 72, 200 - sit * 50, 150 * Bd_rate, 20)
        Player.Md_bar.draw(1143 - (1 - Md_rate) * 72, 200 - sit * 50, 150 * Md_rate, 20)
        Player.pattern_image.clip_draw(self.pattern * 30, 0, 30, 30, 880, 200 - sit * 50)

        if self.down_level != 0:
            Player.down_fall.clip_draw((self.down_level - 1) * 100, 0, 100, 30, 815, 198 - sit * 50)

    def draw_item_number(self, number):
        if self.pattern == 0:
            for i in range(7):
                Player.item_number.clip_draw(20 * self.item[i], 0, 20, 30, 375, 275 - 30 * i)
                if i == number:
                    Player.item_sign.draw(315, 278 - 30 * i)
