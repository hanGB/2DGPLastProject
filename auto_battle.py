from damage_calculator import use_skill
import random
import battle_state


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
