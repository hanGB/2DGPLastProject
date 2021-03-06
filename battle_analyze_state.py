from pico2d import *
import game_framework
import battle_state
import game_world
import map_state

name = "battle_analyze_state"

analyze_ui = None


class AnalyzeUi:
    image = None

    def __init__(self):
        if AnalyzeUi.image is None:
            AnalyzeUi.image = load_image("resource/interface/analyzeUi.png")
        md = battle_state.player.get_player(battle_state.battle_ui.player_now).get_Md() - 1

        if md != 0:
            battle_state.player.get_player(battle_state.battle_ui.player_now).set_Md(md)

    def update(self):
        pass

    def draw(self):
        AnalyzeUi.image.draw(200, 100)
        battle_state.battle_enemy.enemy[battle_state.battle_enemy.get_selected_enemy_number()].draw_attribute_data()
        battle_state.battle_ui.battle_explain.draw(645, 15)


def enter():
    global analyze_ui

    analyze_ui = AnalyzeUi()
    game_world.add_object(analyze_ui, 2)


def exit():
    global analyze_ui
    game_world.remove_object(analyze_ui)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif (event.key == SDLK_a and event.type == SDL_KEYDOWN)\
                or (event.key == SDLK_LSHIFT and event.type == SDL_KEYDOWN)\
                or (event.key == SDLK_TAB and event.type == SDL_KEYDOWN):
            game_framework.pop_state()

        else:
            battle_state.battle_enemy.handle_events(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    battle_state.battle_map.draw(map_state.map.get_type())
    battle_state.battle_enemy.draw()
    analyze_ui.draw()
    update_canvas()
