import game_framework
from pico2d import *

ALICE, LUCIFEL, LUCIFER, FIRST, CITY = range(3)
DEFAULT, SELCECTION = range(3)

SPACE, UP_DOWN, DOWN_DOWN, UP_UP, DOWN_UP, SELECTION = range(6)

key_event_table = {
    (SDL_KEYDOWN, SDLK_UP): UP_DOWN,
    (SDL_KEYDOWN, SDLK_DOWN): DOWN_DOWN,
    (SDL_KEYUP, SDLK_UP): UP_UP,
    (SDL_KEYUP, SDLK_DOWN): DOWN_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


class DeFaultState:

    @staticmethod
    def enter(dialogue, event):
        if event == SPACE:
            pass

        if event == DOWN_DOWN:
            pass
        elif event == DOWN_UP:
            pass

        if event == UP_DOWN:
            pass
        elif event == UP_UP:
            pass

    @staticmethod
    def exit(dialogue, event):
        pass

    @staticmethod
    def do(dialogue):
        pass

    @staticmethod
    def draw(dialogue):
        pass


class SelectState:

    @staticmethod
    def enter(dialogue, event):
        if event == SPACE:
            pass

        if event == DOWN_DOWN:
            pass
        elif event == DOWN_UP:
            pass

        if event == UP_DOWN:
            pass
        elif event == UP_UP:
            pass

    @staticmethod
    def exit(dialogue, event):
        pass

    @staticmethod
    def do(dialogue):
        pass

    @staticmethod
    def draw(dialogue):
        pass


next_state_table = {
    DeFaultState: {SELECTION: DeFaultState, UP_UP: DeFaultState, UP_DOWN: DeFaultState,
                   DOWN_UP: DeFaultState, DOWN_DOWN: DeFaultState, SPACE: SelectState},

    SelectState: {SELECTION: SelectState, UP_UP: SelectState, UP_DOWN: SelectState,
                  DOWN_UP: SelectState, DOWN_DOWN: SelectState, SPACE: DeFaultState}
}


class Dialogue:

    def __init__(self, someone):
        self.dialogue_with = someone

        if self.dialogue_with == ALICE:
            self.dialogue_image = [load_image("resource/dialogue/aliceDialogue1.png"),
                                   load_image("resource/dialogue/aliceDialogue2.png"),
                                   load_image("resource/dialogue/aliceDialogue3.png")]

            self.dialogue_type = [DEFAULT, SELCECTION, DEFAULT]

        elif self.dialogue_with == LUCIFEL:
            self.dialogue_image = [load_image("resource/dialogue/luciferDialogue1.png")]

        elif self.dialogue_with == LUCIFER:
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

    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
