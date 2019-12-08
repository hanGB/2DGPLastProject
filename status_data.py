from skill_data import Skill


class Card:
    def __init__(self, type):
        self.attribute = [0, 0, 0, 0, 0, 0, 0, 0]
        if type == 0:
            self.attribute = [0, 0, 0, 1, 0, 0, 0, 0]
            self.skill = [Skill(23), Skill(43), Skill(13), Skill(72), Skill(81)]

        elif type == 1:
            self.attribute = [1, 0, 0, 2, 0, 0, 0, 0]
            self.skill = [Skill(33), Skill(2), Skill(31), Skill(0), Skill(3)]

        elif type == 2:
            self.attribute = [2, 0, 2, 3, 0, 0, 0, 0]
            self.skill = [Skill(13), Skill(12), Skill(11), Skill(10), Skill(13)]

        elif type == 3:
            self.attribute = [3, 0, 2, 2, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(30), Skill(3)]

        elif type == 4:
            self.attribute = [4, 0, 1, 2, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(32), Skill(1), Skill(0), Skill(3)]

        elif type == 5:
            self.attribute = [5, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(30), Skill(3)]

        elif type == 6:
            self.attribute = [6, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

        elif type == 7:
            self.attribute = [1, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

        elif type == 8:
            self.attribute = [2, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

        elif type == 9:
            self.attribute = [0, 0, 3, 0, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

        elif type == 10:
            self.attribute = [0, 0, 0, 4, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

        elif type == 11:
            self.attribute = [0, 0, 4, 0, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

        elif type == 12:
            self.attribute = [0, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

        elif type == 13:
            self.attribute = [3, 3, 3, 3, 3, 3, 3, 3]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

    def get_attribute(self):
        return self.attribute

    def get_skill(self):
        return self.skill
