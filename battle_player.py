class BattlePlayer:
    def __init__(self, player):
        self.player = player
        self.player_cnt = len(player)
        self.player_slt = 0

    def get_player(self, slt):
        return self.player[slt]

    def draw(self):
        for n in range(self.player_cnt):
            self.player[n].draw_bar(n)