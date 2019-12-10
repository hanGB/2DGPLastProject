from pico2d import *
import room_data
import random
import battle_state
import game_framework
import initium_state
import city_state
import map_state

TIME_PER_CAMERA_MOVE = 2
CAMERA_MOVE_PER_TIME = 1.0 / TIME_PER_CAMERA_MOVE
FRAMES_PER_CAMERA_MOVE = 8

TIME_PER_MOVE = 0.5
MOVE_PER_TIME = 1.0 / TIME_PER_MOVE
FRAMES_PER_MOVE = 4

LEFT_DOWN, RIGHT_DOWN, LEFT_UP, RIGHT_UP, UP_KEY, DOWN_KEY, MOVE, SPACE_KEY = range(8)

NON, CLOSED_BOX, OPENED_BOX, RECOVERY, WAY_OUT, BOSS = range(6)
FIRST, APARTMENT_ONE, TOWER, PYRAMID, APARTMENT_TWO = range(5)
N, E, S, W = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_q): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_e): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_q): LEFT_UP,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_e): RIGHT_UP,
    (SDL_KEYUP, SDLK_UP): UP_KEY,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_KEY,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_KEY
}


class NormalMap:
    @staticmethod
    def enter(map, event):
        if map.map_event[map.location_y][map.location_x][0] == WAY_OUT:
            if map.rain_sound.get_volume() == 0:
                map.rain_sound.set_volume(100)

        if event == LEFT_DOWN:
            map.direction = -1
            map.rooms[map.location_y][map.location_x].turn_sight('q')
            map.sub_counter = 0
        elif event == LEFT_UP or event == RIGHT_UP:
            map.direction = 0

        elif event == RIGHT_DOWN:
            map.direction = 1
            map.rooms[map.location_y][map.location_x].turn_sight('e')
            map.sub_counter = 0

        elif event == DOWN_KEY:
            map.rooms[map.location_y][map.location_x].turn_sight('s')

        elif event == UP_KEY:
            if map.rooms[map.location_y][map.location_x].is_door_in_front_player() is True:
                map.moving = True

        elif event == SPACE_KEY:
            now_direction = map.rooms[map.location_y][map.location_x].get_map_direction()
            if now_direction == map.map_event[map.location_y][map.location_x][1]:
                if map.map_event[map.location_y][map.location_x][0] == RECOVERY:
                    for p in initium_state.player:
                        p.set_Bd(p.get_max_Bd())
                        p.set_Md(p.get_max_Md())

                elif map.map_event[map.location_y][map.location_x][0] == CLOSED_BOX:
                    item_type = random.randint(0, 6)
                    number_of_item = random.randint(1, 5)
                    initium_state.player[0].set_item(item_type, number_of_item)
                    map.map_event[map.location_y][map.location_x] = (OPENED_BOX, now_direction)

        elif event == MOVE:
            now_direction = map.rooms[map.location_y][map.location_x].get_map_direction()
            if map.map_event[map.location_y][map.location_x][0] == WAY_OUT:
                if now_direction == map.map_event[map.location_y][map.location_x][1]:
                    map.rain_sound.set_volume(0)
                    city_state.dungeon_number = 0
                    map_state.clear_data[map.type] = True
                    game_framework.change_state(city_state)

            if not (map.map_event[map.location_y][map.location_x][0] == WAY_OUT and
                    now_direction == map.map_event[map.location_y][map.location_x][1]):
                if map.rain_sound.get_volume() != 0:
                    map.rain_sound.set_volume(0)

                if now_direction == 0:
                    map.location_y += 1
                elif now_direction == 2:
                    map.location_x += 1
                elif now_direction == 4:
                    map.location_y -= 1
                elif now_direction == 6:
                    map.location_x -= 1
                map.rooms[map.location_y][map.location_x].set_map_direction(now_direction)
                battle_outbreak_rate = random.randint(1, 20)
                if battle_outbreak_rate < 6:
                    map.bgm.stop()
                    game_framework.push_state(battle_state)

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(map):
        if map.direction == 1 or map.direction == -1:
            map.sub_counter += game_framework.frame_time * FRAMES_PER_CAMERA_MOVE * CAMERA_MOVE_PER_TIME

            if map.sub_counter > 1:
                map.sub_counter = 0

                if map.direction == 1:
                    map.rooms[map.location_y][map.location_x].turn_sight('e')
                elif map.direction == -1:
                    map.rooms[map.location_y][map.location_x].turn_sight('q')

        if map.moving:
            if map.animation_frame < 1:
                if not map.playing_step_sound:
                    map.step_sound.play()
                    map.playing_step_sound = True

            map.animation_counter += game_framework.frame_time * FRAMES_PER_MOVE * MOVE_PER_TIME
            if map.animation_counter > 1:
                map.animation_counter = 0
                map.animation_frame += 1

            if map.animation_frame == 4:
                map.playing_step_sound = False
                map.moving = False
                map.animation_frame = 0
                map.add_event(MOVE)

    @staticmethod
    def draw(map):
        map.rooms[map.location_y][map.location_x].draw(map.type)

        now_direction = map.rooms[map.location_y][map.location_x].get_map_direction()
        if now_direction == map.map_event[map.location_y][map.location_x][1]:
            if map.map_event[map.location_y][map.location_x][0] == RECOVERY:
                map.recovery_stone.draw(640, 200)
                map.space_bar.draw(640, 200)
            elif map.map_event[map.location_y][map.location_x][0] == CLOSED_BOX:
                map.box.clip_draw(0, 0, 350, 400, 640, 200)
                map.space_bar.draw(640, 200)
            elif map.map_event[map.location_y][map.location_x][0] == OPENED_BOX:
                map.box.clip_draw(350, 0, 350, 400, 640, 200)

        if map.moving:
            map.move_animation[map.type].clip_draw(map.animation_frame * 1280, 0, 1280, 720, 640, 360)

        map.compass.clip_draw(map.rooms[map.location_y][map.location_x].get_map_direction() * 200, 0,
                              200, 150, 1150, 100)
        if map.location_y < 10:
            map.room_number.clip_draw(20 * map.location_y, 0, 20, 30, 1210, 140)
        else:
            map.room_number.clip_draw(20 * (map.location_y % 10), 0, 20, 30, 1230, 140)
            map.room_number.clip_draw(20 * int(map.location_y / 10), 0, 20, 30, 1210, 140)

        if map.location_x < 10:
            map.room_number.clip_draw(20 * map.location_x, 0, 20, 30, 1100, 55)
        else:
            map.room_number.clip_draw(20 * (map.location_x % 10), 0, 20, 30, 1120, 55)
            map.room_number.clip_draw(20 * int(map.location_x / 10), 0, 20, 30, 1100, 55)

        map.key_information.draw(1150, 300)
        map.save_load_key.draw(1150, 400)

        sit = 0
        for player in initium_state.player:
            player.draw_bar_in_map(sit)
            sit += 1


