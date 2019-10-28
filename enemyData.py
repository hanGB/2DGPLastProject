from pico2d import *


class Enemy:
    target = None
    BdBar = None

    def __init__(self, type):
        if Enemy.target is None:
            Enemy.target = load_image("2target.png")

        if Enemy.BdBar is None:
            Enemy.BdBar = load_image("2targetBd.png")

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

    def draw(self, position, slt):
        self.image.draw(200 + position * 200, 300)

        BdRate = self.Bd / self.max_Bd

        if slt == 0:
            if self.type == 1:
                Enemy.target.draw(230 + position * 200 + 100, 250)
                Enemy.BdBar.draw(241 + position * 200 - (1 - BdRate) * 30 + 100, 266, BdRate * 60, 10)
            elif self.type == 2 or self.type == 3 or self.type == 4 or self.type == 6:
                Enemy.target.draw(230 + position * 200 + 100, 310)
                Enemy.BdBar.draw(241 + position * 200 - (1 - BdRate) * 30 + 100, 326, BdRate * 60, 10)
            else:
                Enemy.target.draw(230 + position * 200 + 100, 340)
                Enemy.BdBar.draw(241 + position * 200 - (1 - BdRate) * 30 + 100, 356, BdRate * 60, 10)
