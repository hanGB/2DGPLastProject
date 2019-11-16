from pico2d import *
import room_data
import random
import battle_state
import game_framework

TIME_PER_CAMERA_MOVE = 2
CAMERA_MOVE_PER_TIME = 1.0 / TIME_PER_CAMERA_MOVE
FRAMES_PER_CAMERA_MOVE = 8

LEFT_DOWN, RIGHT_DOWN, LEFT_UP, RIGHT_UP, UP_KEY, DOWN_KEY = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_q): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_e): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_q): LEFT_UP,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_e): RIGHT_UP,
    (SDL_KEYUP, SDLK_UP): UP_KEY,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_KEY,
}


class NormalMap:
    @staticmethod
    def enter(map, event):
        if event == LEFT_DOWN:
            map.direction = -1
            map.rooms[map.location_y][map.location_x].turn_sight('q')
            map.sub_counter = 0
        elif event == LEFT_UP or event == RIGHT_UP:
            map.direction = 0

        elif event == RIGHT_DOWN:
            map.direction = 1
            map.rooms[map.location_y][map.location_x].turn_sight('e')
            map.sub_counter = 0

        elif event == DOWN_KEY:
            map.rooms[map.location_y][map.location_x].turn_sight('s')

        elif event == UP_KEY:
            if map.rooms[map.location_y][map.location_x].is_door_in_front_player() is True:
                now_direction = map.rooms[map.location_y][map.location_x].get_map_direction()
                if now_direction == 0:
                    map.location_y += 1
                elif now_direction == 2:
                    map.location_x += 1
                elif now_direction == 4:
                    map.location_y -= 1
                elif now_direction == 6:
                    map.location_x -= 1
                map.rooms[map.location_y][map.location_x].set_map_direction(now_direction)
                battle_outbreak_rate = random.randint(0, 3)
                if battle_outbreak_rate == 0:
                    game_framework.push_state(battle_state)

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(map):
        if map.direction == 1 or map.direction == -1:
            map.sub_counter += game_framework.frame_time * FRAMES_PER_CAMERA_MOVE * CAMERA_MOVE_PER_TIME

            if map.sub_counter > 1:
                map.sub_counter = 0

                if map.direction == 1:
                    map.rooms[map.location_y][map.location_x].turn_sight('e')
                elif map.direction == -1:
                    map.rooms[map.location_y][map.location_x].turn_sight('q')

    @staticmethod
    def draw(map):
        map.rooms[map.location_y][map.location_x].draw()
        map.compass.clip_draw(map.rooms[map.location_y][map.location_x].get_map_direction() * 200, 0,
                              200, 150, 1150, 100)
        map.room_number.clip_draw(20 * map.location_y, 0, 20, 30, 1210, 140)
        map.room_number.clip_draw(20 * map.location_x, 0, 20, 30, 1100, 55)


next_state_table = {
    NormalMap: {LEFT_DOWN: NormalMap, RIGHT_DOWN: NormalMap,
                LEFT_UP: NormalMap, RIGHT_UP: NormalMap,
                UP_KEY: NormalMap, DOWN_KEY: NormalMap}
}


class Map:
    compass = None
    room_number = None

    def __init__(self, type):
        if Map.compass is None:
            Map.compass = load_image("resource/interface/compass.png")
        if Map.room_number is None:
            Map.room_number = load_image("resource/interface/roomNum.png")

        self.direction = 0
        self.sub_counter = 0
        if type == 0:
            # 0번 던전의 맵 데이터
            # 0, 4 S에서 출발해서 6, 2 N으로 나가는 던전
            self.rooms = [[room_data.Room(1, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 1, 1, 0), room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 1, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(1, 0, 0, 1), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(1, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 1, 1, 0), room_data.Room(1, 0, 0, 1), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 1, 1, 0), room_data.Room(1, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(1, 0, 0, 1), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 1, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 1, 1, 0), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 1, 1), room_data.Room(0, 0, 0, 1)]]
            self.location_y = 0
            self.location_x = 4

        else:
            # 초기화 된 던전 맵
            self.rooms = [[room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)]]
            self.location_x = 0
            self.location_y = 0

        self.event_que = []
        self.cur_state = NormalMap
        self.cur_state.enter(self, None)

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def handle_events(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[event.type, event.key]
            self.add_event(key_event)
