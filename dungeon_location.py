FIRST, APARTMENT_ONE, APARTMENT_TWO, TOWER, PYRAMID = range(5)


class DungeonLocation:
    def __init__(self, type):
        self.location = 0

        if type == FIRST:
            self.x1 = 150
            self.y1 = 1230
            self.x2 = 700
            self.y2 = 1370

        elif type == APARTMENT_ONE:
            self.x1 = 150
            self.y1 = 1230
            self.x2 = 1900
            self.y2 = 1430

        elif type == APARTMENT_TWO:
            self.x1 = 1300
            self.y1 = 1500
            self.x2 = 1850
            self.y2 = 1680

        elif type == TOWER:
            self.x1 = 1730
            self.y1 = 1825
            self.x2 = 1860
            self.y2 = 1860

        elif type == PYRAMID:
            self.x1 = 970
            self.y1 = 1130
            self.x2 = 690
            self.y2 = 1920

    def set_location(self, location):
        self.location = location

    def get_bb(self):

        x_left = self.x1 % 3840
        x_right = self.x2 % 3840

        y_bottom = self.y1 % 2160
        y_top = self.y2 % 2160

        if self.location == 1:
            x_left = 3840 - x_left
            x_right = 3840 - x_right

        elif self.location == 2:
            y_bottom = 2160 - y_bottom
            y_top = 2160 - y_top

        elif self.location == 3:
            x_left = 3840 - x_left
            x_right = 3840 - x_right
            y_bottom = 2160 - y_bottom
            y_top = 2160 - y_top

        return x_left, y_bottom, x_right, y_top
