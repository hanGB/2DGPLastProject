from pico2d import *
import battle_state
import battle_analyze_state
import sword_trigger_state
import contract_wait_escape_state
import game_framework
from damage_calculator import can_use_skill, use_skill
from behavior_tree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
from item_data import use_item


SKILL_FRAMES = 4
ANIMATION_ACCELERATION = 2.5

TIME_PER_SELECTING = 2
SELECTING_PER_TIME = 1.0 / TIME_PER_SELECTING
FRAMES_PER_SELECTING = 8

W_KEY, A_KEY, S_KEY, D_KEY, F_KEY, X_KEY, C_KEY, TAB_KEY, SHIFT_KEY, SPACE_KEY, \
UP_DOWN, DOWN_DOWN, UP_UP, DOWN_UP = range(14)
ALICE, LUCIFEL, LUCIFER = range(3)

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
            battle_ui.player_target = (battle_ui.player_target + 1) % battle_state.player.number_of_players

        elif event == C_KEY:
            battle_ui.auto_play = True
            battle_ui.process_end = False

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(battle_ui):
        if battle_state.now_turn == 0:
            player = battle_state.player.get_player(battle_ui.player_now)
            down_level = player.get_down_level()
            if down_level > 0:
                if down_level == 3:
                    if player.get_turn() > 4:
                        player.set_turn(player.get_turn() - 4)
                    else:
                        player.set_turn(0)
                else:
                    if player.get_turn() > down_level:
                        player.set_turn(player.get_turn() - down_level)
                    else:
                        player.set_turn(0)
                player.set_down_level(0)

            check_player = battle_ui.player_now

            if battle_state.now_turn == 0:
                if battle_state.player.get_player(battle_ui.player_now).get_Bd() <= 0:
                    for p in range(battle_state.player.number_of_players):
                        battle_ui.player_now = (battle_ui.player_now + 1) % battle_state.player.number_of_players
                        if battle_state.player.get_player(battle_ui.player_now).get_Bd() > 0:
                            break

            if battle_state.player.get_player(battle_ui.player_now).get_turn() == 0:
                for p in range(battle_state.player.number_of_players):
                    battle_ui.player_now = (battle_ui.player_now + 1) % battle_state.player.number_of_players
                    if battle_state.player.get_player(battle_ui.player_now).get_turn() != 0:
                        if battle_state.player.get_player(battle_ui.player_now).get_Bd() > 0:
                            break

                if check_player == battle_ui.player_now:
                    battle_state.now_turn = 1

                    for p in range(battle_state.player.get_number_of()):
                        battle_state.player.get_player(p).set_turn(battle_state.player.get_player(p).get_max_turn())

                    battle_ui.player_now = (battle_ui.player_now + 1) % battle_state.player.number_of_players

        if battle_ui.selecting == 1:
            battle_ui.sub_counter += game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME

            if battle_ui.sub_counter > 1:
                battle_ui.sub_counter = 0
                battle_ui.act = (battle_ui.act + 1) % 6
                if battle_ui.act == 0:
                    battle_ui.act = 1

    @staticmethod
    def draw(battle_ui):
        if battle_state.now_turn == 0:
            if battle_ui.is_main is True:
                battle_ui.main_ui.clip_draw(battle_ui.act * 300, 0, 300, 300, 270, 180)
            battle_ui.turn_number.clip_draw((battle_state.player.get_player(battle_ui.player_now).get_turn()) * 100, 0
                                            , 100, 150, 105, 175)
            battle_ui.now_player_mark.draw(880, 200 - battle_ui.player_now * 50)
            battle_ui.player_sign.draw(1250, 200 - battle_ui.player_target * 50)
            battle_ui.battle_explain.draw(645, 15)


