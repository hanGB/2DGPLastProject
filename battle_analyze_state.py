from pico2d import *
import game_framework
import battle_state
import battle_component

name = "battle_analyze_state"

analyze_ui = None


class AnalyzeUi:
    image = None

    def __init__(self):
        if AnalyzeUi.image is None:
            AnalyzeUi.image = load_image("2analyzeUi.png")

    def draw(self, enemy):
        AnalyzeUi.image.draw(200, 100)
        battle_state.battle_enemy[battle_state.enemy_slt].draw_attribute_data()


def enter():
    global analyze_ui

    analyze_ui = AnalyzeUi()


def exit():
    global analyze_ui

    del (analyze_ui)


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
            elif event.key == SDLK_a or event.key == SDLK_LSHIFT or event.key == SDLK_TAB:
                game_framework.pop_state()


def update():
    battle_state.battle_ui.update()


def draw():
    clear_canvas()

    battle_state.battle_map.draw()

    if battle_state.enemy_cnt == 1:
        battle_state.battle_enemy[0].draw(2, 0)

    elif battle_state.enemy_cnt == 2:
        for n in range(battle_state.enemy_cnt):
            battle_state.battle_enemy[n].draw(2 * n + 0.5, n - battle_state.enemy_slt)

    elif battle_state.enemy_cnt == 3:
        for n in range(battle_state.enemy_cnt):
            battle_state.battle_enemy[n].draw(n + n * 0.7, n - battle_state.enemy_slt)

    elif battle_state.enemy_cnt == 4:
        for n in range(battle_state.enemy_cnt):
            battle_state.battle_enemy[n].draw(n + n * 0.2, n - battle_state.enemy_slt)
    analyze_ui.draw(battle_state.battle_enemy[battle_state.enemy_slt])

    update_canvas()
