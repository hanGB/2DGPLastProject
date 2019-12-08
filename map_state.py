from pico2d import *
import game_framework
import map_component
import initium_state
import game_world
import battle_state
import city_state
name = "map_state"

map = None


def enter():
    global map

    # test
    # game_framework.push_state(battle_state)
    # game_framework.change_state(city_state)
    #

    map = map_component.Map(0)


def exit():
    global map

    # del map


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_PLUS:
            for player in initium_state.player:
                player.give_exp(1000)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_world.save()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
            initium_state.load_saved_world()
        else:
            map.handle_events(event)


def update():
    map.update()


def draw():
    clear_canvas()
    map.draw()
    update_canvas()
