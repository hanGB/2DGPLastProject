from pico2d import *
import random
import enemy_data

LEFT_DOWN, RIGHT_DOWN, LEFT_UP, RIGHT_UP = range(4)

key_event_table = {
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
}


class EnemySelectState:
    @staticmethod
    def enter(battle_enemy, event):
        if event == LEFT_DOWN:
            battle_enemy.selecting = -1
            battle_enemy.selected_enemy = (battle_enemy.selected_enemy + battle_enemy.selecting) \
                                          % battle_enemy.number_of_enemys
            battle_enemy.sub_counter = 0
        elif event == RIGHT_DOWN:
            battle_enemy.selecting = 1
            battle_enemy.selected_enemy = (battle_enemy.selected_enemy + battle_enemy.selecting) \
                                          % battle_enemy.number_of_enemys
            battle_enemy.sub_counter = 0
        elif event == LEFT_UP or event == RIGHT_UP:
            battle_enemy.selecting = 0

    @staticmethod
    def exit(battle_enemy, event):
        pass

    @staticmethod
    def do(battle_enemy):
        if battle_enemy.selecting == 1 or battle_enemy.selecting == -1:
            battle_enemy.sub_counter += 1

            if battle_enemy.sub_counter == 100:
                battle_enemy.sub_counter = 0
                battle_enemy.selected_enemy = (battle_enemy.selected_enemy + battle_enemy.selecting) \
                                         % battle_enemy.number_of_enemys

    @staticmethod
    def draw(battle_enemy):
        if battle_enemy.number_of_enemys == 1:
            battle_enemy.enemy[0].draw(2, 0)

        elif battle_enemy.number_of_enemys == 2:
            for n in range(battle_enemy.number_of_enemys):
                battle_enemy.enemy[n].draw(2 * n + 0.5, n - battle_enemy.selected_enemy)

        elif battle_enemy.number_of_enemys == 3:
            for n in range(battle_enemy.number_of_enemys):
                battle_enemy.enemy[n].draw(n + n * 0.7, n - battle_enemy.selected_enemy)

        elif battle_enemy.number_of_enemys == 4:
            for n in range(battle_enemy.number_of_enemys):
                battle_enemy.enemy[n].draw(n + n * 0.2, n - battle_enemy.selected_enemy)


next_state_table = {
    EnemySelectState: {LEFT_DOWN: EnemySelectState, LEFT_UP: EnemySelectState,
                       RIGHT_DOWN: EnemySelectState, RIGHT_UP: EnemySelectState}
}


class BattleEnemy:
    def __init__(self):
        self.selecting = 0
        self.sub_counter = 0
        self.number_of_enemys = random.randint(1, 4)
        self.selected_enemy = 0
        self.enemy = [enemy_data.Enemy(random.randint(1, 11)) for n in range(self.number_of_enemys)]
        self.event_que = []
        self.cur_state = EnemySelectState
        self.cur_state.enter(self, None)

    def get_selected_enemy(self):
        return self.selected_enemy

    def update_state(self):
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def handle_events(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[event.type, event.key]
            self.add_event(key_event)
