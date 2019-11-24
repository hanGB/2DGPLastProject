from pico2d import *
import game_framework
import map_component
import battle_state
name = "map_state"

map = None


def enter():
    global map

    # test
    # game_framework.push_state(battle_state)
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
        # 배틀 진입 테스트
        # if event.type == SDL_KEYDOWN and event.key == SDLK_b:
        #    game_framework.push_state(battle_state)
        else:
            map.handle_events(event)


def update():
    map.update()


def draw():
    clear_canvas()
    map.draw()
    update_canvas()
