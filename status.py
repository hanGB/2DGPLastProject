from pico2d import *
import os


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
    def __init__(self, number, attribute, turn, type, damage, rate):
        # type에 따라 damage가 어디에 적용되는 지 달라진다.

        basic_dir = os.getcwd()
        now_dir = os.path.join(basic_dir, "resource/skill")
        os.chdir(now_dir)

        self.number = number

        if (number / 10) <= 1:
            self.image = load_image("ig.png")
        elif (number / 10) <= 2:
            self.image = load_image("aq.png")

        self.attribute = attribute
        self.turn = turn
        self.type = type
        self.damage = damage
        self.rate = rate

    def draw(self, locate):
        self.image.clip_draw((self.number % 10) * 160, 0, 160, 260, locate * 50, 100)


