from pico2d import *
import os

open_canvas(1280, 720)

# 기본 디렉토리 저장
basic_dir = os.getcwd()

# 리소스가 있는 디렉토리 저장 및 이동

now_dir = os.path.join(basic_dir, "resource/enemy")
os.chdir(now_dir)
enemy = load_image('testdemon.png')


class BattleUi:
    def __init__(self):
        global now_dir

        now_dir = os.path.join(basic_dir, "resource/ui")
        os.chdir(now_dir)

        self.main_ui = load_image("newUi.png")
        self.turn_number = load_image("turnNumber.png")

    def draw(self, menu, act):
        if menu == 0:
            self.main_ui.clip_draw(act * 300, 0, 300, 300, 200, 180)
            self.turn_number.clip_draw(0 * 100, 0, 100, 150, 105, 175)


class Room:
    def __init__(self, n, e, s, w):
        # n,s,w,e는 True(1), False(0)를 가지며 door_location 값이 0일 경우 없다.
        global now_dir

        now_dir = os.path.join(basic_dir, "resource/map")
        os.chdir(now_dir)

        self.door = [load_image('frontdoor.png'), load_image('leftdoor.png'), load_image('rightdoor.png'),
                load_image('dialeftdoor.png'), load_image('diarightdoor.png')]
        self.background_map = [load_image('colormap.png'), load_image('colormapdia.png')]

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
        self.background_map[self.maptype % 2].draw(640, 360)
        for i in range(0, 3):
            if self.door_location[self.maptype][i] != 0:
                self.door[self.door_location[self.maptype][i] - 1].draw(640, 360)


def input_key_in_map():
    global map
    global sight
    global game
    global room
    global room_connect_data

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game = False
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


def input_key_in_battle():
    global sight
    global game
    global act

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game = False
        elif event.type == SDL_KEYDOWN:
            # 메뉴
            if event.key == SDLK_w:
                pass
            elif event.key == SDLK_f:
                pass
            elif event.key == SDLK_DOWN:
                act = (act + 1) % 6
                if act == 0:
                    act = 1
            elif event.key == SDLK_s:
                pass
            elif event.key == SDLK_d:
                pass
            elif event.key == SDLK_a or event.key == SDLK_LSHIFT:
                if act != 0:
                    act = 0
            elif event.key == SDLK_c:
                pass
            elif event.key == SDLK_SPACE:
                pass
            elif event.key == SDLK_TAB:
                pass


act = 0
game = True
i = 0
map = 0
sight = 0
room = (Room(1, 1, 0, 0), Room(0, 1, 1, 0), Room(0, 0, 1, 1), Room(1, 0, 0, 1))
room_connect_data = (((0, 1), (2, 3)), ((4, 0), (2, 2)),
                     ((4, 3), (6, 1)), ((6, 0), (0, 2)))
battleUi = BattleUi()
turn = 0
act = 0
where = 1

while game:
    clear_canvas()

    if where == 0:
        input_key_in_map()

    elif where == 1:
        input_key_in_battle()


    clear_canvas()
    room[map].draw()

    if where == 1:
        battleUi.draw(0, act)

    update_canvas()

close_canvas()
