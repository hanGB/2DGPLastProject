from pico2d import *
import game_framework
import initium_state

name = "clear_end_state"

ending_screen = None


class ClearEnding:
    clear_ending = None
    ending_bgm = None

    def __init__(self):
        if ClearEnding.clear_ending is None:
            ClearEnding.clear_ending = [load_image("resource/title/clearEnding1.png"),
                                        load_image("resource/title/clearEnding2.png")]

        if ClearEnding.ending_bgm is None:
            ClearEnding.ending_bgm = load_wav("resource/sound/warningSound.wav")
            ClearEnding.ending_bgm.set_volume(30)

        ClearEnding.ending_bgm.play()
        self.part = 0
        self.timer = 0

    def draw(self):
        self.clear_ending[self.part].draw(640, 360)

    def update(self):
        delay(0.01)
        self.timer += 0.01

        if self.timer > 1.5:
            self.timer = 0
            if self.part == 0:
                self.part = 1
            else:
                game_framework.change_state(initium_state)

    def stop_bgm(self):
        ClearEnding.ending_bgm.stop()


def enter():
    global ending_screen

    ending_screen = ClearEnding()


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


def update():
    ending_screen.update()


def draw():
    clear_canvas()
    ending_screen.draw()
    update_canvas()
