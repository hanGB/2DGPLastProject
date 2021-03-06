from pico2d import *
import game_framework
import game_world
import initium_state
from background import Background
from location_bar import LocationBar
from dungeon_location import DungeonLocation

FIRST, APARTMENT_ONE, APARTMENT_TWO, TOWER, PYRAMID = range(5)

name = "city_state"

location_bar = None
background = None
key_information = None
dungeon_number = 0

dungeon_location = None
destination = -1


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def enter():
    global location_bar
    location_bar = LocationBar()
    game_world.add_object(location_bar, 1)

    global background
    background = Background()
    game_world.add_object(background, 0)

    global key_information

    if key_information is None:
        key_information = load_image("resource/interface/keyInformCity.png")

    global dungeon_location

    dungeon_location = [DungeonLocation(FIRST), DungeonLocation(APARTMENT_ONE), DungeonLocation(APARTMENT_TWO),
                        DungeonLocation(TOWER), DungeonLocation(PYRAMID)]

    location_bar.set_background(background, dungeon_number)
    background.set_center_object(location_bar)
    background.update()


def exit():
    global location_bar
    global background
    global key_information

    game_world.remove_object(location_bar)
    game_world.remove_object(background)

    del location_bar
    del background
    # del key_information


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
            if initium_state.city_dialogue_played:
                location_bar.handle_events(event)
            else:
                initium_state.city_dialogue.handle_events(event)


def update():
    global destination
    colliding = False

    if initium_state.city_dialogue_played:
        for dl in dungeon_location:
            if collide(dl, location_bar):
                location_bar.set_colliding(True)
                colliding = True
                destination = dl.get_type()
                break

        if not colliding:
            location_bar.set_colliding(False)
            destination = -1
    else:
        initium_state.city_dialogue.update()

    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
        key_information.draw(1150, 300)
    else:
        initium_state.city_dialogue.draw()
    update_canvas()
