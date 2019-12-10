from pico2d import *


class Room:
    door = None
    background_map = None

    def __init__(self, n, e, s, w):
        # n,s,w,e는 True(1), False(0)를 가지며 door_location 값이 0일 경우 없다.

        if Room.door is None:
            Room.door = [[load_image('resource/map/frontdoor.png'), load_image('resource/map/leftdoor.png')
                         , load_image('resource/map/rightdoor.png'), load_image('resource/map/dialeftdoor.png')
                         , load_image('resource/map/diarightdoor.png')],
                        [load_image('resource/map/apartfrontdoor.png'), load_image('resource/map/apartleftdoor.png')
                            , load_image('resource/map/apartrightdoor.png'), load_image('resource/map/apartdialeftdoor.png')
                            , load_image('resource/map/apartdiarightdoor.png')],
                        [load_image('resource/map/towerfrontdoor.png'), load_image('resource/map/towerleftdoor.png')
                            , load_image('resource/map/towerrightdoor.png'), load_image('resource/map/towerdialeftdoor.png')
                            , load_image('resource/map/towerdiarightdoor.png')],
                        [load_image('resource/map/pyramidfrontdoor.png'), load_image('resource/map/pyramidleftdoor.png')
                            , load_image('resource/map/pyramidrightdoor.png'), load_image('resource/map/pyramiddialeftdoor.png')
                            , load_image('resource/map/pyramiddiarightdoor.png')]]

        if Room.background_map is None:
            Room.background_map = [[load_image('resource/map/colormap.png'),
                                    load_image('resource/map/colormapdia.png')],
                                   [load_image('resource/map/apartmap.png'),
                                    load_image('resource/map/apartmapdia.png')],
                                   [load_image('resource/map/towercolormap.png'),
                                    load_image('resource/map/towercolormapdia.png')],
                                   [load_image('resource/map/pyramidcolormap.png'),
                                    load_image('resource/map/pyramidcolormapdia.png')]]

        # door_location - 1이 실제 사용 값
        self.door_location = [(2 * w, 1 * n, 3 * e), (4 * n, 0,  5 * e), (2 * n, 1 * e, 3 * s), (4 * e, 0, 5 * s),
                              (2 * e, 1 * s, 3 * w), (4 * s, 0, 5 * w), (2 * s, 1 * w, 3 * n), (4 * w, 0, 5 * n)]
        self.map_direction = 0

    def turn_sight(self, turn):
        if turn == 'q':
            self.map_direction = (self.map_direction - 1) % 8
        elif turn == 'e':
            self.map_direction = (self.map_direction + 1) % 8
        elif turn == 's':
            self.map_direction = (self.map_direction + 4) % 8

    def get_map_direction(self):
        return self.map_direction

    def set_map_direction(self, direction):
        self.map_direction = direction

    def is_door_in_front_player(self):
        if self.door_location[self.map_direction][1] != 0:
            return True

    def update(self):
        pass

    def draw(self, type):
        Room.background_map[type][self.map_direction % 2].draw(640, 360)
        for i in range(0, 3):
            if self.door_location[self.map_direction][i] != 0:
                Room.door[type][self.door_location[self.map_direction][i] - 1].draw(640, 360)
