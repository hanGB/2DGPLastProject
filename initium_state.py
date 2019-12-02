import game_framework
import map_state
import random
import game_world
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

    for p in player:
        game_world.add_object(p, 2)

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


def load_saved_world():
    global player
    player = []

    game_world.load()
    for o in game_world.all_objects():
        if isinstance(o, Player):
            player.append(o)
            if len(player) == 3:
                break