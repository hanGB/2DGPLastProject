import random

HIT, AWFUL, WEAK, HALF, NON, REVEN, SHOCK, MISS = range(8)
MATTER_ATTACK, MIND_ATTACK, MATTER_DEFENCE, MIND_DEFENCE, HIT_RATE, AVOID_RATE = range(6)


def calculate_damage_for_normal_skill(user, target, skill):
    user_stat = user.get_stat()
    target_stat = target.get_stat()
    target_attribute = target.get_attribute()
    skill_pattern = skill.get_pattern()
    user_buff = user.get_buff()
    target_buff = target.get_buff()

    buff = user_buff[0] - target_buff[1]

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
        additional__damage = user_stat[MATTER_ATTACK] - target_stat[MATTER_DEFENCE]
    else:
        additional__damage = user_stat[MIND_ATTACK] - target_stat[MIND_DEFENCE]

    additional_damage = additional__damage / 100

    damage = skill.get_damage() * (1 + additional__damage)

    damage *= buff

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


def can_use_skill(user, skill):
    if user.get_Md() < skill.get_Md():
        return False

    if user.get_turn() < skill.get_turn():
        return False

    user.set_Md(user.get_Md() - skill.get_Md())
    user.set_turn(user.get_turn() - skill.get_turn())
    return True


def calculate_damage(user, target, skill):

    skill_type = skill.get_number() / 10

    if skill_type < 5 or 9 <= skill_type < 10:
        weakness, damage = calculate_damage_for_normal_skill(user, target, skill)
        target.set_hit_weakness(weakness)
        if target.get_Bd() - damage > 0:
            target.set_Bd(target.get_Bd() - damage)
        else:
            target.set_Bd(0)

        if weakness == REVEN:
            if user.get_Bd() - damage:
                user.set_Bd(user.get_Bd() - damage)
            else:
                user.set_Bd(0)

        elif weakness == SHOCK:
            user.set_down_level(2)


def use_skill(user, target, skill):
    if can_use_skill(user, skill):
        calculate_damage(user, target, skill)
