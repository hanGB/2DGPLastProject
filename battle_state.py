from pico2d import *
import game_framework
import map_state
import random
import math
import enemy_data
import player_data
import battle_component
import status

name = "battle_state"

player = None
player_cnt = None
enemy = None
battle_ui = None
battle_map = None
enemy_slt = None
enemy_cnt = None
sd_key_check = None
dir = None
sub_counter = None

LEFT_DOWN, RIGHT_DOWN, LEFT_UP, RIGHT_UP = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
}

def enter():
    global battle_ui
    global battle_map
    global enemy_slt
    global enemy
    global enemy_cnt
    global player
    global player_cnt
    global dir
    global sub_counter

    dir = 0
    sub_counter = 0
    player = [player_data.Player(0, 100, 100, [10, 10, 10, 10, 10]),
              player_data.Player(1, 100, 100, [10, 10, 10, 10, 10]),
              player_data.Player(3, 100, 100, [10, 10, 10, 10, 10])]

    player_cnt = len(player)

    enemy_cnt = random.randint(1, 4)
    enemy_slt = math.floor(enemy_cnt / 2)

    enemy = [enemy_data.Enemy(random.randint(1, 11)) for n in range(enemy_cnt)]

    battle_ui = battle_component.BattleUi()
    battle_map = map_state.Room(0, 0, 0, 0)
    enemy_slt = 0


def exit():
    global dir
    global sub_counter
    global battle_ui
    global battle_map
    global enemy_slt
    global enemy
    global enemy_cnt
    global player
    global player_cnt

    del (enemy)
    del (enemy_slt)
    del (enemy_cnt)
    del (battle_ui)
    del (battle_map)
    del (player)
    del (player_cnt)
    del (dir)
    del (sub_counter)

def pause():
    pass


def resume():
    pass


def handle_events():
    global act
    global enemy_slt
    global sd_key_check
    global dir
    global sub_counter

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        # 임시 배틀 종료 키 - 이동시 랜덤 전투 발생 구현시 삭제
        elif event.type == SDL_KEYDOWN and event.key == SDLK_b:
            game_framework.pop_state()

        elif (event.type, event.key) in key_event_table:
                key_event = key_event_table[event.type, event.key]
                if key_event == LEFT_DOWN:
                    dir = -1
                    sub_counter = 0
                    enemy_slt = (enemy_slt + dir) % enemy_cnt
                elif key_event == RIGHT_DOWN:
                    dir = 1
                    sub_counter = 0
                    enemy_slt = (enemy_slt + dir) % enemy_cnt
                elif key_event == LEFT_UP or key_event == RIGHT_UP:
                    dir = 0
        else:
            battle_ui.handle_events(event)


def update():
    global dir
    global sub_counter
    global enemy_slt

    if dir != 0:
        sub_counter += 1
        if sub_counter == 80:
            sub_counter = 0
            enemy_slt = (enemy_slt + dir) % enemy_cnt

    battle_ui.update()


def draw():
    clear_canvas()

    battle_map.draw()

    if enemy_cnt == 1:
        enemy[0].draw(2, 0)

    elif enemy_cnt == 2:
        for n in range(enemy_cnt):
            enemy[n].draw(2 * n + 0.5, n - enemy_slt)

    elif enemy_cnt == 3:
        for n in range(enemy_cnt):
            enemy[n].draw(n + n * 0.7, n - enemy_slt)

    elif enemy_cnt == 4:
        for n in range(enemy_cnt):
            enemy[n].draw(n + n * 0.2, n - enemy_slt)

    battle_ui.draw()

    for n in range(player_cnt):
        player[n].draw(n)

    update_canvas()
