from pico2d import *
import game_framework
import battle_state

# test
import status

name = "battle_skill_state"

skill = None
skill_cnt = None
skill_slt = None
skillUi = None


class SkillUi:
    image = None

    def __init__(self):

        if SkillUi.image is None:
            SkillUi.image = load_image("2skillUi.png")

    def draw(self):
        SkillUi.image.draw(150, 170)


def enter():
    global skill_slt
    global skillUi
    global skill
    global skill_cnt

    skill_cnt = 5
    skill = [status.Skill(0, 0, 1, 0, 50, 90),
             status.Skill(12, 0, 3, 0, 350, 90),
             status.Skill(81, 0, 2, 0, 150, 90),
             status.Skill(53, 0, 2, 0, 150, 90),
             status.Skill(43, 0, 2, 0, 150, 90)]

    skill_slt = 0
    skillUi = SkillUi()


def exit():
    global skill_slt
    global skillUi
    global skill
    global skill_cnt

    del (skill_slt)
    del (skillUi)
    del (skill)
    del (skill_cnt)


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
            if event.key == SDLK_UP:
                skill_slt = (skill_slt - 1) % skill_cnt
            elif event.key == SDLK_LEFT:
                battle_state.enemy_slt = (battle_state.enemy_slt - 1) % 5
            elif event.key == SDLK_RIGHT:
                battle_state.enemy_slt = (battle_state.enemy_slt + 1) % 5
            elif event.key == SDLK_a or event.key == SDLK_LSHIFT or event.key == SDLK_w:
                game_framework.pop_state()

            elif event.key == SDLK_SPACE:
                pass
            elif event.key == SDLK_TAB:
               # game_framework.push_state(battle_analyze_state)
                pass


def update():
    battle_state.battleUi.update()


def draw():
    clear_canvas()

    battle_state.battleMap.draw()
    battle_state.battleUi.draw(-1)
    skillUi.draw()

    for i in range(skill_cnt):
        if skill_slt == i:
            skill[i].draw(i, 1)
        else:
            skill[i].draw(i, 0)
    update_canvas()
