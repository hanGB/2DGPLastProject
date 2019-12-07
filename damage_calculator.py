import random
from player_data import Player
from enemy_data import Enemy
import battle_state

HIT, AWFUL, WEAK, HALF, NON, REVEN, SHOCK, MISS = range(8)
MATTER_ATTACK, MIND_ATTACK, MATTER_DEFENCE, MIND_DEFENCE, HIT_RATE, AVOID_RATE = range(6)
ATTACK_BUFF, DEFENCE_BUFF = range(2)


def calculate_damage_for_normal_skill(user, target, skill):
    user_stat = user.get_stat()
    target_stat = target.get_stat()
    target_attribute = target.get_attribute()
    skill_pattern = skill.get_pattern()
    user_buff = user.get_buff()
    target_buff = target.get_buff()

    buff = user_buff[ATTACK_BUFF] - target_buff[DEFENCE_BUFF]

    buff = 1 + buff / 10

    target_weakness = target_attribute[skill_pattern]

    # non 일 경우 데미지 계산없이 리턴
    if target_weakness == NON:
        return NON, 0

    additional_hit_rate = user_stat[HIT_RATE] - target_stat[AVOID_RATE]

    additional_hit_rate = additional_hit_rate * 0.3
    hit_rate = skill.get_rate() + additional_hit_rate

    rate_check = random.randint(0, 100)

    if hit_rate < rate_check:
        return MISS, 0

    if skill_pattern < 4:
        additional_damage = user_stat[MATTER_ATTACK] - target_stat[MATTER_DEFENCE]
    else:
        additional_damage = user_stat[MIND_ATTACK] - target_stat[MIND_DEFENCE]

    additional_damage = additional_damage / 100

    damage = skill.get_damage() * (1 + additional_damage)

    damage *= buff

    if damage < 2:
        damage = 2

    if target_weakness == HIT:
        return HIT, damage

    elif target_weakness == AWFUL:
        return AWFUL, damage * 2

    elif target_weakness == WEAK:
        return WEAK, damage * 1.5

    elif target_weakness == HALF:
        return HALF, damage * 0.5

    elif target_weakness == REVEN:
        return REVEN, damage

    elif target_weakness == SHOCK:
        return SHOCK, damage * 0.5


def calculate_down_level_for_normal_skill(user, target, weakness, damage):
    target.set_hit_weakness(weakness)
    target_down_level = target.get_down_level()

    if target_down_level == 0:
        if weakness == AWFUL:
            target.set_down_level(3)
        elif weakness == WEAK:
            target.set_down_level(1)

    elif target_down_level == 1:
        if weakness == AWFUL:
            target.set_down_level(3)
        elif weakness == WEAK:
            target.set_down_level(2)

    elif target_down_level == 2:
        if weakness == AWFUL:
            target.set_down_level(3)
        elif weakness == WEAK:
            target.set_down_level(1)

    if target.get_Bd() - damage > 0:
        target.set_Bd(target.get_Bd() - damage)
    else:
        target.set_Bd(0)
        target.set_down_level(0)

    if weakness == REVEN:
        if user.get_Bd() - damage > 0:
            user.set_Bd(user.get_Bd() - damage)
        else:
            user.set_Bd(1)

    elif weakness == SHOCK:
        user.set_down_level(2)


def calculate_buff_for_buff_skill(target, skill):
    target_buff = target.get_buff()
    buff_type = skill.get_buff_type()
    effect = skill.get_damage()

    is_hit = [False, False]

    if buff_type == 2:
        if effect > 0:
            if target_buff[ATTACK_BUFF] < 9:
                is_hit[ATTACK_BUFF] = True
                target_buff[ATTACK_BUFF] += effect
                if target_buff[ATTACK_BUFF] > 9:
                    target_buff[ATTACK_BUFF] = 9

            if target_buff[DEFENCE_BUFF] < 9:
                is_hit[DEFENCE_BUFF] = True
                target_buff[DEFENCE_BUFF] += effect
                if target_buff[DEFENCE_BUFF] > 9:
                    target_buff[DEFENCE_BUFF] = 9

        if effect < 0:
            if target_buff[ATTACK_BUFF] > -9:
                is_hit[ATTACK_BUFF] = True
                target_buff[ATTACK_BUFF] += effect
                if target_buff[ATTACK_BUFF] < -9:
                    target_buff[ATTACK_BUFF] = -9

            if target_buff[DEFENCE_BUFF] > -9:
                is_hit[DEFENCE_BUFF] = True
                target_buff[DEFENCE_BUFF] += effect
                if target_buff[DEFENCE_BUFF] < -9:
                    target_buff[DEFENCE_BUFF] = -9
    else:
        if effect > 0:
            if target_buff[buff_type] < 9:
                is_hit[buff_type] = True
                target_buff[buff_type] += effect
                if target_buff[buff_type] > 9:
                    target_buff[buff_type] = 9

        if effect < 0:
            if target_buff[buff_type] > -9:
                is_hit[buff_type] = True
                target_buff[buff_type] += effect
                if target_buff[buff_type] < -9:
                    target_buff[buff_type] = -9

    target.set_buff(target_buff)

    if is_hit[ATTACK_BUFF] or is_hit[DEFENCE_BUFF]:
        target.set_hit_weakness(HIT)

    else:
        target.set_hit_weakness(MISS)


def can_use_skill(user, skill):
    if user.get_Md() < skill.get_Md():
        return False

    if user.get_turn() < skill.get_turn():
        return False

    return True


def calculate_damage(user, target, skill):

    skill_type = skill.get_number() / 10
    all_targets = skill.get_all_targets()
    if skill_type < 5 or 9 <= skill_type < 10:
        if all_targets:
            if isinstance(target, Enemy):
                for enemy in battle_state.battle_enemy.get_list():
                    weakness, damage = calculate_damage_for_normal_skill(user, enemy, skill)
                    calculate_down_level_for_normal_skill(user, enemy, weakness, damage)
                    enemy.set_time_to_show_hit()
            elif isinstance(target, Player):
                for player in battle_state.player.get_list():
                    weakness, damage = calculate_damage_for_normal_skill(user, player, skill)
                    calculate_down_level_for_normal_skill(user, player, weakness, damage)
                    player.set_time_to_show_hit()
        else:
            weakness, damage = calculate_damage_for_normal_skill(user, target, skill)
            calculate_down_level_for_normal_skill(user, target, weakness, damage)
            target.set_time_to_show_hit()

    elif 5 <= skill_type < 7:
        if all_targets:
            if isinstance(target, Enemy):
                for enemy in battle_state.battle_enemy.get_list():
                    calculate_buff_for_buff_skill(enemy, skill)
                    enemy.set_time_to_show_hit()
            elif isinstance(target, Player):
                for player in battle_state.player.get_list():
                    calculate_buff_for_buff_skill(player, skill)
                    player.set_time_to_show_hit()
        else:
            calculate_buff_for_buff_skill(target, skill)
            target.set_time_to_show_hit()


def use_skill(user, target, skill):
    user.set_Md(user.get_Md() - skill.get_Md())
    user.set_turn(user.get_turn() - skill.get_turn())
    calculate_damage(user, target, skill)
