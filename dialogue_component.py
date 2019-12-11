import game_framework
import battle_state
from pico2d import *
import death_end_state
import initium_state

ALICE, LUCIFEL, LUCIFER, FIRST, CITY = range(5)
SELCECTION, DEFAULT = range(2)
SPACE, SHIFT = range(2)

key_event_table = {
    (SDL_KEYDOWN, SDLK_SPACE): SPACE,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT
}


class DeFaultState:

    @staticmethod
    def enter(dialogue, event):
        if dialogue.dialogue_with == ALICE:
            if dialogue.dialogue_type[dialogue.now_dialogue] == SELCECTION:
                if event == SPACE:
                    game_framework.change_state(death_end_state)
                elif event == SHIFT:
                    dialogue.now_dialogue += 1
            else:
                if event == SPACE:
                    dialogue.now_dialogue += 1

            if dialogue.now_dialogue >= len(dialogue.dialogue_image):
                battle_state.boss_battle = ALICE
                game_framework.change_state(battle_state)

        else:
            if event == SPACE:
                dialogue.now_dialogue += 1

                if dialogue.dialogue_with == LUCIFEL:
                    if dialogue.now_dialogue == 3:
                        dialogue.now_dialogue += 1
                        battle_state.boss_battle = LUCIFEL
                        game_framework.push_state(battle_state)

                if dialogue.now_dialogue >= len(dialogue.dialogue_image):
                    if dialogue.dialogue_with == FIRST:
                        initium_state.first_dialogue_played = True
                    if dialogue.dialogue_with == CITY:
                        initium_state.city_dialogue_played = True

    @staticmethod
    def exit(dialogue, event):
        pass

    @staticmethod
    def do(dialogue):
        pass

    @staticmethod
    def draw(dialogue):
        if dialogue.now_dialogue < len(dialogue.dialogue_image):
            dialogue.dialogue_image[dialogue.now_dialogue].draw(640, 360)


next_state_table = {
    DeFaultState: {SHIFT: DeFaultState, SPACE: DeFaultState},
}


class Dialogue:

    def __init__(self, someone):
        self.dialogue_with = someone

        if self.dialogue_with == ALICE:
            self.dialogue_image = [load_image("resource/dialogue/aliceDialogue1.png"),
                                   load_image("resource/dialogue/aliceDialogue2.png"),
                                   load_image("resource/dialogue/aliceDialogue3.png")]

            self.dialogue_type = [DEFAULT, SELCECTION, DEFAULT]

        elif self.dialogue_with == LUCIFER:
            self.dialogue_image = [load_image("resource/dialogue/luciferDialogue1.png")]

        elif self.dialogue_with == LUCIFEL:
            self.dialogue_image = [load_image("resource/dialogue/lucifelDialogue1.png"),
                                   load_image("resource/dialogue/lucifelDialogue2.png"),
                                   load_image("resource/dialogue/selfDialogue7.png"),
                                   load_image("resource/dialogue/lucifelDialogue3.png")]

        elif self.dialogue_with == FIRST:
            self.dialogue_image = [load_image("resource/dialogue/selfDialogue1.png"),
                                   load_image("resource/dialogue/someoneDialogue1.png"),
                                   load_image("resource/dialogue/selfDialogue2.png"),
                                   load_image("resource/dialogue/someoneDialogue2.png"),
                                   load_image("resource/dialogue/someoneDialogue3.png"),
                                   load_image("resource/dialogue/someoneDialogue4.png"),
                                   load_image("resource/dialogue/someoneDialogue5.png"),
                                   load_image("resource/dialogue/selfDialogue3.png")]

        elif self.dialogue_with == CITY:
            self.dialogue_image = [load_image("resource/dialogue/selfDialogue4.png"),
                                   load_image("resource/dialogue/someoneDialogue6.png"),
                                   load_image("resource/dialogue/someoneDialogue7.png"),
                                   load_image("resource/dialogue/someoneDialogue8.png"),
                                   load_image("resource/dialogue/someoneDialogue9.png"),
                                   load_image("resource/dialogue/someoneDialogue10.png"),
                                   load_image("resource/dialogue/selfDialogue5.png"),
                                   load_image("resource/dialogue/selfDialogue6.png")]

        self.now_dialogue = 0

        self.event_que = []
        self.cur_state = DeFaultState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)

    def handle_events(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
