import game_framework
import player_data
import map_state

name = "initium_state"

player = None


def enter():
    global player

    player = [player_data.Player(0, 100, 100, [10, 10, 10, 10, 10]),
              player_data.Player(1, 100, 100, [10, 10, 10, 10, 10]),
              player_data.Player(3, 100, 100, [10, 10, 10, 10, 10])]

    game_framework.push_state(map_state)


def exit():
    global player

    del (player)


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
