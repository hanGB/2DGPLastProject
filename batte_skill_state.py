from pico2d import *
import game_framework
import battle_state
import battle_analyze_state

import status

name = "battle_skill_state"

skill = None
skill_cnt = None
skill_slt = None
skill_ui = None


class SkillUi:
    image = None

    def __init__(self):

        if SkillUi.image is None:
            SkillUi.image = load_image("2skillUi.png")

    def draw(self):
        SkillUi.image.draw(150, 170)



def enter():
    global skill_ui

    skill_ui = SkillUi()


def exit():


def pause():
    pass


def resume():
    pass


def handle_events():
    global skill_slt

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_DOWN:
                skill_slt = (skill_slt + 1) % skill_cnt
            elif event.key == SDLK_UP:
                skill_slt = (skill_slt - 1) % skill_cnt
            elif event.key == SDLK_LEFT:
                battle_state.enemy_slt = (battle_state.enemy_slt - 1) % battle_state.enemy_cnt
            elif event.key == SDLK_RIGHT:
                battle_state.enemy_slt = (battle_state.enemy_slt + 1) % battle_state.enemy_cnt
            elif event.key == SDLK_a or event.key == SDLK_LSHIFT:
                game_framework.pop_state()

            elif event.key == SDLK_SPACE:
                pass
            elif event.key == SDLK_TAB:
               game_framework.push_state(battle_analyze_state)


def update():
    battle_state.battle_ui.update()


def draw():
    clear_canvas()

    battle_state.battle_map.draw()
    battle_state.battle_ui.draw(-1)
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


    for n in range(battle_state.player_cnt):
        battle_state.player[n].draw(n)
    update_canvas()
