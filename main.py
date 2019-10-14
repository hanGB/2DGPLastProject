from pico2d import *
import os

open_canvas(1280, 720)

# 기본 디렉토리 저장
basic_dir = os.getcwd()

# 리소스가 있는 디렉토리 저장 및 이동

now_dir = os.path.join(basic_dir, "resource/enemy")
os.chdir(now_dir)
enemy = load_image('testdemon.png')

now_dir = os.path.join(basic_dir, "resource/ui")
os.chdir(now_dir)

ui = load_image('ui.png')
ui2 = load_image('ui2.png')
uiAct = load_image('uiAct.png')
uiBack = load_image('uiBackground.png')


class Room:
    def __init__(self, n, w, e, s):
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


    def update(self, turn):
        if turn == 'q':
            self.maptype = (self.maptype - 1) % 8
        elif turn == 'e':
            self.maptype = (self.maptype + 1) % 8
        elif turn == 's':
            self.maptype = (self.maptype + 4) % 8


    def draw(self):
        self.background_map[self.maptype % 2].draw(640, 360)
        for i in range(0, 3):
            if self.door_location[self.maptype][i] != 0:
                self.door[self.door_location[self.maptype][i] - 1].draw(640, 360)


def show_ui():
    global act

    uiBack.draw(640, 125)
    ui.clip_draw(0, 0, 250, 100, 160, 190)
    ui.clip_draw(250, 0, 230, 100, 153, 120)
    ui2.clip_draw(0, 0, 250, 100, 460, 192)
    ui2.clip_draw(250, 0, 230, 100, 454, 52)
    ui2.clip_draw(500, 0, 230, 100, 454, 122)
    uiAct.clip_draw(300 * act, 0, 300, 100, 190, 58)


def out_of_program():
    global game

    for event in events:
        if event.type == SDL_QUIT:
            game = False


def input_key_in_battle():
    global act
    global game

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_DOWN:
                act = act % 3 + 1


def input_key_in_map():
    global map
    global game
    global room

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game = False
        elif event.type == SDL_KEYDOWN:
            # 시점 이동
            if event.key == SDLK_q or event.key == SDLK_LEFT:
                room.update('q')
            elif event.key == SDLK_e or event.key == SDLK_RIGHT:
                room.update('e')
            elif event.key == SDLK_DOWN:
                room.update('s')
            # 방 이동
            elif event.key == SDLK_UP:
                    pass



act = 0
game = True
i = 0
map = 0
room = Room(1, 1, 0, 0)

while game:
    clear_canvas()

    input_key_in_map()

    clear_canvas()
    room.draw()
    update_canvas()

close_canvas()
