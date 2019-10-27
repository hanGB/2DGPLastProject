from pico2d import *
import game_framework
import map_state

name = "title_state"

title = None
menu = None


class Title:
    def __init__(self):
        self.title = load_image("0title.png")
        self.menu = load_image("0mainMenu.png")

    def draw(self, menu):
        self.title.draw(640, 360)
        self.menu.clip_draw(menu * 640, 0, 640, 360, 960, 180)


def enter():
    global title
    global menu

    title = Title()
    menu = 0


def exit():
    global title
    global menu

    del (title)
    del (menu)


def pause():
    pass


def resume():
    pass


def handle_events():
    global menu

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if menu == 0:
                menu = 1
            elif menu == 1:
                if event.key == SDLK_UP or event.key == SDLK_DOWN:
                    menu = 2
                elif event.key == SDLK_SPACE or event.key == SDLK_RETURN:
                    game_framework.change_state(map_state)
            elif menu == 2:
                if event.key == SDLK_UP or event.key == SDLK_DOWN:
                    menu = 1
                elif event.key == SDLK_SPACE or event.key == SDLK_RETURN:
                    game_framework.quit()


def update():
    pass


def draw():
    clear_canvas()
    title.draw(menu)
    update_canvas()
