from skill_data import Skill

class Card:
    def __init__(self, type):
        self.attribute = [0, 0, 0, 0, 0, 0, 0, 0]
        if type == 0:
            self.attribute = [0, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 1:
            self.attribute = [1, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [Skill(3), Skill(2), Skill(1), Skill(0), Skill(3)]

        elif type == 2:
            self.attribute = [2, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 3:
            self.attribute = [3, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 4:
            self.attribute = [4, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 5:
            self.attribute = [5, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 6:
            self.attribute = [6, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 7:
            self.attribute = [1, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 8:
            self.attribute = [2, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 9:
            self.attribute = [0, 0, 3, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 10:
            self.attribute = [0, 0, 0, 4, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 11:
            self.attribute = [0, 0, 4, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 12:
            self.attribute = [0, 0, 0, 0, 0, 0, 0, 0]
            self.skill = [11, 12, 12, 31, 21]

        elif type == 13:
            self.attribute = [3, 3, 3, 3, 3, 3, 3, 3]
            self.skill = [11, 12, 12, 31, 21]

    def getAttribute(self):
        return self.attribute

    def getSkill(self):
        return self.skill
