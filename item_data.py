import battle_state

BD, MD, BD_MD, REBIRTH = range(4)


def item_data(type):
    if type == 0:
        return BD, 50
    elif type == 1:
        return BD, 250
    elif type == 2:
        return BD, 500
    elif type == 3:
        return MD, 50
    elif type == 4:
        return MD, 150
    elif type == 5:
        return BD_MD, 999
    elif type == 6:
        return REBIRTH, 999


def use_item(target, type):
    players = battle_state.player.get_list()
    player_with_item_data = players[0]

    item_list = player_with_item_data.get_item()

    if item_list[type] != 0:
        item_effect, item_val = item_data(type)
        max_Bd, Bd = target.get_max_Bd(), target.get_Bd()
        max_Md, Md = target.get_max_Md(), target.get_Md()

        if item_effect == BD:
            if max_Bd > Bd:
                after_Bd = Bd + item_val

                if after_Bd > max_Bd:
                    after_Bd = max_Bd

                target.set_Bd(after_Bd)

                player_with_item_data.set_item(type, -1)

        elif item_effect == MD:
            if max_Md > Md:
                after_Md = Md + item_val

                if after_Md > max_Md:
                    after_Md = max_Md

                target.set_Md(after_Md)

                player_with_item_data.set_item(type, -1)

        elif item_effect == BD_MD:
            if max_Bd > Bd or max_Md > Md:
                if item_val == 999:
                    target.set_Bd(max_Bd)
                    target.set_Md(max_Md)

                    player_with_item_data.set_item(type, -1)

        elif item_effect == REBIRTH:
            if Bd <= 0:
                target.set_Bd(max_Bd)

                player_with_item_data.set_item(type, -1)

