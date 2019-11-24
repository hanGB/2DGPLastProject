import game_framework
import map_state

from player_data import Player

name = "initium_state"

player = None


def enter():
    global player

    player = [Player(8, 100, 100, [10, 10, 10, 10, 10, 10]),
              Player(0, 100, 100, [10, 10, 10, 10, 10, 10]),
              Player(5, 100, 100, [10, 10, 10, 10, 10, 10])]

    game_framework.push_state(map_state)


def exit():
    global player

    del player


def pause():
    pass


def resume():
    pass


def handle_events():
   pass


def update():
    pass


def draw():
    pass
