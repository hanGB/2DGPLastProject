import city_state

FIRST, APARTMENT_ONE, APARTMENT_TWO, TOWER, PYRAMID = range(5)


class DungeonLocation:
    def __init__(self, type):
        if type == FIRST:
            self.x1 = 160
            self.y1 = 1230
            self.x2 = 670
            self.y2 = 1445

        elif type == APARTMENT_ONE:
            self.x1 = 1080
            self.y1 = 1184
            self.x2 = 1890
            self.y2 = 1455

        elif type == APARTMENT_TWO:
            self.x1 = 1300
            self.y1 = 1455
            self.x2 = 1840
            self.y2 = 1680

        elif type == TOWER:
            self.x1 = 1710
            self.y1 = 1800
            self.x2 = 1905
            self.y2 = 1850

        elif type == PYRAMID:
            self.x1 = 135
            self.y1 = 1795
            self.x2 = 680
            self.y2 = 1925

    def get_bb(self):
        location = city_state.location_bar.get_location()

        x_left = self.x1
        x_right = self.x2

        y_bottom = self.y1
        y_top = self.y2

        if location == 0:
            temp = x_left
            x_left = 3840 - x_right
            x_right = 3840 - temp

        elif location == 2:
            temp = y_bottom
            y_bottom = 2160 - y_top
            y_top = 2160 - temp

        elif location == 3:
            temp = x_left
            x_left = 3840 - x_right
            x_right = 3840 - temp
            temp = y_top
            y_top = 2160 - y_bottom
            y_bottom = 2160 - temp

        return x_left, y_bottom, x_right, y_top
