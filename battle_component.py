from pico2d import *
import battle_state
import battle_analyze_state
import sword_trigger_state
import contract_wait_escape_state
import game_framework
from damage_calculator import can_use_skill
from auto_battle import Auto, Manual
import game_world

TIME_PER_SELECTING = 2
SELECTING_PER_TIME = 1.0 / TIME_PER_SELECTING
FRAMES_PER_SELECTING = 8

W_KEY, A_KEY, S_KEY, D_KEY, F_KEY, X_KEY, C_KEY, TAB_KEY, SHIFT_KEY, SPACE_KEY, \
UP_DOWN, DOWN_DOWN, UP_UP, DOWN_UP = range(14)

key_event_table = {
    (SDL_KEYDOWN, SDLK_w): W_KEY,
    (SDL_KEYDOWN, SDLK_a): A_KEY,
    (SDL_KEYDOWN, SDLK_s): S_KEY,
    (SDL_KEYDOWN, SDLK_d): D_KEY,
    (SDL_KEYDOWN, SDLK_f): F_KEY,
    (SDL_KEYDOWN, SDLK_x): X_KEY,
    (SDL_KEYDOWN, SDLK_c): C_KEY,
    (SDL_KEYDOWN, SDLK_TAB): TAB_KEY,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_KEY,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_KEY,
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP
}


class MainState:
    @staticmethod
    def enter(battle_ui, event):
        battle_ui.is_main = True
        if event == DOWN_DOWN:
            battle_ui.selecting = 1
            battle_ui.act = (battle_ui.act + 1) % 6
            if battle_ui.act == 0:
                battle_ui.act = 1
            battle_ui.sub_counter = 0

        elif event == DOWN_UP:
            if battle_ui.selecting == 1:
                battle_ui.selecting = 0

        elif event == UP_DOWN:
            battle_ui.act = 0
            battle_ui.selecting = 0

        elif event == SPACE_KEY:
            if battle_ui.act != 0:
                if battle_ui.act == 1:
                    game_framework.push_state(battle_analyze_state)
                elif battle_ui.act == 3:
                    battle_ui.sd_key = 1
                    battle_ui.is_main = False
                    game_framework.push_state(sword_trigger_state)
                else:
                    battle_ui.is_main = False
                    game_framework.push_state(contract_wait_escape_state)

        elif event == S_KEY or event == D_KEY:
            if event == S_KEY:
                battle_ui.sd_key = 0
            else:
                battle_ui.sd_key = 1
            battle_ui.is_main = False
            game_framework.push_state(sword_trigger_state)

        elif event == A_KEY or event == SHIFT_KEY:
            if battle_ui.act != 0:
                battle_ui.act = 0

        elif event == TAB_KEY:
            game_framework.push_state(battle_analyze_state)

        elif event == X_KEY:
            for p in range(battle_state.player.number_of_players):
                battle_ui.player_now = (battle_ui.player_now + 1) % battle_state.player.number_of_players
                if battle_state.player.get_player(battle_ui.player_now).get_turn() != 0:
                    if battle_state.player.get_player(battle_ui.player_now).get_Bd() > 0:
                        break

        elif event == C_KEY:
            battle_ui.play_processor \
                = Auto(battle_state.player.get_player(battle_state.battle_ui.player_now), battle_state.battle_enemy)
            game_world.add_object(battle_ui.play_processor, 3)
            battle_ui.process_end = False

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(battle_ui):
        down_level = battle_state.player.get_player(battle_ui.get_player_now()).get_down_level()
        if down_level != 0:
            turn = battle_state.player.get_player(battle_ui.player_now).get_turn() - down_level
            if turn < 0:
                turn = 0
            battle_state.player.get_player(battle_ui.player_now).set_turn(turn)

        if battle_ui.process_end:
            if battle_ui.play_processor is not None:
                game_world.remove_object(battle_ui.play_processor)
                battle_ui.play_processor = None

        if battle_state.now_turn == 0:
            player_now = battle_ui.get_player_now()
            check_player = player_now

            if battle_state.player.get_player(player_now).get_turn() == 0:
                for p in range(battle_state.player.number_of_players):
                    battle_ui.player_now = (battle_ui.player_now + 1) % battle_state.player.number_of_players
                    if battle_state.player.get_player(battle_ui.player_now).get_turn() != 0:
                        if battle_state.player.get_player(battle_ui.player_now).get_Bd() > 0:
                            break
                if check_player == battle_ui.player_now:
                    battle_state.now_turn = 1
                    for p in range(battle_state.player.get_number_of()):
                        battle_state.player.get_player(p).set_turn(battle_state.player.get_player(p).get_max_turn())

        if battle_ui.selecting == 1:
            battle_ui.sub_counter += game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME

            if battle_ui.sub_counter > 1:
                battle_ui.sub_counter = 0
                battle_ui.act = (battle_ui.act + 1) % 6
                if battle_ui.act == 0:
                    battle_ui.act = 1

    @staticmethod
    def draw(battle_ui):
        if battle_ui.is_main is True:
            battle_ui.main_ui.clip_draw(battle_ui.act * 300, 0, 300, 300, 270, 180)
        battle_ui.turn_number.clip_draw((battle_state.player.get_player(battle_ui.player_now).get_turn()) * 100, 0
                                        , 100, 150, 105, 175)
        battle_ui.player_sign.draw(1250, 200 - battle_ui.player_now * 50)
        battle_ui.battle_explain.draw(645, 15)