next_state_table = {
    NormalMap: {LEFT_DOWN: NormalMap, RIGHT_DOWN: NormalMap,
                LEFT_UP: NormalMap, RIGHT_UP: NormalMap,
                UP_KEY: NormalMap, DOWN_KEY: NormalMap,
                MOVE: NormalMap, SPACE_KEY: NormalMap}
}


class Map:
    compass = None
    room_number = None
    move_animation = None
    key_information = None
    save_load_key = None
    step_sound = None
    box = None
    recovery_stone = None
    rain_sound = None
    space_bar = None

    def __init__(self, type):
        if Map.rain_sound is None:
            Map.rain_sound = load_wav("resource/sound/moreRainSound.wav")
            Map.rain_sound.set_volume(0)

        Map.rain_sound.repeat_play()

        if Map.space_bar is None:
            Map.space_bar = load_image("resource/interface/spaceBig.png")

        if Map.box is None:
            Map.box = load_image('resource/map/box.png')

        if Map.recovery_stone is None:
            Map.recovery_stone = load_image('resource/map/recoveryStone.png')

        if Map.save_load_key is None:
            Map.save_load_key = load_image("resource/interface/keyInformSave.png")
        if Map.key_information is None:
            Map.key_information = load_image("resource/interface/keyInformMap.png")
        if Map.compass is None:
            Map.compass = load_image("resource/interface/compass.png")
        if Map.room_number is None:
            Map.room_number = load_image("resource/interface/roomNum.png")
        if Map.move_animation is None:
            Map.move_animation = [load_image("resource/animation/moveAni.png"),
                                  load_image("resource/animation/apartmoveAni.png"),
                                  load_image("resource/animation/towermoveAni.png"),
                                  load_image("resource/animation/pyramidmoveAni.png")]
        if Map.step_sound is None:
            Map.step_sound = load_wav("resource/sound/stepSound.wav")
            Map.step_sound.set_volume(120)

        self.direction = 0
        self.sub_counter = 0
        self.animation_counter = 0
        self.animation_frame = 0
        self.moving = False
        self.playing_step_sound = False
        self.sound_playing = False
        self.rain_sound_playing = False
        self.type = type

        if type == FIRST:
            self.bgm = load_music("resource/sound/firstDungeonBGM.mp3")
            self.bgm.set_volume(30)
            # 0번 던전의 맵 데이터
            # 0, 4 S에서 출발해서 6, 2 N으로 나가는 던전
            self.rooms = [[room_data.Room(1, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 1, 1, 0), room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 1, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(1, 0, 0, 1), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(1, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 1, 1, 0), room_data.Room(1, 0, 0, 1), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 1, 1, 0), room_data.Room(1, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(1, 0, 0, 1), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 1, 1, 0), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 1, 1), room_data.Room(0, 0, 0, 1)]]

            if map_state.clear_data[type]:
                self.location_y = 6
                self.location_x = 1
                self.direction = 4
            else:
                self.location_y = 0
                self.location_x = 4

            self.map_event = [[(RECOVERY, 4), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(CLOSED_BOX, 6), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (CLOSED_BOX, 2), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (CLOSED_BOX, 4), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(NON, 0), (WAY_OUT, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (RECOVERY, 2)]]

        elif type == APARTMENT_ONE:
            self.bgm = load_music("resource/sound/apartDungeonBGM.mp3")
            self.bgm.set_volume(30)

            self.rooms = [[room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],
                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],
                          [room_data.Room(0, 1, 0, 0), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 0, 0, 1)],
                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],
                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],
                          [room_data.Room(0, 1, 0, 0), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 0, 0, 1)],
                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],
                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],
                          [room_data.Room(0, 1, 0, 0), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 0, 0, 1)],
                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],
                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)]]

            if map_state.clear_data[type]:
                self.location_y = 0
                self.location_x = 8
            else:
                self.location_y = 0
                self.location_x = 8

            self.map_event = [[(NON, 0), (NON, 0), (RECOVERY, 0),
                               (NON, 0), (NON, 0), (CLOSED_BOX, 0),
                               (NON, 0), (NON, 0), (WAY_OUT, 4),
                               (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(CLOSED_BOX, 6), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (CLOSED_BOX, 2)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(CLOSED_BOX, 6), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (CLOSED_BOX, 2)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(CLOSED_BOX, 6), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (CLOSED_BOX, 2)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (WAY_OUT, 0),
                               (NON, 0), (NON, 0), (CLOSED_BOX, 0),
                               (NON, 0), (NON, 0), (RECOVERY, 0),
                               (NON, 0), (NON, 0)]]

        elif type == PYRAMID:
            self.bgm = load_music("resource/sound/pyramidDungeonBGM.mp3")
            self.bgm.set_volume(30)

            self.rooms = [[room_data.Room(0, 1, 0, 0), room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(1, 0, 0, 1)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0)],

                          [room_data.Room(1, 1, 0, 0), room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(1, 0, 0, 1), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0)],

                          [room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0)],

                          [room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 1, 0, 0),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 0, 0, 1), room_data.Room(0, 0, 0, 0),
                           room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0)],

                          [room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0)],

                          [room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 1, 1, 0),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 0, 1, 1), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0)],

                          [room_data.Room(1, 0, 1, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0)],

                          [room_data.Room(0, 1, 1, 0), room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 1, 0, 1), room_data.Room(0, 0, 1, 1)]]

            if map_state.clear_data[type]:
                self.location_y = 0
                self.location_x = 0
            else:
                self.location_y = 0
                self.location_x = 0

            self.map_event = [[(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (CLOSED_BOX, 2)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(RECOVERY, 4), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (RECOVERY, 4),
                               (NON, 0), (BOSS, 2), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (CLOSED_BOX, 0), (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0)],

                              [(CLOSED_BOX, 6), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0), (RECOVERY, 0)]]

        elif type == TOWER:
            self.bgm = load_music("resource/sound/towerDungeonBGM.mp3")
            self.bgm.set_volume(30)

            self.rooms = [[room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 0, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 1, 0, 0), room_data.Room(0, 1, 0, 1), room_data.Room(1, 1, 1, 1),
                           room_data.Room(0, 1, 0, 1), room_data.Room(0, 0, 0, 1)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(1, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)],

                          [room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 1, 0),
                           room_data.Room(0, 0, 0, 0), room_data.Room(0, 0, 0, 0)]]

            if map_state.clear_data[type]:
                self.location_y = 0
                self.location_x = 2
            else:
                self.location_y = 0
                self.location_x = 2

            self.map_event = [[(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (NON, 0),
                               (NON, 0), (NON, 0)],

                              [(CLOSED_BOX, 6), (NON, 0), (NON, 0),
                               (NON, 0), (CLOSED_BOX, 2)],

                              [(NON, 0), (NON, 0), (RECOVERY, 0),
                               (NON, 0), (NON, 0)],

                              [(NON, 0), (NON, 0), (BOSS, 0),
                               (NON, 0), (NON, 0)]]

        self.event_que = []
        self.cur_state = NormalMap
        self.cur_state.enter(self, None)

    def get_type(self):
        return self.type

    def start_bgm(self):
        self.bgm.repeat_play()

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def is_playing(self):
        return self.sound_playing

    def set_sound_playing_true(self):
        self.sound_playing = True

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def handle_events(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[event.type, event.key]
            self.add_event(key_event)
