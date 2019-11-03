from pico2d import *
import battle_state
import battle_analyze_state
import sword_trigger_state
import contract_wait_escape_state
import game_framework

W_KEY, A_KEY, S_KEY, D_KEY, F_KEY, C_KEY, TAB_KEY, SHIFT_KEY, SPACE_KEY, \
UP_DOWN, DOWN_DOWN, UP_UP, DOWN_UP = range(13)

key_event_table = {
    (SDL_KEYDOWN, SDLK_w): W_KEY,
    (SDL_KEYDOWN, SDLK_a): A_KEY,
    (SDL_KEYDOWN, SDLK_s): S_KEY,
    (SDL_KEYDOWN, SDLK_d): D_KEY,
    (SDL_KEYDOWN, SDLK_f): F_KEY,
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

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(battle_ui):
        if battle_ui.selecting == 1:
            battle_ui.sub_counter += 1

            if battle_ui.sub_counter == 100:
                battle_ui.sub_counter = 0
                battle_ui.act = (battle_ui.act + 1) % 6
                if battle_ui.act == 0:
                    battle_ui.act = 1

    @staticmethod
    def draw(battle_ui):
        if battle_ui.is_main is True:
            battle_ui.main_ui.clip_draw(battle_ui.act * 300, 0, 300, 300, 270, 180)
        battle_ui.turn_number.clip_draw((battle_state.player.get_player(battle_ui.player).get_turn() - 1) * 100, 0
                                        , 100, 150, 105, 175)


class SkillState:
    skill_cnt = 0

    @staticmethod
    def enter(battle_ui, event):
        SkillState.skill_cnt = len(battle_state.player.get_player(battle_ui.player).get_card().getSkill())
        if event == DOWN_DOWN:
            battle_ui.selecting = 1
            battle_ui.skill_slt = (battle_ui.skill_slt + battle_ui.selecting) % SkillState.skill_cnt
            battle_ui.sub_counter = 0
        elif event == DOWN_UP or event == UP_UP:
            battle_ui.selecting = 0

        elif event == UP_DOWN:
            battle_ui.selecting = -1
            battle_ui.skill_slt = (battle_ui.skill_slt + battle_ui.selecting) % SkillState.skill_cnt
            battle_ui.sub_counter = 0

        elif event == TAB_KEY:
            game_framework.push_state(battle_analyze_state)

        elif event == SPACE_KEY:
            print("use skill")

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(battle_ui):
        if battle_ui.selecting == 1 or battle_ui.selecting == -1:
            battle_ui.sub_counter += 1

            if battle_ui.sub_counter == 80:
                battle_ui.sub_counter = 0
                battle_ui.skill_slt = (battle_ui.skill_slt + battle_ui.selecting) % SkillState.skill_cnt

    @staticmethod
    def draw(battle_ui):
        battle_ui.turn_number.clip_draw((battle_state.player.get_player(battle_ui.player).get_turn() - 1) * 100, 0
                                        , 100, 150, 105, 175)
        battle_ui.skill_ui.draw(150, 170)

        for i in range(len(battle_state.player.get_player(battle_ui.player).get_card().getSkill())):
            if battle_ui.skill_slt == i:
                battle_state.player.get_player(battle_ui.player).get_card().getSkill()[i].draw(i, 1)
            else:
                battle_state.player.get_player(battle_ui.player).get_card().getSkill()[i].draw(i, 0)


class ItemState:
    @staticmethod
    def enter(battle_ui, event):
        if event == DOWN_DOWN:
            battle_ui.selecting = 1
            battle_ui.item_slt = (battle_ui.item_slt + battle_ui.selecting) % 7
            battle_ui.sub_counter = 0
        elif event == DOWN_UP or event == UP_UP:
            battle_ui.selecting = 0

        elif event == UP_DOWN:
            battle_ui.selecting = -1
            battle_ui.item_slt = (battle_ui.item_slt + battle_ui.selecting) % 7
            battle_ui.sub_counter = 0

        elif event == SPACE_KEY:
            print("use item")

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(battle_ui):
        if battle_ui.selecting == 1 or battle_ui.selecting == -1:
            battle_ui.sub_counter += 1

            if battle_ui.sub_counter == 80:
                battle_ui.sub_counter = 0
                battle_ui.item_slt = (battle_ui.item_slt + battle_ui.selecting) % 7

    @staticmethod
    def draw(battle_ui):
        battle_ui.item_ui.draw(360, 220)
        battle_state.player.get_player(0).draw_item_number(battle_ui.item_slt)


next_state_table = {
    MainState: {DOWN_DOWN: MainState, DOWN_UP: MainState, UP_DOWN: MainState, UP_UP: MainState,
                W_KEY: SkillState, F_KEY: ItemState, A_KEY: MainState, S_KEY: MainState, D_KEY: MainState,
                C_KEY: MainState, TAB_KEY: MainState, SHIFT_KEY: MainState, SPACE_KEY: MainState},
    SkillState: {DOWN_DOWN: SkillState, DOWN_UP: SkillState, UP_DOWN: SkillState, UP_UP: SkillState,
                 W_KEY: MainState, F_KEY: SkillState, A_KEY: MainState, S_KEY: SkillState, D_KEY: SkillState,
                 C_KEY: SkillState, TAB_KEY: SkillState, SHIFT_KEY: MainState, SPACE_KEY: SkillState},
    ItemState: {DOWN_DOWN: ItemState, DOWN_UP: ItemState, UP_DOWN: ItemState, UP_UP: ItemState,
                W_KEY: ItemState, F_KEY: MainState, A_KEY: MainState, S_KEY: ItemState, D_KEY: ItemState,
                C_KEY: ItemState, TAB_KEY: MainState, SHIFT_KEY: MainState, SPACE_KEY: ItemState}
}


class BattleUi:
    main_ui = None
    turn_number = None
    skill_ui = None
    item_ui = None

    def __init__(self):
        if BattleUi.main_ui is None:
            BattleUi.main_ui = load_image("2newUi.png")
        if BattleUi.turn_number is None:
            BattleUi.turn_number = load_image("2turnNumber.png")

        if BattleUi.skill_ui is None:
            BattleUi.skill_ui = load_image("2skillUi.png")

        if BattleUi.item_ui is None:
            BattleUi.item_ui = load_image("2item.png")

        self.act = 0
        self.sd_key = -1
        self.player = 0
        self.item_slt = 0
        self.skill_slt = 0
        self.sub_counter = 0
        self.sub_menu_select = -1
        self.selecting = 0
        self.is_main = True
        self.event_que = []
        self.cur_state = MainState
        self.cur_state.enter(self, None)

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
