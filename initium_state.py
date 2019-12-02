import game_framework
import map_state
import random
from player_data import Player


name = "initium_state"

player = None


def enter():
    global player
    data = [0, 3, 5, 6]
    chosenPlayer = []

    chosenPlayer.append(data[random.randint(0, 3)])
    data.remove(chosenPlayer[0])

    chosenPlayer.append(data[random.randint(0, 2)])

    player = [Player(8, 100, 100, [10, 10, 10, 10, 10, 10]),
              Player(chosenPlayer[0], 100, 100, [10, 10, 10, 10, 10, 10]),
              Player(chosenPlayer[1], 100, 100, [10, 10, 10, 10, 10, 10])]

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
