from pico2d import *
import game_framework
import battle_state


name = "battle_item_state"

itemUi = None
item_slt = 0
player_slt = None


class ItemUi:
    image = None
    number = None

    def __init__(self):
        if ItemUi.image is None:
            ItemUi.image = load_image("2item.png")
        if ItemUi.number is None:
            ItemUi.number = load_image("2itemNum.png")

    def draw(self):
        ItemUi.image.draw(360, 220)
        battle_state.player[0].draw_item_number(item_slt)


def enter():
    global itemUi
    global player_slt

    player_slt = 0
    itemUi = ItemUi()


def exit():
    global itemUi
    global player_slt

    del(player_slt)
    del (itemUi)


def pause():
    pass


def resume():
    pass


def handle_events():
    global item_slt
    global player_slt

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_DOWN:
                item_slt = (item_slt + 1) % 7
            elif event.key == SDLK_UP:
                item_slt = (item_slt - 1) % 7
            elif event.key == SDLK_LEFT:
                player_slt = (player_slt - 1) % battle_state.player_cnt
            elif event.key == SDLK_RIGHT:
                player_slt = (player_slt + 1) % battle_state.player_cnt
            elif event.key == SDLK_a or event.key == SDLK_LSHIFT:
                game_framework.pop_state()

            elif event.key == SDLK_SPACE:
                pass


def update():
    battle_state.battle_ui.update()


def draw():
    clear_canvas()

    battle_state.battle_map.draw()
    if battle_state.enemy_cnt == 1:
        battle_state.battle_enemy[0].draw(2, 1)

    elif battle_state.enemy_cnt == 2:
        for n in range(battle_state.enemy_cnt):
            battle_state.battle_enemy[n].draw(2 * n + 0.5, 1)

    elif battle_state.enemy_cnt == 3:
        for n in range(battle_state.enemy_cnt):
            battle_state.battle_enemy[n].draw(n + n * 0.7, 1)

    elif battle_state.enemy_cnt == 4:
        for n in range(battle_state.enemy_cnt):
            battle_state.battle_enemy[n].draw(n + n * 0.2, 1)

    itemUi.draw()
    battle_state.player[0].draw_item_number(item_slt)
    for n in range(battle_state.player_cnt):
        battle_state.player[n].draw(n)
    update_canvas()
