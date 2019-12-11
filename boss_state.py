from pico2d import *
import game_framework
import game_world
import map_state
import initium_state
from dialogue_component import Dialogue
from room_data import Room
import clear_end_state

ALICE, LUCIFEL, LUCIFER, FIRST, CITY, LUCIFEL_TWO = range(6)

name = "boss_state"
boss = LUCIFEL

dialogue = None
battle_map = None
last_boss = 0


def enter():
    global dialogue

    dialogue = Dialogue(boss)

    game_world.add_object(dialogue, 2)

    global battle_map
    battle_map = Room(0, 0, 0, 0)


def exit():
    global dialogue
    global battle_map

    game_world.remove_object(dialogue)
    del dialogue
    del battle_map


def pause():
    global boss

    if boss == LUCIFEL:
        boss = LUCIFEL_TWO


def resume():
    if boss == LUCIFER:
        game_framework.change_state(clear_end_state)

    else:
        global dialogue

        game_world.remove_object(dialogue)

        dialogue = Dialogue(boss)
        game_world.add_object(dialogue, 2)


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
    if boss == ALICE:
        initium_state.Alice.draw_in_map()
    elif boss == LUCIFEL:
        initium_state.Lucifel.draw_in_map()
    elif boss == LUCIFER:
        initium_state.Lucifer.draw_in_map()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
