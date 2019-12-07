from pico2d import *
import status_data
import game_framework

MATTER_ATTACK, MIND_ATTACK, MATTER_DEFENCE, MIND_DEFENCE, HIT_RATE, AVOID_RATE = range(6)

TIME_PER_SHOW = 2
SHOW_PER_TIME = 1.0 / TIME_PER_SHOW
FRAMES_PER_SHOW = 8


class Player:
    bar = None
    Bd_bar = None
    Md_bar = None
    pattern_image = None
    item_number = None
    item_sign = None
    down_fall = None
    show_hit = None
    level_up_image = None
    level_number = None
    buff_coin = None

    def __init__(self, pattern, Bd, Md, stat):

        if Player.buff_coin is None:
            Player.buff_coin = load_image("resource/interface/buffCoin.png")

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

        if Player.show_hit is None:
            Player.show_hit = load_image("resource/interface/attackWeakness.png")

        if Player.level_up_image is None:
            Player.level_up_image = load_image("resource/interface/levelUp.png")

        if Player.level_number is None:
                Player.level_number = load_image("resource/interface/roomNum.png")

        self.pattern = pattern
        self.max_Bd = Bd
        self.max_Md = Md
        self.max_turn = 3
        self.level = 10
        self.exp = 0
        self.stat = stat  # MatAtt, MindAtt, MatDef, MindDef, HitRate, AvoidRate
        self.buff = [0, 0]
        self.Bd = self.max_Bd
        self.Md = self.max_Md
        self.card_type = 0
        self.card = status_data.Card(self.card_type)
        self.down_level = 0
        self.turn = self.max_turn

        if self.pattern == 8:
            if Player.item_number is None:
                Player.item_number = load_image("resource/interface/itemNum.png")

            if Player.item_sign is None:
                Player.item_sign = load_image("resource/interface/itemSign.png")
            self.item = [3, 0, 0, 2, 0, 0, 0]

        self.hit_weakness = -1
        self.time_to_show_hit = 0
        self.level_up = False
        self.level_up_counter = 0

    def __getstate__(self):
        state = {'pattern': self.pattern, 'max_Bd': self.max_Bd, 'max_Md': self.max_Md,
                 'Bd': self.Bd, 'Md': self.Md, "max_turn": self.max_turn, 'level': self.level,
                 'exp': self.exp, "stat": self.stat, "card_type ": self.card_type}
        return state

    def __setstate__(self, state):
        self.__init__(state['pattern'], state['max_Bd'], state['max_Md'], state["stat"])
        self.__dict__.update(state)

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
        return self.card.get_attribute()

    def get_stat(self):
        return self.stat

    def get_max_Bd(self):
        return self.max_Bd

    def get_max_Md(self):
        return self.max_Md

    def get_max_turn(self):
        return self.max_turn

    def get_buff(self):
        return self.buff

    def set_buff(self, buff):
        self.buff = buff

    def set_hit_weakness(self, hit_weakness):
        self.hit_weakness = hit_weakness

    def set_time_to_show_hit(self):
        self.time_to_show_hit = 0

    def get_down_level(self):
        return self.down_level

    def set_down_level(self, down_level):
        self.down_level = down_level

    def set_card(self, card):
        self.card = card

    def get_item(self):
        return self.item

    def set_item(self, type, number):
        self.item[type] += number

    def give_exp(self, exp):
        if self.level != 99:
            if self.Bd > 0:
                self.exp += exp
                if self.exp > self.level * 30:
                    self.exp = self.exp - self.level * 30
                    self.level += 1
                    self.level_up = True

                    if self.pattern == 8:
                        self.max_Bd += 7
                        self.max_Md += 7
                        if self.level % 2 == 0:
                            self.stat[MATTER_ATTACK] += 1
                            self.stat[MATTER_DEFENCE] += 1
                            self.stat[HIT_RATE] += 1
                        else:
                            self.stat[MIND_ATTACK] += 1
                            self.stat[MIND_DEFENCE] += 1
                            self.stat[AVOID_RATE] += 1

                    elif self.pattern == 0:
                        self.max_Bd += 9
                        self.max_Md += 5
                        if self.level % 3 == 0:
                            self.stat[MATTER_ATTACK] += 1
                            self.stat[MATTER_DEFENCE] += 1
                        elif self.level % 3 == 1:
                            self.stat[MATTER_ATTACK] += 1
                            self.stat[MIND_ATTACK] += 1
                            self.stat[MIND_DEFENCE] += 1
                        elif self.level % 3 == 2:
                            self.stat[MATTER_ATTACK] += 1
                            self.stat[AVOID_RATE] += 1
                            self.stat[HIT_RATE] += 1

                    elif self.pattern == 3:
                        self.max_Bd += 8
                        self.max_Md += 6
                        if self.level % 2 == 0:
                            self.stat[MATTER_ATTACK] += 2
                            self.stat[MATTER_DEFENCE] += 1
                            self.stat[HIT_RATE] += 1
                        else:
                            self.stat[MIND_DEFENCE] += 1
                            self.stat[AVOID_RATE] += 1

                    elif self.pattern == 5:
                        self.max_Bd += 6
                        self.max_Md += 9
                        if self.level % 2 == 0:
                            self.stat[MATTER_ATTACK] += 2
                            self.stat[MATTER_DEFENCE] += 1
                            self.stat[HIT_RATE] += 1
                        else:
                            self.stat[MIND_DEFENCE] += 1
                            self.stat[AVOID_RATE] += 1

                    elif self.pattern == 6:
                        self.max_Bd += 6
                        self.max_Md += 8
                        if self.level % 3 == 0:
                            self.stat[MIND_ATTACK] += 1
                            self.stat[MATTER_ATTACK] += 1
                            self.stat[MATTER_DEFENCE] += 1
                        elif self.level % 3 == 1:
                            self.stat[MIND_ATTACK] += 1
                            self.stat[MIND_ATTACK] += 1
                            self.stat[MIND_DEFENCE] += 1
                        elif self.level % 3 == 2:
                            self.stat[MIND_ATTACK] += 1
                            self.stat[AVOID_RATE] += 1
                            self.stat[HIT_RATE] += 1

    def draw_bar(self, sit):
        Bd_rate = self.Bd / self.max_Bd
        Md_rate = self.Md / self.max_Md

        Player.bar.draw(1060, 200 - sit * 50)
        Player.Bd_bar.draw(972 - (1 - Bd_rate) * 72, 200 - sit * 50, 150 * Bd_rate, 20)
        Player.Md_bar.draw(1143 - (1 - Md_rate) * 72, 200 - sit * 50, 150 * Md_rate, 20)
        Player.pattern_image.clip_draw(self.pattern * 30, 0, 30, 30, 880, 200 - sit * 50)

        if self.buff[0] < 0:
            buff_count = self.buff[0] * -1
            for i in range(buff_count):
                Player.buff_coin.clip_draw(5, 0, 5, 5, 897 + i * 5, 214 - sit * 50)
        elif self.buff[0] > 0:
            for i in range(self.buff[0]):
                Player.buff_coin.clip_draw(0, 0, 5, 5, 897 + i * 5, 214 - sit * 50)

        if self.buff[1] < 0:
            buff_count = self.buff[1] * -1
            for i in range(buff_count):
                Player.buff_coin.clip_draw(5, 0, 5, 5, 897 + i * 5, 184 - sit * 50)
        elif self.buff[1] > 0:
            for i in range(self.buff[1]):
                Player.buff_coin.clip_draw(0, 0, 5, 5, 897 + i * 5, 184 - sit * 50)

        if self.down_level != 0:
            Player.down_fall.clip_draw((self.down_level - 1) * 100, 0, 100, 30, 815, 198 - sit * 50)

        if self.hit_weakness != -1:
            Player.show_hit.clip_draw(self.hit_weakness * 200, 0, 200, 50, 1000, 198 - sit * 50)
            self.time_to_show_hit += game_framework.frame_time * FRAMES_PER_SHOW * SHOW_PER_TIME

            if self.time_to_show_hit > 1:
                self.hit_weakness = -1
                self.time_to_show_hit = 0

    def draw_bar_in_map(self, sit):
        Bd_rate = self.Bd / self.max_Bd
        Md_rate = self.Md / self.max_Md

        Player.bar.clip_draw(0, 0, 180, 50, 130, 550 - sit * 80)
        Player.bar.clip_draw(0, 0, 180, 50, 160, 520 - sit * 80)

        Player.Bd_bar.draw(127 - (1 - Bd_rate) * 72, 550 - sit * 80, 150 * Bd_rate, 20)
        Player.Md_bar.draw(157 - (1 - Md_rate) * 72, 520 - sit * 80, 150 * Md_rate, 20)

        Player.pattern_image.clip_draw(self.pattern * 30, 0, 30, 30, 30, 550 - sit * 80)

        level_units = self.level % 10
        level_tens = self.level / 10
        Player.level_number.clip_draw(20 * int(level_tens), 0, 20, 30, 20, 520 - sit * 80)
        Player.level_number.clip_draw(20 * int(level_units), 0, 20, 30, 37, 520 - sit * 80)

        if self.level_up:
            Player.level_up_image.draw(130, 550 - sit * 80)
            self.level_up_counter += game_framework.frame_time * FRAMES_PER_SHOW * SHOW_PER_TIME
            if self.level_up_counter > 10:
                self.level_up = False
                self.level_up_counter = 0

    def draw_item_number(self, number):
        if self.pattern == 8:
            for i in range(7):
                Player.item_number.clip_draw(20 * self.item[i], 0, 20, 30, 375, 275 - 30 * i)
                if i == number:
                    Player.item_sign.draw(315, 278 - 30 * i)

    def draw(self):
        pass

    def update(self):
        pass
