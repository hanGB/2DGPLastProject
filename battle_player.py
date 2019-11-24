class BattlePlayer:
    def __init__(self, player):
        self.player = player
        self.number_of_players = len(player)
        self.selected_player = 0

    def get_player(self, selected_player):
        return self.player[selected_player]

    def get_all_players(self):
        return self.player

    def get_list(self):
        return self.player

    def get_number_of(self):
        return self.number_of_players

    def update(self):
        pass

    def draw(self):
        for n in range(self.number_of_players):
            self.player[n].draw_bar(n)
