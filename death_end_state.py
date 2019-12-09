from pico2d import *
import game_framework
import title_state

name = "death_end_state"

ending_screen = None


class DeathEnding:
    death_ending = None
    ending_bgm = None

    def __init__(self):
        if DeathEnding.death_ending is None:
            DeathEnding.death_ending = load_image("resource/title/deathEnding.png")

        if DeathEnding.ending_bgm is None:
            DeathEnding.ending_bgm = load_music("resource/sound/deathBGM.mp3")
            DeathEnding.ending_bgm.set_volume(40)

        DeathEnding.ending_bgm.repeat_play()

    def draw(self):
        self.death_ending .draw(640, 360)

    def stop_bgm(self):
        DeathEnding.ending_bgm.stop()


def enter():
    global ending_screen

    ending_screen = DeathEnding()


def exit():

    global ending_screen

    del ending_screen


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            ending_screen.stop_bgm()
            game_framework.change_state(title_state)


def update():
    pass


def draw():
    clear_canvas()
    ending_screen.draw()
    update_canvas()