class SkillState:
    number_of_skills = 0

    @staticmethod
    def enter(battle_ui, event):
        SkillState.number_of_skills = len(battle_state.player.get_player(battle_ui.player_now).get_card().get_skill())
        if event == DOWN_DOWN:
            battle_ui.selecting = 1
            battle_ui.selected_skill = (battle_ui.selected_skill + battle_ui.selecting) % SkillState.number_of_skills
            battle_ui.sub_counter = 0
        elif event == DOWN_UP or event == UP_UP:
            battle_ui.selecting = 0

        elif event == UP_DOWN:
            battle_ui.selecting = -1
            battle_ui.selected_skill = (battle_ui.selected_skill + battle_ui.selecting) % SkillState.number_of_skills
            battle_ui.sub_counter = 0

        elif event == TAB_KEY:
            game_framework.push_state(battle_analyze_state)

        elif event == SPACE_KEY:
            if (can_use_skill(battle_state.player.get_player(battle_state.battle_ui.player_now),
                              battle_state.player.get_player(battle_ui.player_now).
                              get_card().get_skill()[battle_ui.selected_skill])):

                battle_ui.play_processor \
                    = Manual(battle_state.player.get_player(battle_state.battle_ui.player_now),
                             battle_state.battle_enemy.get_selected_enemy(),
                             battle_state.player.get_player(battle_ui.player_now).
                             get_card().get_skill()[battle_ui.selected_skill])

                game_world.add_object(battle_ui.play_processor, 3)
                battle_ui.process_end = False

        elif event == X_KEY:
            battle_ui.player_target = (battle_ui.player_target + 1) % battle_state.player.number_of_players

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(battle_ui):
        if battle_ui.process_end:
            if battle_ui.play_processor is not None:
                game_world.remove_object(battle_ui.play_processor)
                battle_ui.play_processor = None

        if battle_state.player.get_player(battle_ui.player_now).get_turn() == 0:
            battle_ui.add_event(SHIFT_KEY)

        if battle_state.player.get_player(battle_ui.get_player_now()).get_down_level() != 0:
            battle_ui.add_event(SHIFT_KEY)

        if battle_ui.selecting == 1 or battle_ui.selecting == -1:
            battle_ui.sub_counter += game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME

            if battle_ui.sub_counter > 1:
                battle_ui.sub_counter = 0
                battle_ui.selected_skill = (battle_ui.selected_skill + battle_ui.selecting) \
                                           % SkillState.number_of_skills

    @staticmethod
    def draw(battle_ui):
        battle_ui.turn_number.clip_draw((battle_state.player.get_player(battle_ui.player_now).get_turn()) * 100, 0
                                        , 100, 150, 105, 175)
        battle_ui.skill_ui.draw(150, 170)
        battle_ui.player_sign.draw(1250, 200 - battle_ui.player_target * 50)

        for i in range(len(battle_state.player.get_player(battle_ui.player_now).get_card().get_skill())):
            if battle_ui.selected_skill == i:
                battle_state.player.get_player(battle_ui.player_now).get_card().get_skill()[i].draw(i, 1)
            else:
                battle_state.player.get_player(battle_ui.player_now).get_card().get_skill()[i].draw(i, 0)
        battle_ui.battle_explain.draw(645, 15)


