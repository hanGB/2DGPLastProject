from pico2d import *
import game_framework
from dialogue_component import Dialogue

ALICE, LUCIFEL, LUCIFER = range(3)

name = "battle_state"
boss = LUCIFEL

dialogue = None

def enter():
    global dialogue

    dialogue = Dialogue(boss)

def exit():


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            dialogue.handle_events(event)



def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    battle_map.draw(map_state.map.get_type())
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
