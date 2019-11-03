from pico2d import *
import game_framework
import map_state
import player_data
import battle_component
import battle_enemy_controller
import battle_player
import game_world

name = "battle_state"

player = None
battle_enemy = None
battle_ui = None
battle_map = None


def enter():
    global battle_ui
    global battle_map
    global battle_enemy
    global player

# 테스트 용, 플레이어 생성은 게임 시작할 때 할 것
    test_player = [player_data.Player(0, 100, 100, [10, 10, 10, 10, 10]),
                   player_data.Player(1, 100, 100, [10, 10, 10, 10, 10]),
                   player_data.Player(3, 100, 100, [10, 10, 10, 10, 10])]

    player = battle_player.BattlePlayer(test_player)

    battle_map = map_state.Room(0, 0, 0, 0)
    battle_enemy = battle_enemy_controller.BattleEnemy()
    battle_ui = battle_component.BattleUi()

    game_world.add_object(battle_map, 0)
    game_world.add_object(battle_enemy, 1)
    game_world.add_object(player, 2)
    game_world.add_object(battle_ui, 2)


def exit():
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

        # 임시 배틀 종료 키 - 이동시 랜덤 전투 발생 구현시 삭제
        elif event.type == SDL_KEYDOWN and event.key == SDLK_b:
            game_framework.pop_state()
        else:
            battle_ui.handle_events(event)
            battle_enemy.handle_events(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
