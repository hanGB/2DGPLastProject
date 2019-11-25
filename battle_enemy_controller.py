from pico2d import *
import random
import enemy_data
import game_framework
import battle_state
import death_end_state
from damage_calculator import use_skill
from behavior_tree import BehaviorTree, SequenceNode, LeafNode


SKILL_FRAMES = 8
ANIMATION_ACCELERATION = 2.5

TIME_PER_SELECTING = 2
SELECTING_PER_TIME = 1.0 / TIME_PER_SELECTING
FRAMES_PER_SELECTING = 8

LEFT_DOWN, RIGHT_DOWN, LEFT_UP, RIGHT_UP, TURN_CHANGE, VICTORY, DEFEAT = range(7)

key_event_table = {
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP
}


class BattleEndState:
    @staticmethod
    def enter(battle_enemy, event):
        if event == VICTORY:
            battle_enemy.is_victory = True
            battle_enemy.waiting_time = 0

        elif event == DEFEAT:
            battle_enemy.is_victory = False
            battle_enemy.waiting_time = 0

    @staticmethod
    def exit(battle_enemy, event):
        pass

    @staticmethod
    def do(battle_enemy):
        battle_enemy.waiting_time += game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME
        if battle_enemy.waiting_time > 3:
            if battle_enemy.is_victory:
                for player in battle_state.player.get_all_players():
                    player.give_exp(battle_enemy.exp)
                game_framework.pop_state()
            else:
                game_framework.change_state(death_end_state)

    @staticmethod
    def draw(battle_enemy):
        if battle_enemy.is_victory:
            battle_enemy.battle_result_image.clip_draw(0, 150, 800, 150, 635, 500)
        else:
            battle_enemy.battle_result_image.clip_draw(0, 0, 800, 150, 665, 500)


class EnemyAttackState:
    @staticmethod
    def enter(battle_enemy, event):
        battle_enemy.auto_play = True

    @staticmethod
    def exit(battle_enemy, event):
        pass

    @staticmethod
    def do(battle_enemy):
        if battle_state.now_turn == 0:
            battle_enemy.add_event(TURN_CHANGE)

        if battle_state.now_turn == 1:
            check_enemy = battle_enemy.enemy_now
            if not battle_state.skill_processing:
                if battle_enemy.enemy[battle_enemy.enemy_now].get_turn() == 0:
                    for e in range(battle_enemy.number_of_enemies):
                        battle_enemy.enemy_now = (battle_enemy.enemy_now + 1) % battle_enemy.number_of_enemies
                        if battle_enemy.enemy[battle_enemy.enemy_now].get_turn() != 0:
                            break

                    if check_enemy == battle_enemy.enemy_now:
                        battle_state.now_turn = 0
                        for e in range(battle_enemy.number_of_enemies):
                            battle_enemy.enemy[e].set_turn(battle_enemy.enemy[e].get_max_turn())
                else:
                    if not battle_enemy.auto_play:
                        battle_enemy.auto_play = True

        for enemy in battle_enemy.enemy:
            if enemy.get_Bd() <= 0:
                battle_enemy.exp += (enemy.get_type() ** 2)
                if battle_enemy.number_of_enemies != 1:
                    battle_enemy.enemy.remove(enemy)
                    battle_enemy.number_of_enemies -= 1
                    battle_enemy.enemy_now = 0
                else:
                    battle_enemy.add_event(VICTORY)

        counter = len(battle_state.player.get_all_players())
        for player in battle_state.player.get_all_players():
            if player.get_Bd() <= 0:
                counter -= 1

            if counter == 0:
                battle_enemy.add_event(DEFEAT)

    @staticmethod
    def draw(battle_enemy):
        if battle_enemy.number_of_enemies == 1:
            battle_enemy.enemy[0].draw(2, 0)

        elif battle_enemy.number_of_enemies == 2:
            for n in range(battle_enemy.number_of_enemies):
                battle_enemy.enemy[n].draw(2 * n + 0.5, n - battle_enemy.selected_enemy)

        elif battle_enemy.number_of_enemies == 3:
            for n in range(battle_enemy.number_of_enemies):
                battle_enemy.enemy[n].draw(n + n * 0.7, n - battle_enemy.selected_enemy)

        elif battle_enemy.number_of_enemies == 4:
            for n in range(battle_enemy.number_of_enemies):
                battle_enemy.enemy[n].draw(n + n * 0.2, n - battle_enemy.selected_enemy)


