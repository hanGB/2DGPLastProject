import random

from pico2d import *
import city_state
import game_framework
PIXEL_PER_METER = (10.0 / 0.5)
FALL_SPEED_KMPH = 20.0  # Km / Hour
FALL_SPEED_MPM = (FALL_SPEED_KMPH * 5000.0 / 60.0)
FALL_SPEED_MPS = (FALL_SPEED_MPM / 60.0)
FALL_SPEED_PPS = (FALL_SPEED_MPS * PIXEL_PER_METER)


class Background:
    image = None
    rain = None
    bgm = None
    rain_sound = None

    def __init__(self):
        if Background.image is None:
            Background.image = load_image('resource/map/infinityCityMap.png')
        if Background.rain is None:
            Background.rain = load_image('resource/map/rain.png')

        if Background.bgm is None:
            Background.bgm = load_music("resource/sound/cityBGM.mp3")
            Background.bgm.set_volume(40)

        if Background.rain_sound is None:
            Background.rain_sound = load_wav("resource/sound/moreRainSound.wav")
            Background.rain_sound.set_volume(80)

        Background.bgm.repeat_play()
        Background.rain_sound.repeat_play()

        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.w = self.image.w
        self.h = self.image.h

    def set_center_object(self, location_bar):
        self.center_object = location_bar

        self.rain_x = self.center_object.x
        self.rain_y = self.center_object.y

    def draw(self):
        self.image.clip_draw_to_origin(self.q3l, self.q3b, self.q3w, self.q3h, 0, 0)                        # quadrant 3
        self.image.clip_draw_to_origin(self.q2l, self.q2b, self.q2w, self.q2h, 0, self.q3h)                 # quadrant 2
        self.image.clip_draw_to_origin(self.q4l, self.q4b, self.q4w, self.q4h, self.q3w, 0)                 # quadrant 4
        self.image.clip_draw_to_origin(self.q1l, self.q1b, self.q1w, self.q1h, self.q3w, self.q3h)          # quadrant 4

        self.rain.clip_draw_to_origin(self.q3lr, self.q3br, self.q3wr, self.q3hr, 0, 0)  # quadrant 3
        self.rain.clip_draw_to_origin(self.q2lr, self.q2br, self.q2wr, self.q2hr, 0, self.q3hr)  # quadrant 2
        self.rain.clip_draw_to_origin(self.q4lr, self.q4br, self.q4wr, self.q4hr, self.q3wr, 0)  # quadrant 4
        self.rain.clip_draw_to_origin(self.q1lr, self.q1br, self.q1wr, self.q1hr, self.q3wr, self.q3hr)  # quadrant 4

    def update(self):
        # quadrant 3
        self.q3l = (int(self.center_object.x) - self.canvas_width // 2) % self.w
        self.q3b = (int(self.center_object.y) - self.canvas_height // 2) % self.h
        self.q3w = clamp(0, self.w - self.q3l, self.w)
        self.q3h = clamp(0, self.h - self.q3b, self.h)
        # quadrant 2
        self.q2l = self.q3l
        self.q2b = 0
        self.q2w = self.q3w
        self.q2h = self.canvas_height - self.q3h
        # quadrant 4
        self.q4l = 0
        self.q4b = self.q3b
        self.q4w = self.canvas_width - self.q3w
        self.q4h = self.q3h
        # quadrant 1
        self.q1l = 0
        self.q1b = 0
        self.q1w = self.q4w
        self.q1h = self.q2h


        # rain
        location = city_state.location_bar.get_location()

        if location == 0:
            self.rain_x += FALL_SPEED_PPS * game_framework.frame_time
            self.rain_y += 2 * FALL_SPEED_PPS * game_framework.frame_time
        elif location == 1:
            self.rain_x -= FALL_SPEED_PPS * game_framework.frame_time
            self.rain_y += 2 * FALL_SPEED_PPS * game_framework.frame_time
        elif location == 2:
            self.rain_x += FALL_SPEED_PPS * game_framework.frame_time
            self.rain_y -= 2 * FALL_SPEED_PPS * game_framework.frame_time
        elif location == 3:
            self.rain_x -= FALL_SPEED_PPS * game_framework.frame_time
            self.rain_y -= 2 * FALL_SPEED_PPS * game_framework.frame_time

        # quadrant 3
        self.q3lr = (int(self.rain_x) - self.canvas_width // 2) % self.w
        self.q3br = (int(self.rain_y) - self.canvas_height // 2) % self.h
        self.q3wr = clamp(0, self.w - self.q3lr, self.w)
        self.q3hr = clamp(0, self.h - self.q3br, self.h)
        # quadrant 2
        self.q2lr = self.q3lr
        self.q2br = 0
        self.q2wr = self.q3wr
        self.q2hr = self.canvas_height - self.q3hr
        # quadrant 4
        self.q4lr = 0
        self.q4br = self.q3br
        self.q4wr = self.canvas_width - self.q3wr
        self.q4hr = self.q3hr
        # quadrant 1
        self.q1lr = 0
        self.q1br = 0
        self.q1wr = self.q4wr
        self.q1hr = self.q2hr

    def handle_event(self, event):
        pass





