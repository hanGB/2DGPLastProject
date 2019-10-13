from pico2d import *
import os

open_canvas(1280, 720)

# 기본 디렉토리 저장
basic_dir = os.getcwd()

# 리소스가 있는 디렉토리 저장 및 이동
now_dir = os.path.join(basic_dir, "resource/map")
os.chdir(now_dir)

background_map = [load_image('colormap.png'), load_image('colormapdia.png')]
door = [load_image('frontdoor.png'), load_image('leftdoor.png'), load_image('rightdoor.png'),
        load_image('dialeftdoor.png'), load_image('diarightdoor.png')]
now_dir = os.path.join(basic_dir, "resource/enemy")
os.chdir(now_dir)
enemy = load_image('testdemon.png')

now_dir = os.path.join(basic_dir, "resource/ui")
os.chdir(now_dir)

ui = load_image('ui.png')
ui2 = load_image('ui2.png')
uiAct = load_image('uiAct.png')
uiBack = load_image('uiBackground.png')


def show_ui():
    global act

    uiBack.draw(640, 125)
    ui.clip_draw(0, 0, 250, 100, 160, 190)
    ui.clip_draw(250, 0, 230, 100, 153, 120)
    ui2.clip_draw(0, 0, 250, 100, 460, 192)
    ui2.clip_draw(250, 0, 230, 100, 454, 52)
    ui2.clip_draw(500, 0, 230, 100, 454, 122)
    uiAct.clip_draw(300 * act, 0, 300, 100, 190, 58)


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

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_q:
                map = (map - 1) % 8
            elif event.key == SDLK_e:
                map = (map + 1) % 8


act = 0
game = True
i = 0
map = 0
door_location = [(0, 2, -1, -1), (3, 4, -1, -1), (1, 0, -1, -1), (-1, 3, -1, -1),
                 (-1, 1, -1, -1), (-1, -1, -1, -1), (2, -1, -1, -1), (4, -1, -1, -1)]

while game:
    clear_canvas()
    background_map[map % 2].draw(640, 360)
    for i in range(0, 4):
        if door_location[map][i] != -1:
            door[door_location[map][i]].draw(640, 360)
    # show_ui()
    input_key_in_map()
    # enemy.clip_draw(0 + 86 * i, 0, 85, 100, 640, 460)
    # i = (i + 1) % 2
    update_canvas()

close_canvas()