class EnemySelectState:
    @staticmethod
    def enter(battle_enemy, event):
        if event == LEFT_DOWN:
            battle_enemy.selecting = -1
            battle_enemy.selected_enemy = (battle_enemy.selected_enemy + battle_enemy.selecting) \
                                          % battle_enemy.number_of_enemies
            battle_enemy.sub_counter = 0
        elif event == RIGHT_DOWN:
            battle_enemy.selecting = 1
            battle_enemy.selected_enemy = (battle_enemy.selected_enemy + battle_enemy.selecting) \
                                          % battle_enemy.number_of_enemies
            battle_enemy.sub_counter = 0
        elif event == LEFT_UP or event == RIGHT_UP:
            battle_enemy.selecting = 0

    @staticmethod
    def exit(battle_enemy, event):
        pass

    @staticmethod
    def do(battle_enemy):
        if battle_state.now_turn == 1:
            battle_enemy.add_event(TURN_CHANGE)

        if battle_enemy.selecting == 1 or battle_enemy.selecting == -1:
            battle_enemy.sub_counter += game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME

            if battle_enemy.sub_counter > 1:
                battle_enemy.sub_counter = 0
                battle_enemy.selected_enemy = (battle_enemy.selected_enemy + battle_enemy.selecting) \
                                            % battle_enemy.number_of_enemies

        for enemy in battle_enemy.enemy:
            if enemy.get_Bd() <= 0:
                battle_enemy.exp += (enemy.get_type() ** 2)
                if battle_enemy.number_of_enemies != 1:
                    battle_enemy.enemy.remove(enemy)
                    battle_enemy.number_of_enemies -= 1
                    battle_enemy.enemy_now = 0
                    battle_enemy.selected_enemy = 0
                else:
                    battle_enemy.add_event(VICTORY)

        counter = len(battle_state.player.get_all_players())
        for player in battle_state.player.get_all_players():
            if player.get_Bd() <= 0:
                counter -= 1

            if counter == 0:
                battle_enemy.add_event(DEFEAT)

    @staticmethod
    def draw(battle_enemy):
        if battle_enemy.number_of_enemies == 1:
            battle_enemy.enemy[0].draw(2, 0)

        elif battle_enemy.number_of_enemies == 2:
            for n in range(battle_enemy.number_of_enemies):
                battle_enemy.enemy[n].draw(2 * n + 0.5, n - battle_enemy.selected_enemy)

        elif battle_enemy.number_of_enemies == 3:
            for n in range(battle_enemy.number_of_enemies):
                battle_enemy.enemy[n].draw(n + n * 0.7, n - battle_enemy.selected_enemy)

        elif battle_enemy.number_of_enemies == 4:
            for n in range(battle_enemy.number_of_enemies):
                battle_enemy.enemy[n].draw(n + n * 0.2, n - battle_enemy.selected_enemy)


next_state_table = {
    EnemySelectState: {LEFT_DOWN: EnemySelectState, LEFT_UP: EnemySelectState,
                       RIGHT_DOWN: EnemySelectState, RIGHT_UP: EnemySelectState, TURN_CHANGE: EnemyAttackState,
                       VICTORY: BattleEndState, DEFEAT: BattleEndState},
    EnemyAttackState: {LEFT_DOWN: EnemyAttackState, LEFT_UP: EnemyAttackState,
                       RIGHT_DOWN: EnemyAttackState, RIGHT_UP: EnemyAttackState, TURN_CHANGE: EnemySelectState,
                       VICTORY: BattleEndState, DEFEAT: BattleEndState},
    BattleEndState: {LEFT_DOWN: BattleEndState, LEFT_UP: BattleEndState,
                     RIGHT_DOWN: BattleEndState, RIGHT_UP: BattleEndState, TURN_CHANGE: BattleEndState,
                     VICTORY: BattleEndState, DEFEAT: BattleEndState}
}


class BattleEnemy:
    battle_result_image = None

    def __init__(self):
        self.selecting = 0
        self.sub_counter = 0
        self.number_of_enemies = random.randint(1, 4)
        self.selected_enemy = 0
        self.enemy = [enemy_data.Enemy(random.randint(1, 5)) for n in range(self.number_of_enemies)]
        self.event_que = []
        self.cur_state = EnemySelectState
        self.cur_state.enter(self, None)
        self.enemy_now = 0
        self.is_victory = False
        self.waiting_time = 0
        self.exp = 0

        if BattleEnemy.battle_result_image is None:
            BattleEnemy.battle_result_image = load_image("resource/interface/battleResult.png")

        self.user = self.enemy[self.enemy_now]
        self.targets = battle_state.player.get_list()

        self.selected_skill_data = None
        self.selected_target = None

        self.sword_trigger = battle_state.sword_trigger

        self.showing_skill_name = False
        self.time_of_showing_skill = 0
        self.showing_skill_animation = False
        self.skill_frame = 0

        self.auto_play = False

        self.build_behavior_tree()

    def check_auto_play(self):
        if self.auto_play:
            battle_state.skill_processing = True
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.FAIL

    def select_skill(self):
        self.user = self.enemy[self.enemy_now]

        skills = self.user.get_card().get_skill()
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
        self.targets = battle_state.player.get_list()

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
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        check_auto_play_node = LeafNode("Check Auto Play", self.check_auto_play)

        select_skill_node = LeafNode("Select Skill", self.select_skill)
        select_target_node = LeafNode("Select Target", self.select_target)
        show_skill_name_node = LeafNode("Show Skill Name", self.show_skill_name)
        skill_animation_node = LeafNode("Skill Animation", self.skill_animation)
        use_skill_node = LeafNode("Use Skill", self.use_skill)

        auto_node = SequenceNode("Auto")

        auto_node.add_children(check_auto_play_node, select_skill_node, select_target_node,
                               show_skill_name_node, skill_animation_node, use_skill_node)

        self.bt = BehaviorTree(auto_node)

    def get_selected_enemy(self):
        return self.enemy[self.selected_enemy]

    def get_selected_enemy_number(self):
        return self.selected_enemy

    def get_number_of(self):
        return self.number_of_enemies

    def get_list(self):
        return self.enemy

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        if self.showing_skill_name:
            self.selected_skill_data.draw_before_use()

        elif self.showing_skill_animation:
            self.selected_skill_data.draw_animation(self.skill_frame)

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
