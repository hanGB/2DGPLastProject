from pico2d import *
import game_framework
import game_world
from background import Background
from location_bar import LocationBar

name = "MainState"

location_bar = None
background = None


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

    background.set_center_object(location_bar)
    location_bar.set_background(background)


def exit():
    global location_bar
    global background

    game_world.remove_object(location_bar)
    game_world.remove_object(background)
    del location_bar
    del background


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
            location_bar.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()






