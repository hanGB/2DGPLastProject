from skill_data import Skill

NORMAL, AWFUL, WEAK, HALF, NON, REVEN, SHOCK = range(7)


class Card:
    def __init__(self, type):
        self.attribute = [NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL]
        if type == 0:
            self.attribute = [NORMAL, NON, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NON]
            self.skill = [Skill(41), Skill(11), Skill(31), Skill(61), Skill(71)]

        elif type == 1:
            self.attribute = [NORMAL, NORMAL, WEAK, WEAK, NORMAL, NORMAL, NORMAL, NORMAL]
            self.skill = [Skill(54), Skill(53)]

        elif type == 2:
            self.attribute = [NORMAL, NORMAL, WEAK, HALF, NORMAL, NORMAL, NORMAL, NORMAL]
            self.skill = [Skill(3), Skill(64), Skill(63)]

        elif type == 3:
            self.attribute = [NORMAL, NORMAL, NORMAL, HALF, WEAK, NORMAL, NORMAL, NORMAL]
            self.skill = [Skill(13), Skill(72)]

        elif type == 4:
            self.attribute = [NORMAL, HALF, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, WEAK]
            self.skill = [Skill(62), Skill(61), Skill(33)]

        elif type == 5:
            self.attribute = [NORMAL, WEAK, NORMAL, NORMAL, NORMAL, NON, NORMAL, WEAK]
            self.skill = [Skill(43), Skill(82)]

        elif type == 6:
            self.attribute = [NORMAL, NORMAL, AWFUL, NON, NORMAL, NORMAL, NORMAL, NORMAL]
            self.skill = [Skill(42), Skill(54), Skill(53), Skill(52), Skill(51)]

        elif type == 7:
            self.attribute = [NORMAL, WEAK, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, REVEN]
            self.skill = [Skill(1), Skill(64), Skill(63), Skill(62), Skill(61)]

        elif type == 8:
            self.attribute = [NORMAL, WEAK, NORMAL, HALF, NORMAL, NORMAL, NORMAL, NORMAL]
            self.skill = [Skill(11), Skill(52), Skill(54), Skill(12)]

        elif type == 9:
            self.attribute = [NORMAL, SHOCK, HALF, AWFUL, NORMAL, NORMAL, NORMAL, WEAK]
            self.skill = [Skill(21), Skill(51), Skill(53), Skill(22)]

        elif type == 10:
            self.attribute = [NORMAL, NORMAL, WEAK, NON, NORMAL, NORMAL, NORMAL, NORMAL]
            self.skill = [Skill(0), Skill(54), Skill(1)]

        elif type == 11:
            self.attribute = [NORMAL, NORMAL, NON, NORMAL, WEAK, NORMAL, NORMAL, NON]
            self.skill = [Skill(30), Skill(71), Skill(31)]

        elif type == 12:
            self.attribute = [NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL, NORMAL]
            self.skill = [Skill(52), Skill(53), Skill(40), Skill(30), Skill(72)]

        elif type == 13:
            self.attribute = [HALF, HALF, HALF, HALF, HALF, HALF, HALF, HALF]
            self.skill = [Skill(0), Skill(10), Skill(20), Skill(30), Skill(40), Skill(50), Skill(60)]

    def get_attribute(self):
        return self.attribute

    def get_skill(self):
        return self.skill
