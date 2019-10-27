from pico2d import *
import game_framework
import title_state

name = "warning_state"

warning = None
warning_time = 0.0

basic_dir = os.getcwd()
now_dir = os.path.join(basic_dir, "resource")
os.chdir(now_dir)


class Warning:
    def __init__(self):
        self.image = load_image("0warning.png")

    def draw(self):
        self.image.draw(640, 360)


def enter():
    global warning

    warning = Warning()


def exit():
    global warning

    del (warning)


def pause():
    pass


def resume():
    pass


def handle_events():
    global warning_time

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            warning_time = 0
            game_framework.change_state(title_state)


def update():
    global warning_time

    if warning_time > 3.0:
        warning_time = 0
        game_framework.change_state(title_state)

    delay(0.01)
    warning_time += 0.01


def draw():
    clear_canvas()
    warning.draw()
    update_canvas()
