from pico2d import *
import game_framework
import room_data
import battle_component
import battle_enemy_controller
import battle_player
import game_world
import initium_state
import map_state
from skill_data import Skill

name = "battle_state"

player = None
battle_enemy = None
battle_ui = None
battle_map = None
now_turn = 0
sword_trigger = None
skill_processing = False
boss_battle = -1


def enter():
    global battle_ui
    global battle_map
    global battle_enemy
    global player
    global now_turn
    global sword_trigger

    sword_trigger = [Skill(91), Skill(90)]
    now_turn = 0
    player = battle_player.BattlePlayer(initium_state.player)

    for p in range(len(initium_state.player)):
        player.get_player(p).set_turn(player.get_player(p).get_max_turn())

    battle_map = room_data.Room(0, 0, 0, 0)
    battle_enemy = battle_enemy_controller.BattleEnemy()
    battle_ui = battle_component.BattleUi()

    game_world.add_object(battle_enemy, 1)
    game_world.add_object(player, 2)
    game_world.add_object(battle_ui, 2)


def exit():
    global sword_trigger

    del sword_trigger

    game_world.clear()


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
            if not skill_processing:
                battle_ui.handle_events(event)
                battle_enemy.handle_events(event)


def update():
    if battle_ui.get_escape():
        battle_ui.set_escape(False)
        game_framework.pop_state()

    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    battle_map.draw(map_state.map.get_type())
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
