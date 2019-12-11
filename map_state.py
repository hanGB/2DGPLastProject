from pico2d import *
import game_framework
import map_component
import initium_state
import game_world
import battle_state
import city_state
name = "map_state"

map = None
destination = 0
clear_data = [False, False, False, False, False]


def enter():
    global map

    # test
    # game_framework.push_state(battle_state)
    # game_framework.change_state(city_state)
    #

    map = map_component.Map(destination)


def exit():
    global map

    del map


def pause():
    pass


def resume():
    map.start_bgm()


def handle_events():
    events = get_events()

    for event in events:
        if initium_state.first_dialogue_played:
            if event.type == SDL_QUIT:
                game_framework.quit()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_KP_PLUS:
                for player in initium_state.player:
                    player.give_exp(10000)
            elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
                game_world.save()
            elif event.type == SDL_KEYDOWN and event.key == SDLK_l:
                initium_state.load_saved_world()
            else:
                map.handle_events(event)
        else:
            if event.type == SDL_QUIT:
                game_framework.quit()
            else:
                initium_state.first_dialogue.handle_events(event)


def update():
    if not map.is_playing():
        map.start_bgm()
        map.set_sound_playing_true()

    if initium_state.first_dialogue_played:
        map.update()
    else:
        initium_state.first_dialogue.update()


def draw():
    clear_canvas()
    map.draw()
    if not initium_state.first_dialogue_played:
        initium_state.first_dialogue.draw()

    update_canvas()
