from pico2d import *
import status


class Enemy:
    target = None
    BdBar = None
    name = None
    attribute = None

    def __init__(self, type):
        if Enemy.target is None:
            Enemy.target = load_image("2target.png")

        if Enemy.BdBar is None:
            Enemy.BdBar = load_image("2targetBd.png")

        if Enemy.name is None:
            Enemy.name = load_image("2enemyName.png")

        if Enemy.attribute is None:
            Enemy.attribute = load_image("2analWeakness.png")

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
            self.image = load_image("4-12lucipel.png")
            self.max_Bd = 5000
            self.status = [50, 50, 50, 50, 50]
            self.max_turn = 5

        elif type == 13:
            self.image = load_image("4-13luciper.png")
            self.max_Bd = 9999
            self.status = [99, 99, 19, 19, 19]
            self.max_turn = 9

        self.Bd = self.max_Bd
        self.buf = [0, 0]
        self.turn = self.max_turn
        self.down = 0
        self.card = status.Card(self.type)

    def get_Bd(self):
        return self.Bd

    def set_Bd(self, Bd):
        self.Bd = Bd

    def get_type(self):
        return self.type

    def get_attribute(self):
        return self.card.getAttribute()

    def draw(self, position, slt):
        self.image.draw(200 + position * 200, 300)

        Bd_rate = self.Bd / self.max_Bd

        if slt == 0:
            if self.type == 1:
                Enemy.target.draw(230 + position * 200 + 100, 250)
                Enemy.BdBar.draw(241 + position * 200 - (1 - Bd_rate) * 30 + 100, 266, Bd_rate * 60, 10)
            elif self.type == 2 or self.type == 3 or self.type == 4 or self.type == 6:
                Enemy.target.draw(230 + position * 200 + 100, 310)
                Enemy.BdBar.draw(241 + position * 200 - (1 - Bd_rate) * 30 + 100, 326, Bd_rate * 60, 10)
            else:
                Enemy.target.draw(230 + position * 200 + 100, 340)
                Enemy.BdBar.draw(241 + position * 200 - (1 - Bd_rate) * 30 + 100, 356, Bd_rate * 60, 10)

    def draw_attribute_data(self):
        Enemy.name.clip_draw(0, 400 - self.type * 30, 250, 30, 200, 235)
        for n in range(8):
            if self.card.attribute[n] != 0:
                if n < 4:
                    Enemy.attribute.clip_draw((self.card.attribute[n] - 1) * 60, 0, 60, 20, 90 + 67 * n, 145)
                else:
                    Enemy.attribute.clip_draw((self.card.attribute[n] - 1) * 60, 0, 60, 20, 90 + 67 * (n - 4), 64)
