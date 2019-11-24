from damage_calculator import use_skill
from behavior_tree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
import random
import battle_state
import game_framework

TIME_PER_SELECTING = 2
SELECTING_PER_TIME = 1.0 / TIME_PER_SELECTING
FRAMES_PER_SELECTING = 8
SKILL_FRAMES = 8


def auto_play(user, targets):

    sword_trigger = battle_state.sword_trigger

    skills = user.get_card().get_skill()
    number_of_skills = len(skills)
    skill_select_list = number_of_skills + 2
    count = 0
    targets = targets.get_list()

    while user.get_turn() != 0:
        number_of_targets = len(targets)
        selected_target = random.randint(0, number_of_targets - 1)
        selected_skill = random.randint(0, skill_select_list - 1)

        if count > 10:
            use_skill(user, targets[selected_target], sword_trigger[0])

        if selected_skill - number_of_skills == 0:
            use_skill(user, targets[selected_target], sword_trigger[0])

        elif selected_skill - number_of_skills == 1:
            use_skill(user, targets[selected_target], sword_trigger[1])

        else:
            use_skill(user, targets[selected_target], skills[selected_skill])

        count += 1


class Auto:
    def __init__(self, user, targets):
        self.user = user
        self.targets = targets.get_list()
        self.selected_skill = None
        self.selected_target = None
        self.sword_trigger = battle_state.sword_trigger
        self.time_of_showing_skill = 0
        self.skill_frame = 0

    def select_skill(self):
        skills = self.user.get_card().get_skill()
        usable_skills = []

        for skill in skills:
            if skill.get_Md() <= self.user.get_Md() and skill.get_turn() <= self.user.get_turn():
                usable_skills.append(skill)

        number_of_skills = len(usable_skills)

        if self.user.get_turn() >= 1:
            skill_select_list = number_of_skills + 2
        else:
            skill_select_list = number_of_skills + 1

        index_of_selected_skill = random.randint(0, skill_select_list - 1)

        if index_of_selected_skill - number_of_skills == 0:
            self.selected_skill = self.sword_trigger[0]

        elif index_of_selected_skill - number_of_skills == 1:
            self.selected_skill = self.sword_trigger[1]

        else:
            self.selected_skill = usable_skills[index_of_selected_skill]

        return BehaviorTree.SUCCESS

    def select_target(self):
        usable_targets = []

        for target in self.targets:
            if target.get_Bd() > 0:
                usable_targets.append(target)

        number_of_targets = len(usable_targets)

        index_of_selected_target = random.randint(0, number_of_targets - 1)
        self.selected_target = usable_targets[index_of_selected_target]

    def show_skill_name(self):
        self.selected_skill.draw_before_use()
        self.time_of_showing_skill += game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME

        if self.time_of_showing_skill > 2:
            self.time_of_showing_skill = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def skill_animation(self):
        self.selected_skill.draw_animation(self.skill_frame)
        self.skill_frame += game_framework.frame_time * FRAMES_PER_SELECTING * SELECTING_PER_TIME

        if self.skill_frame > SKILL_FRAMES:
            self.skill_frame = 0
            return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def use_skill(self):
        use_skill(self.user, self.selected_target, self.selected_skill)
        return BehaviorTree.SUCCESS

    def build_behavior_tree(self):
        select_skill_node = LeafNode("Select Skill", self.select_skill)
        select_target_node = LeafNode("Select Target", self.select_target)
        show_skill_name_node = LeafNode("Show Skill Name", self.show_skill_name)
        skill_animation_node = LeafNode("Skill Animation", self.skill_animation)
        use_skill_node = LeafNode("Use Skill", self.use_skill)

        skill_process_node = SequenceNode("Skill Process")
        skill_process_node.add_children(select_skill_node, select_target_node, show_skill_name_node,
                                        skill_animation_node, use_skill_node)

        self.bt = BehaviorTree(skill_process_node)

    def update(self):
        self.bt.run()
