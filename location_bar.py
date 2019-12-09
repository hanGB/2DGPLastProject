import game_framework
from pico2d import *
import city_state
import map_state

PIXEL_PER_METER = (10.0 / 0.3)
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

RIGHT_DOWN, LEFT_DOWN, UP_DOWN, DOWN_DOWN, RIGHT_UP, LEFT_UP, UP_UP, DOWN_UP, SPACE = range(9)

FIRST, APARTMENT_ONE, APARTMENT_TWO, TOWER, PYRAMID = range(5)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


class MovingState:

    @staticmethod
    def enter(location_bar, event):
        if event == RIGHT_DOWN:
            location_bar.x_velocity += RUN_SPEED_PPS
        elif event == RIGHT_UP:
            location_bar.x_velocity -= RUN_SPEED_PPS
        if event == LEFT_DOWN:
            location_bar.x_velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            location_bar.x_velocity += RUN_SPEED_PPS

        if event == UP_DOWN:
            location_bar.y_velocity += RUN_SPEED_PPS
        elif event == UP_UP:
            location_bar.y_velocity -= RUN_SPEED_PPS
        if event == DOWN_DOWN:
            location_bar.y_velocity -= RUN_SPEED_PPS
        elif event == DOWN_UP:
            location_bar.y_velocity += RUN_SPEED_PPS

        if event == SPACE:
            map_state.destination = city_state.destination
            game_framework.change_state(map_state)


    @staticmethod
    def exit(location_bar, event):
        pass

    @staticmethod
    def do(location_bar):
        location_bar.x += location_bar.x_velocity * game_framework.frame_time
        location_bar.y += location_bar.y_velocity * game_framework.frame_time

        location_bar.x %= 3840
        location_bar.y %= 2160

        if 1920 > location_bar.x > 0 and 1080 > location_bar.y > 0:
            location_bar.location = 2

        elif 1920 > location_bar.x > 0 and 2160 > location_bar.y > 1080:
            location_bar.location = 1

        elif 3840 > location_bar.x > 1920 and 1080 > location_bar.y > 0:
            location_bar.location = 3

        elif 3840 > location_bar.x > 1920 and 2160 > location_bar.y > 1080:
            location_bar.location = 0

    @staticmethod
    def draw(location_bar):
        cx, cy = location_bar.canvas_width // 2, location_bar.canvas_height // 2

        location_bar.image.clip_draw(45 * location_bar.location, 0, 45, 60, cx, cy)

        if location_bar.colliding:
            if location_bar.location == 0:
                location_bar.space_image.draw(cx - 35, cy + 5)

            elif location_bar.location == 1:
                location_bar.space_image.draw(cx + 35, cy + 5)

            elif location_bar.location == 2:
                location_bar.space_image.draw(cx - 35, cy)

            elif location_bar.location == 3:
                location_bar.space_image.draw(cx + 35, cy)


next_state_table = {
    MovingState: {RIGHT_UP: MovingState, LEFT_UP: MovingState, RIGHT_DOWN: MovingState, LEFT_DOWN: MovingState,
                  UP_UP: MovingState, UP_DOWN: MovingState, DOWN_UP: MovingState, DOWN_DOWN: MovingState,
                  SPACE: MovingState}
}


class LocationBar:
    image = None
    space_image = None

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()

        if LocationBar.image is None:
            LocationBar.image = load_image("resource/map/locationBar.png")
        if LocationBar.space_image is None:
            LocationBar.space_image = load_image("resource/interface/space.png")

        self.dir = 1
        self.x_velocity, self.y_velocity = 0, 0
        self.location = 1
        self.colliding = False
        self.event_que = []
        self.cur_state = MovingState
        self.cur_state.enter(self, None)

    def set_colliding(self, tf):
        self.colliding = tf

    def get_location(self):
        return self.location

    def set_background(self, bg, dungeon):
        self.bg = bg

        x1, y1, x2, y2 = city_state.dungeon_location[dungeon].get_bb()

        self.x = (x1 + x2) / 2
        self.y = (y1 + y2) / 2

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def get_location(self):
        return self.location

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def get_bb(self):
        x = self.x % 3840
        y = self.y % 2160
        return x - 30, y - 30, x + 30, y + 30
