from pico2d import *
import game_framework
import map_state
import batte_skill_state
import random
import math
import sword_trigger_state
import contract_wait_escape_state
import battle_analyze_state
import enemyData

name = "battle_state"


class BattleUi:
    def __init__(self):

        self.main_ui = load_image("2newUi.png")
        self.turn_number = load_image("2turnNumber.png")
       # self.heartbeat = load_image("2heartbeat.png")
        self.heartbeat_case = load_image("2heartbeatCase.png")
        self.beat = 0

    def update(self):
        # self.beat = (self.beat + 1) % 850
        pass

    def draw(self, act):
        if act != -1:
            self.main_ui.clip_draw(act * 300, 0, 300, 300, 270, 180)
        self.turn_number.clip_draw((5 - 1) * 100, 0, 100, 150, 105, 175)
        # self.heartbeat.clip_draw(self.beat, 0, 200, 60, 1100, 210)
        self.heartbeat_case.draw(1100, 210)


enemy = None
act = None
battleUi = None
battleMap = None
enemy_slt = None
enemy_cnt = None
sd_key_check = None


def enter():
    global battleUi
    global battleMap
    global act
    global enemy_slt
    global enemy
    global enemy_cnt

    enemy_cnt = random.randint(1, 4)
    enemy_slt = math.floor(enemy_cnt / 2)

    enemy = [enemyData.Enemy(random.randint(1, 11)) for n in range(enemy_cnt)]

    battleUi = BattleUi()
    battleMap = map_state.Room(0, 0, 0, 0)
    act = 0
    enemy_slt = 0


def exit():
    global battleUi
    global battleMap
    global act
    global enemy_slt
    global enemy
    global enemy_cnt

    del (enemy)
    del (enemy_slt)
    del (enemy_cnt)
    del (battleUi)
    del (battleMap)
    del (act)


def pause():
    pass


def resume():
    pass


def handle_events():
    global act
    global enemy_slt
    global sd_key_check

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            # 메뉴
            if event.key == SDLK_w:
                game_framework.push_state(batte_skill_state)
            elif event.key == SDLK_f:
                pass
            elif event.key == SDLK_DOWN:
                act = (act + 1) % 6
                if act == 0:
                    act = 1

            elif event.key == SDLK_LEFT:
                enemy_slt = (enemy_slt - 1) % enemy_cnt
            elif event.key == SDLK_RIGHT:
                enemy_slt = (enemy_slt + 1) % enemy_cnt

            elif event.key == SDLK_s:
                sd_key_check = 0
                game_framework.push_state(sword_trigger_state)
            elif event.key == SDLK_d:
                sd_key_check = 1
                game_framework.push_state(sword_trigger_state)
            elif event.key == SDLK_a or event.key == SDLK_LSHIFT:
                if act != 0:
                    act = 0
            elif event.key == SDLK_c:
                pass
            elif event.key == SDLK_SPACE:
                if act == 2 or act == 4 or act == 5:
                    game_framework.push_state(contract_wait_escape_state)
                elif act == 3:
                    sd_key_check = 1
                    game_framework.push_state(sword_trigger_state)
                elif act == 1:
                    game_framework.push_state(battle_analyze_state)
            elif event.key == SDLK_TAB:
                game_framework.push_state(battle_analyze_state)

            # 임시 배틀 종료 키
            elif event.key == SDLK_b:
                game_framework.pop_state()


def update():
    battleUi.update()


def draw():
    clear_canvas()

    battleMap.draw()

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

    battleUi.draw(act)
    update_canvas()
