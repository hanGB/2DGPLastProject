DOWN2 = 2


def contract_enemy(user, target):
    down_level = target.get_down_level()

    if down_level >= DOWN2:
        user.set_card(target.get_card())
        target.set_Bd(-1)