class ItemState:
    @staticmethod
    def enter(battle_ui, event):
        if event == DOWN_DOWN:
            battle_ui.selecting = 1
            battle_ui.selected_item = (battle_ui.selected_item + battle_ui.selecting) % 7
            battle_ui.sub_counter = 0
        elif event == DOWN_UP or event == UP_UP:
            battle_ui.selecting = 0

        elif event == UP_DOWN:
            battle_ui.selecting = -1
            battle_ui.selected_item = (battle_ui.selected_item + battle_ui.selecting) % 7
            battle_ui.sub_counter = 0

        elif event == SPACE_KEY:
            print("use item")

        elif event == X_KEY:
            battle_ui.player_target = (battle_ui.player_target + 1) % battle_state.player.number_of_players

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(battle_ui):
        if battle_state.player.get_player(battle_ui.player_now).get_turn() == 0:
            battle_ui.add_event(SHIFT_KEY)

        if battle_ui.selecting == 1 or battle_ui.selecting == -1:
            battle_ui.sub_counter += game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME

            if battle_ui.sub_counter > 1:
                battle_ui.sub_counter = 0
                battle_ui.selected_item = (battle_ui.selected_item + battle_ui.selecting) % 7

    @staticmethod
    def draw(battle_ui):
        battle_ui.item_ui.draw(360, 220)
        battle_state.player.get_player(0).draw_item_number(battle_ui.selected_item)
        battle_ui.player_sign.draw(1250, 200 - battle_ui.player_target * 50)
        battle_ui.battle_explain.draw(645, 15)


next_state_table = {
    MainState: {DOWN_DOWN: MainState, DOWN_UP: MainState, UP_DOWN: MainState, UP_UP: MainState,
                W_KEY: SkillState, F_KEY: ItemState, A_KEY: MainState, S_KEY: MainState, D_KEY: MainState,
                X_KEY: MainState, C_KEY: MainState, TAB_KEY: MainState, SHIFT_KEY: MainState, SPACE_KEY: MainState},
    SkillState: {DOWN_DOWN: SkillState, DOWN_UP: SkillState, UP_DOWN: SkillState, UP_UP: SkillState,
                 W_KEY: MainState, F_KEY: SkillState, A_KEY: MainState, S_KEY: SkillState, D_KEY: SkillState,
                 X_KEY: SkillState, C_KEY: SkillState, TAB_KEY: SkillState, SHIFT_KEY: MainState, SPACE_KEY: SkillState},
    ItemState: {DOWN_DOWN: ItemState, DOWN_UP: ItemState, UP_DOWN: ItemState, UP_UP: ItemState,
                W_KEY: ItemState, F_KEY: MainState, A_KEY: MainState, S_KEY: ItemState, D_KEY: ItemState,
                X_KEY: ItemState, C_KEY: ItemState, TAB_KEY: MainState, SHIFT_KEY: MainState, SPACE_KEY: ItemState}
}


class BattleUi:
    main_ui = None
    turn_number = None
    skill_ui = None
    item_ui = None
    player_sign = None
    battle_explain = None

    def __init__(self):
        if BattleUi.main_ui is None:
            BattleUi.main_ui = load_image("resource/interface/newUi.png")
        if BattleUi.turn_number is None:
            BattleUi.turn_number = load_image("resource/interface/turnNumber.png")

        if BattleUi.skill_ui is None:
            BattleUi.skill_ui = load_image("resource/interface/skillUi.png")

        if BattleUi.item_ui is None:
            BattleUi.item_ui = load_image("resource/interface/item.png")

        if BattleUi.player_sign is None:
            BattleUi.player_sign = load_image("resource/interface/playerSign.png")

        if BattleUi.battle_explain is None:
            BattleUi.battle_explain = load_image("resource/interface/battleExplain.png")

        self.act = 0
        self.sd_key = -1
        self.player_now = 0
        self.selected_item = 0
        self.selected_skill = 0
        self.sub_counter = 0
        self.sub_menu_select = -1
        self.selecting = 0
        self.player_target = 0
        self.is_main = True
        self.event_que = []
        self.cur_state = MainState
        self.cur_state.enter(self, None)
        self.escape = False
        self.play_processor = None

        self.process_end = False

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def get_act(self):
        return self.act

    def get_sd_key(self):
        return self.sd_key

    def set_is_main(self, tf):
        self.is_main = tf

    def set_escape(self, tf):
        self.escape = tf

    def get_escape(self):
        return self.escape

    def get_player_now(self):
        return self.player_now

    def set_process_end(self, t):
        self.process_end = t

    def get_process_end(self):
        return self.process_end

    def get_play_processor(self):
        return self.play_processor

    def set_play_processor(self, pp):
        self.play_processor = pp

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
