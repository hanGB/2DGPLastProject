from pico2d import *
import game_framework
import battle_state


name = "contract_wait_escape_state"

cwe_ui = None


class CWEUi:
    image = None

    def __init__(self, key):
        if key == 2:
            self.key = 2
        elif key == 4:
            self.key = 1
        elif key == 5:
            self.key = 0

        if CWEUi.image is None:
            CWEUi.image = load_image("2etcUi.png")

    def draw(self):
        CWEUi.image.clip_draw(0, 90, 300, 30, 300, 170)
        CWEUi.image.clip_draw(0, self.key * 30, 300, 30, 300, 80)


def enter():
    global cwe_ui

    cwe_ui = CWEUi(battle_state.act)


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
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                battle_state.enemy_slt = (battle_state.enemy_slt - 1) % battle_state.enemy_cnt
            elif event.key == SDLK_RIGHT:
                battle_state.enemy_slt = (battle_state.enemy_slt + 1) % battle_state.enemy_cnt
            elif event.key == SDLK_SPACE:
                if battle_state.act == 0:
                    pass
                elif battle_state.act == 0:
                    pass
                elif battle_state.act == 0:
                    pass

            elif event.key == SDLK_a or event.key == SDLK_LSHIFT:
                game_framework.pop_state()


def update():
    battle_state.battleUi.update()


def draw():
    clear_canvas()

    battle_state.battleMap.draw()

    if battle_state.enemy_cnt == 1:
        battle_state.enemy[0].draw(2, 0)

    elif battle_state.enemy_cnt == 2:
        for n in range(battle_state.enemy_cnt):
            battle_state.enemy[n].draw(2 * n + 0.5, n - battle_state.enemy_slt)

    elif battle_state.enemy_cnt == 3:
        for n in range(battle_state.enemy_cnt):
            battle_state.enemy[n].draw(n + n * 0.7, n - battle_state.enemy_slt)

    elif battle_state.enemy_cnt == 4:
        for n in range(battle_state.enemy_cnt):
            battle_state.enemy[n].draw(n+ n * 0.2, n - battle_state.enemy_slt)

    battle_state.battleUi.draw(-1)
    cwe_ui.draw()

    update_canvas()
