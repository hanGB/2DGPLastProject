from pico2d import *
import game_framework
import battle_state
import battle_analyze_state

name = "contract_wait_escape_state"

cwe_ui = None


class CWEUi:
    image_do = None
    image_act = None
    image_ny = None

    def __init__(self, key):
        if key == 2:
            self.key = 2
        elif key == 4:
            self.key = 1
        elif key == 5:
            self.key = 0

        if CWEUi.image_do is None:
            CWEUi.image_do = load_image("2doyouwant.png")

        if CWEUi.image_act is None:
            CWEUi.image_act = load_image("2etcAct.png")

        if CWEUi.image_ny is None:
            CWEUi.image_ny = load_image("2noyes.png")

    def getKey(self):
        return self.key

    def draw(self):
        CWEUi.image_do.draw(390, 180)
        CWEUi.image_act.clip_draw(0, self.key * 50, 300, 50, 410, 150)
        CWEUi.image_ny.draw(370, 90)


def enter():
    global cwe_ui

    cwe_ui = CWEUi(battle_state.battle_ui.get_act())


def exit():
    global cwe_ui

    del(cwe_ui)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.key == SDLK_SPACE and event.type == SDL_KEYDOWN:
            if cwe_ui.getKey() == 2:
                print("contract")

            elif cwe_ui.getKey() == 1:
                print("wait")

            elif cwe_ui.getKey() == 0:
                print("escape")

        elif (event.key == SDLK_a and event.type == SDL_KEYDOWN) \
                or (event.key == SDLK_LSHIFT and event.type == SDL_KEYDOWN):
            battle_state.battle_ui.set_is_main(True)
            game_framework.pop_state()

        elif event.key == SDLK_TAB and event.type == SDL_KEYDOWN:
            game_framework.push_state(battle_analyze_state)

        else:
            battle_state.battle_enemy.handle_events(event)


def update():
    battle_state.battle_enemy.update()


def draw():
    clear_canvas()

    battle_state.battle_map.draw()
    battle_state.battle_enemy.draw()
    battle_state.battle_ui.draw()
    battle_state.player.draw()
    cwe_ui.draw()


    update_canvas()
