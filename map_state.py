from pico2d import *
import game_framework
import battle_state
import title_state

name = "map_state"


class Room:
    door = None
    background_map = None

    def __init__(self, n, e, s, w):
        # n,s,w,e는 True(1), False(0)를 가지며 door_location 값이 0일 경우 없다.

        if Room.door is None:
            Room.door = [load_image('1frontdoor.png'), load_image('1leftdoor.png'), load_image('1rightdoor.png'),
                         load_image('1dialeftdoor.png'), load_image('1diarightdoor.png')]
        if Room.background_map is None:
            Room.background_map = [load_image('1colormap.png'), load_image('1colormapdia.png')]

        # door_location - 1이 실제 사용 값
        self.door_location = [(2 * w, 1 * n, 3 * e), (4 * n, 0,  5 * e), (2 * n, 1 * e, 3 * s), (4 * e, 0, 5 * s),
                         (2 * e, 1 * s, 3 * w) , (4 * s, 0, 5 * w), (2 * s, 1 * w, 3 * n), (4 * w, 0, 5 * n)]
        self.maptype = 0

    def update(self, turn, sight):
        if turn == 'q':
            if sight != self.maptype:
                self.maptype = sight
            self.maptype = (self.maptype - 1) % 8
        elif turn == 'e':
            if sight != self.maptype:
                self.maptype = sight
            self.maptype = (self.maptype + 1) % 8
        elif turn == 's':
            if sight != self.maptype:
                self.maptype = sight
            self.maptype = (self.maptype + 4) % 8

    def draw(self):
        Room.background_map[self.maptype % 2].draw(640, 360)
        for i in range(0, 3):
            if self.door_location[self.maptype][i] != 0:
                Room.door[self.door_location[self.maptype][i] - 1].draw(640, 360)


room_connect_data = (((0, 1), (2, 3)), ((4, 0), (2, 2)),
                         ((4, 3), (6, 1)), ((6, 0), (0, 2)))

map = None
sight = None
room = None


def enter():
    global room
    global map
    global sight

    # test
    # game_framework.push_state(battle_state)
    #

    map = 0
    sight = 0
    room = (Room(1, 1, 0, 0), Room(0, 1, 1, 0), Room(0, 0, 1, 1), Room(1, 0, 0, 1))


def exit():
    global room
    global map
    global sight

    del (room)
    del (map)
    del (sight)


def pause():
    pass


def resume():
    pass


def handle_events():
    global map
    global sight
    global room
    global room_connect_data

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            # 시점 이동
            if event.key == SDLK_q or event.key == SDLK_LEFT:
                room[map].update('q', sight)
                sight = (sight - 1) % 8
            elif event.key == SDLK_e or event.key == SDLK_RIGHT:
                room[map].update('e', sight)
                sight = (sight + 1) % 8
            elif event.key == SDLK_DOWN:
                room[map].update('s', sight)
                sight = (sight + 4) % 8
            # 방 이동
            elif event.key == SDLK_UP:
                for i in range(0, 2):
                    if room_connect_data[map][i][0] == sight:
                        map = room_connect_data[map][i][0]

            # 임시 배틀 인카운트 키
            elif event.key == SDLK_b:
                game_framework.push_state(battle_state)
            elif event.key == SDLK_ESCAPE:
                game_framework.change_state(title_state)


def update():
    pass


def draw():
    clear_canvas()

    room[map].draw()

    update_canvas()
