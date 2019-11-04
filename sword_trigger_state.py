from pico2d import *
import game_framework
import battle_state
import battle_analyze_state
import game_world

name = "sword_trigger_state"

sword_trigger_ui = None


class SwordTriggerUi:
    image = None

    def __init__(self, key):
        self.key = key

        if SwordTriggerUi.image is None:
            SwordTriggerUi.image = load_image("resource/interface/sdInBattle.png")

    def getKey(self):
        return self.key

    def update(self):
        pass

    def draw(self):
        SwordTriggerUi.image.clip_draw(0,  (2 - self.key) * 50, 250, 50, 300, 170)
        SwordTriggerUi.image.clip_draw(0, 0 * 50, 250, 50, 170, 80)


def enter():
    global sword_trigger_ui

    sword_trigger_ui = SwordTriggerUi(battle_state.battle_ui.get_sd_key())
    game_world.add_object(sword_trigger_ui, 2)


def exit():
    global sword_trigger_ui
    game_world.remove_object(sword_trigger_ui)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        elif event.key == SDLK_s and event.type == SDL_KEYDOWN:
            if sword_trigger_ui.getKey() == 0:
                print("sword")

        elif event.key == SDLK_d and event.type == SDL_KEYDOWN:
            if sword_trigger_ui.getKey() == 1:
                print("trigger")

        elif event.key == (SDLK_a and event.type == SDL_KEYDOWN) \
                or (event.key == SDLK_LSHIFT and event.type == SDL_KEYDOWN):
            battle_state.battle_ui.set_is_main(True)
            game_framework.pop_state()

        elif event.key == SDLK_TAB and event.type == SDL_KEYDOWN:
            game_framework.push_state(battle_analyze_state)

        else:
            battle_state.battle_enemy.handle_events(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
