from pico2d import *
import game_framework
import battle_state
import battle_analyze_state
import game_world
from skill_data import Skill
from damage_calculator import can_use_skill
from damage_calculator import use_skill
from behavior_tree import BehaviorTree, SequenceNode, LeafNode

TIME_PER_SELECTING = 2
SELECTING_PER_TIME = 1.0 / TIME_PER_SELECTING
FRAMES_PER_SELECTING = 8
SKILL_FRAMES = 4
ANIMATION_ACCELERATION = 2.5

name = "sword_trigger_state"

sword_trigger_ui = None


class SwordTriggerUi:
    image = None

    def __init__(self, key):
        self.key = key

        if SwordTriggerUi.image is None:
            SwordTriggerUi.image = load_image("resource/interface/sdInBattle.png")
        self.sword_trigger = [Skill(91), Skill(90)]

        self.selected_skill_data = None
        self.selected_target = None

        self.sword_trigger = battle_state.sword_trigger

        self.showing_skill_animation = False
        self.skill_frame = 0

        self.manual_play = False

        self.build_behavior_tree()

    def set_manual_play(self, true):
        self.manual_play = true

    def set_skill_target(self, skill, target):
        self.selected_skill_data = skill
        self.selected_target = target

    def check_manual_play(self):
        if self.manual_play:
            battle_state.skill_processing = True
            return BehaviorTree.SUCCESS

        else:
            return BehaviorTree.FAIL

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
        use_skill(battle_state.player.get_player(battle_state.battle_ui.player_now),
                  self.selected_target, self.selected_skill_data)

        battle_state.skill_processing = False

        self.manual_play = False
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        check_manual_play_node = LeafNode("Check Manual Play", self.check_manual_play)

        skill_animation_node = LeafNode("Skill Animation", self.skill_animation)
        use_skill_node = LeafNode("Use Skill", self.use_skill)

        process_skill_node = SequenceNode("Skill Process")
        process_skill_node.add_children(check_manual_play_node, skill_animation_node, use_skill_node)

        self.bt = BehaviorTree(process_skill_node)

    def get_key(self):
        return self.key

    def get_sword_trigger(self, number):
        return self.sword_trigger[number]

    def update(self):
        self.bt.run()

    def draw(self):
        SwordTriggerUi.image.clip_draw(0,  (2 - self.key) * 50, 250, 50, 300, 170)

        if self.showing_skill_animation:
            self.selected_skill_data.draw_animation(self.skill_frame)


def enter():
    global sword_trigger_ui

    sword_trigger_ui = SwordTriggerUi(battle_state.battle_ui.get_sd_key())
    game_world.add_object(sword_trigger_ui, 2)


def exit():
    global sword_trigger_ui
    game_world.remove_object(sword_trigger_ui)


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if not battle_state.skill_processing:
            if event.key == SDLK_s and event.type == SDL_KEYDOWN:
                if sword_trigger_ui.get_key() == 0:
                    if (can_use_skill(battle_state.player.get_player(battle_state.battle_ui.player_now),
                                      sword_trigger_ui.get_sword_trigger(0))):

                        sword_trigger_ui.set_manual_play(True)
                        sword_trigger_ui.set_skill_target(sword_trigger_ui.get_sword_trigger(0),
                                                          battle_state.battle_enemy.get_selected_enemy())

            elif event.key == SDLK_d and event.type == SDL_KEYDOWN:
                if sword_trigger_ui.get_key() == 1:
                    if (can_use_skill(battle_state.player.get_player(battle_state.battle_ui.player_now),
                                      sword_trigger_ui.get_sword_trigger(1))):

                        sword_trigger_ui.set_manual_play(True)
                        sword_trigger_ui.set_skill_target(sword_trigger_ui.get_sword_trigger(1),
                                                          battle_state.battle_enemy.get_selected_enemy())

            elif event.key == (SDLK_a and event.type == SDL_KEYDOWN) \
                    or (event.key == SDLK_LSHIFT and event.type == SDL_KEYDOWN):
                battle_state.battle_ui.set_is_main(True)
                game_framework.pop_state()

            elif event.key == SDLK_x and event.type == SDL_KEYDOWN:
                battle_state.battle_ui.player_target \
                    = (battle_state.battle_ui.player_target + 1) % battle_state.player.number_of_players

            elif event.key == SDLK_TAB and event.type == SDL_KEYDOWN:
                game_framework.push_state(battle_analyze_state)

            else:
                battle_state.battle_enemy.handle_events(event)


def update():
    if battle_state.player.get_player(battle_state.battle_ui.get_player_now()).get_turn() == 0:
        battle_state.battle_ui.set_is_main(True)
        game_framework.pop_state()

    if battle_state.player.get_player(battle_state.battle_ui.get_player_now()).get_down_level() != 0:
        battle_state.battle_ui.set_is_main(True)
        game_framework.pop_state()

    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
