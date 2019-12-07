from pico2d import *
import game_framework
import initium_state

TIME_PER_SELECTING = 1
SELECTING_PER_TIME = 1.0 / TIME_PER_SELECTING
FRAMES_PER_SELECTING = 2

name = "title_state"

title = None
menu = None
selecting_menu = None


class Title:
    def __init__(self):
        self.title = load_image("resource/title/title.png")
        self.menu = load_image("resource/title/mainMenu.png")

    def draw(self, menu):
        self.title.draw(640, 360)
        self.menu.clip_draw(menu * 640, 0, 640, 360, 960, 180)


def enter():
    global title
    global menu
    global selecting_menu
    # test
    # game_framework.change_state(initium_state)
    #

    title = Title()
    menu = 2
    selecting_menu = False


def exit():
    global title
    global menu
    global selecting_menu

    del title
    del menu
    del selecting_menu


def pause():
    pass


def resume():
    pass


def handle_events():
    global menu
    global selecting_menu

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if int(menu) == 2:
                menu = 1
            else:
                if event.key == SDLK_UP or event.key == SDLK_DOWN:
                    menu = (menu + 1) % 2
                    if not selecting_menu:
                        selecting_menu = True
                if event.key == SDLK_SPACE or event.key == SDLK_RETURN:
                    if int(menu) == 1:
                        game_framework.change_state(initium_state)
                    elif int(menu) == 0:
                        game_framework.quit()
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_UP or event.key == SDLK_DOWN:
                if selecting_menu:
                    selecting_menu = False
                    menu = int(menu)


def update():
    global menu

    if selecting_menu:
        menu = (menu + game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME) % 2


def draw():
    clear_canvas()
    title.draw(2 - int(menu))
    update_canvas()
