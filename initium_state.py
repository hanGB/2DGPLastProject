import game_framework
import map_state
import random
import game_world
import city_state
from enemy_data import Enemy
from player_data import Player

BS, RS, BD, RD, BH, RH, BC, RC, ZERO = range(9)

name = "initium_state"

player = None
Lucifel = None
Lucifer = None
Alice = None

def enter():
    global player
    data = [BS, RD, RH, BC]
    chosenPlayer = []

    chosenPlayer.append(data[random.randint(0, 3)])
    data.remove(chosenPlayer[0])

    chosenPlayer.append(data[random.randint(0, 2)])

    player = [Player(ZERO, 100, 100, [10, 10, 10, 10, 10, 10]),
              Player(chosenPlayer[0], 100, 100, [10, 10, 10, 10, 10, 10]),
              Player(chosenPlayer[1], 100, 100, [10, 10, 10, 10, 10, 10])]

    for p in player:
        game_world.add_object(p, 2)

    global Alice
    global Lucifel
    global Lucifer

    Alice = Enemy(0)
    Lucifel = Enemy(12)
    Lucifer = Enemy(13)

    #game_framework.push_state(map_state)
    game_framework.push_state(city_state)


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
    player.clear()

    for o in game_world.all_objects():
        if isinstance(o, Player):
            game_world.remove_object(o)

    game_world.load()
    for o in game_world.all_objects():
        if isinstance(o, Player):
            player.append(o)
            if len(player) == 3:
                break