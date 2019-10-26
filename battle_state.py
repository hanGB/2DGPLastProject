from pico2d import *

import game_framework
import map_state

name = "battle_state"

basic_dir = os.getcwd()


class BattleUi:
    def __init__(self):
        global now_dir

        now_dir = os.path.join(basic_dir, "resource/ui")
        os.chdir(now_dir)

        self.main_ui = load_image("newUi.png")
        self.turn_number = load_image("turnNumber.png")
        self.heartbeat = load_image("heartbeat.png")
        self.heartbeat_case = load_image("heartbeatCase.png")
        self.beat = 0

    def update(self):
        self.beat = (self.beat + 1) % 850

    def draw(self, menu, act):
        if menu == 0:
            self.main_ui.clip_draw(act * 300, 0, 300, 300, 270, 180)
            self.turn_number.clip_draw((5 - 1) * 100, 0, 100, 150, 105, 175)
            self.heartbeat.clip_draw(self.beat, 0, 200, 60, 1100, 210)
            self.heartbeat_case.draw(1100, 210)


act = None
battleUi = None
battleMap = None


def enter():
    global battleUi
    global battleMap
    global act

    battleUi = BattleUi()
    battleMap = map_state.Room(0, 0, 0, 0)
    act = 0


def exit():
    global battleUi
    global battleMap
    global act

    del (battleUi)
    del (battleMap)
    del (act)


def pause():
    pass


def resume():
    pass


def handle_events():
    global act

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
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

            # 임시 배틀 종료 키
            elif event.key == SDLK_b:
                game_framework.pop_state()


def update():
    battleUi.update()


def draw():
    clear_canvas()

    battleMap.draw()
    battleUi.draw(0, act)

    update_canvas()
