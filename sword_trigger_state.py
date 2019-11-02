from pico2d import *
import game_framework
import battle_state
import battle_analyze_state

name = "sword_trigger_state"

sword_trigger_ui = None


class SwordTriggerUi:
    image = None

    def __init__(self, key):
        self.key = key

        if SwordTriggerUi.image is None:
            SwordTriggerUi.image = load_image("2sdInBattle.png")

    def draw(self):
        SwordTriggerUi.image.clip_draw(0,  (2 - self.key) * 50, 250, 50, 300, 170)
        SwordTriggerUi.image.clip_draw(0, 0 * 50, 250, 50, 170, 80)


def enter():
    global sword_trigger_ui

    sword_trigger_ui = SwordTriggerUi(battle_state.sd_key_check)


def exit():
    global sword_trigger_ui

    del (sword_trigger_ui)


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
            elif event.key == SDLK_a or event.key == SDLK_LSHIFT:
                game_framework.pop_state()
            elif event.key == SDLK_TAB:
                game_framework.push_state(battle_analyze_state)


def update():
    battle_state.battle_ui.update()


def draw():
    clear_canvas()

    battle_state.battle_map.draw()

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
            battle_state.enemy[n].draw(n + n * 0.2, n - battle_state.enemy_slt)

    battle_state.battle_ui.draw(-1)
    sword_trigger_ui.draw()

    for n in range(battle_state.player_cnt):
        battle_state.player[n].draw(n)

    update_canvas()