class SkillState:
    number_of_skills = 0

    @staticmethod
    def enter(battle_ui, event):
        SkillState.number_of_skills = len(battle_state.player.get_player(battle_ui.player_now).get_skill())
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
                              get_skill()[battle_ui.selected_skill])):

                battle_ui.user = battle_state.player.get_player(battle_ui.player_now)
                battle_ui.selected_skill_data = \
                    battle_state.player.get_player(battle_ui.player_now) \
                    .get_skill()[battle_ui.selected_skill]

                if battle_ui.selected_skill_data.get_ally_target():
                    players = battle_state.player.get_list()
                    battle_ui.selected_target = players[battle_ui.player_target]
                else:
                    battle_ui.selected_target = battle_state.battle_enemy.get_selected_enemy()

                battle_ui.manual_play = True
                battle_ui.process_end = False

        elif event == X_KEY:
            battle_ui.player_target = (battle_ui.player_target + 1) % battle_state.player.number_of_players

    @staticmethod
    def exit(battle_ui, event):
        pass

    @staticmethod
    def do(battle_ui):
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
        battle_ui.now_player_mark.draw(880, 200 - battle_ui.player_now * 50)
        battle_ui.player_sign.draw(1250, 200 - battle_ui.player_target * 50)

        for i in range(len(battle_state.player.get_player(battle_ui.player_now).get_skill())):
            if battle_ui.selected_skill == i:
                battle_state.player.get_player(battle_ui.player_now).get_skill()[i].draw(i, 1)
            else:
                battle_state.player.get_player(battle_ui.player_now).get_skill()[i].draw(i, 0)
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
            players = battle_state.player.get_list()
            use_item(players[battle_ui.player_target], battle_ui.selected_item)

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
        battle_ui.now_player_mark.draw(880, 200 - battle_ui.player_now * 50)
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
    now_player_mark = None
    battle_explain = None

    def __init__(self):

        if battle_state.boss_battle == ALICE:
            self.bgm = load_music("resource/sound/aliceBGM.mp3")
        elif battle_state.boss_battle == LUCIFEL:
            self.bgm = load_music("resource/sound/lucifelBGM.mp3")
        elif battle_state.boss_battle == LUCIFER:
            self.bgm = load_music("resource/sound/luciferBGM.mp3")
        else:
            self.bgm = load_music("resource/sound/battleBGM.mp3")

        self.bgm.set_volume(20)

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

        if BattleUi.now_player_mark is None:
            BattleUi.now_player_mark = load_image("resource/interface/playerNow.png")

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

        self.user = battle_state.player.get_list()[self.player_now]
        self.targets = battle_state.battle_enemy.get_list()

        self.selected_skill_data = None
        self.selected_target = None

        self.sword_trigger = battle_state.sword_trigger

        self.showing_skill_name = False
        self.time_of_showing_skill = 0
        self.showing_skill_animation = False
        self.skill_frame = 0

        self.auto_play = False
        self.manual_play = False

        self.bgm.repeat_play()

        self.build_behavior_tree()

    def check_auto_play(self):
        if self.auto_play:
            battle_state.skill_processing = True
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.FAIL

    def check_manual_play(self):
        if self.manual_play:
            battle_state.skill_processing = True
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.FAIL

    def select_skill(self):
        self.user = battle_state.player.get_list()[self.player_now]

        skills = self.user.get_skill()
        usable_skills = []

        for skill in skills:
            if skill.get_Md() <= self.user.get_Md() and skill.get_turn() <= self.user.get_turn():
                usable_skills.append(skill)

        number_of_skills = len(usable_skills)

        if self.user.get_turn() >= 1:
            if self.user.get_Md() >= 1:
                skill_select_list = number_of_skills + 2
            else:
                skill_select_list = number_of_skills + 1
        else:
            battle_state.skill_processing = False
            return BehaviorTree.FAIL

        if skill_select_list == 1:
            index_of_selected_skill = 1
        else:
            index_of_selected_skill = random.randint(0, skill_select_list - 1)

        if index_of_selected_skill - number_of_skills == 0:
            self.selected_skill_data = self.sword_trigger[0]

        elif index_of_selected_skill - number_of_skills == 1:
            self.selected_skill_data = self.sword_trigger[1]

        else:
            self.selected_skill_data = usable_skills[index_of_selected_skill]

        return BehaviorTree.SUCCESS

    def select_target(self):
        ally_target = self.selected_skill_data.get_ally_target()
        if ally_target:
            self.targets = battle_state.player.get_list()
        else:
            self.targets = battle_state.battle_enemy.get_list()

        usable_targets = []

        for target in self.targets:
            if target.get_Bd() > 0:
                usable_targets.append(target)

        number_of_targets = len(usable_targets)
        if number_of_targets == 1:
            self.selected_target = usable_targets[0]
        elif number_of_targets == 0:
            battle_state.skill_processing = False
            return BehaviorTree.FAIL
        else:
            index_of_selected_target = random.randint(0, number_of_targets - 1)
            self.selected_target = usable_targets[index_of_selected_target]

        return BehaviorTree.SUCCESS

    def show_skill_name(self):
        self.showing_skill_name = True
        self.time_of_showing_skill += game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME

        if self.time_of_showing_skill > 2:
            self.time_of_showing_skill = 0
            self.showing_skill_name = False
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def skill_animation(self):
        self.showing_skill_animation = True
        self.skill_frame += game_framework.frame_time * FRAMES_PER_SELECTING \
                            * SELECTING_PER_TIME * ANIMATION_ACCELERATION

        if self.skill_frame > SKILL_FRAMES:
            self.skill_frame = 0
            self.showing_skill_animation = False
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def use_skill(self):
        use_skill(self.user, self.selected_target, self.selected_skill_data)

        battle_state.skill_processing = False
        self.auto_play = False
        self.manual_play = False
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        check_auto_play_node = LeafNode("Check Auto Play", self.check_auto_play)
        check_manual_play_node = LeafNode("Check Manual Play", self.check_manual_play)

        select_skill_node = LeafNode("Select Skill", self.select_skill)
        select_target_node = LeafNode("Select Target", self.select_target)
        show_skill_name_node = LeafNode("Show Skill Name", self.show_skill_name)
        skill_animation_node = LeafNode("Skill Animation", self.skill_animation)
        use_skill_node = LeafNode("Use Skill", self.use_skill)

        process_skill_node = SelectorNode("Process Skill")

        auto_node = SequenceNode("Auto")
        manual_node = SequenceNode("Manual")

        auto_node.add_children(check_auto_play_node, select_skill_node, select_target_node,
                               show_skill_name_node, skill_animation_node, use_skill_node)
        manual_node.add_children(check_manual_play_node, show_skill_name_node,
                                 skill_animation_node, use_skill_node)

        process_skill_node.add_children(auto_node, manual_node)

        self.bt = BehaviorTree(process_skill_node)

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

    def draw(self):
        self.cur_state.draw(self)
        if self.showing_skill_name:
            self.selected_skill_data.draw_before_use()

        elif self.showing_skill_animation:
            self.selected_skill_data.draw_animation(self.skill_frame)

    def stop_bgm(self):
        self.bgm.stop()

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        self.bt.run()

    def handle_events(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[event.type, event.key]
            self.add_event(key_event)
