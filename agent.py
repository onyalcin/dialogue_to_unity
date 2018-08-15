import time
import random
import logging
import threading
from enum import Enum
from bml import Body, Gesture, Speech


logger = logging.getLogger(__name__)


class State(Enum):
    Idle = 0
    Listening = 1
    Thinking = 2
    Speaking = 3


class Agent(threading.Thread):
    def __init__(self, character):
        super().__init__(name='Agent')
        self._stop_event = threading.Event()
        self._lock = threading.Lock()
        self._character = character
        self._state = State.Idle
        self._param = None
        self._new_state = None
        self._new_param = None

    def run(self):
        while not self._stop_event.is_set():
            state = self._refresh_state()

            if state == State.Idle:
                self._state_idle()
            elif state == State.Listening:
                self._state_listening()
            elif state == State.Thinking:
                self._state_thinking()
            elif state == State.Speaking:
                self._state_speaking()

    def stop(self):
        self._stop_event.set()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.join()

    def _transition(self, new_state, param=None):
        with self._lock:
            self._new_state = new_state
            self._new_param = param

    def transition_idle(self):
        self._transition(State.Idle)

    def transition_listening(self):
        self._transition(State.Listening)

    def transition_thinking(self):
        self._transition(State.Thinking)

    def transition_speaking(self, response):
        assert isinstance(response, list)
        for el in response:
            assert isinstance(el[0], Speech)
        self._transition(State.Speaking, response)

    def _state_idle(self):
        # FIXME: This is so horrible I cant even look at it
        if self._character.__class__.__name__ == 'SmartBody':
            self._character.execute([Body(posture='ChrBrad@Idle01')])
        elif self._character.__class__.__name__ == 'UnityBody':
            #self._character.execute([Gesture(name= 'idle-pondering')])
            pass
        while True:
            if not self._check_state(State.Idle):
                break

    def _state_listening(self):
        self._random_actions(State.Listening, self.LISTENING_ACTIONS)

    def _state_thinking(self):
        self._random_actions(State.Thinking, self.THINKING_ACTIONS)

    def _state_speaking(self):
        for part in self._param[:-1]:
            self._character.execute(part)

        self._character.execute_and_check(self._param[-1])
        self._do_transition(State.Idle)

    def _random_actions(self, state, actions):
        while self._check_state(state):
            actions = list(actions)
            random.shuffle(actions)

            for anim_time, command in actions:
                self._character.execute_and_check(command)

                if not self._check_state(state):
                    break

    def _sleep(self, t, period=0.1):
        initial_state = self._state
        start = time.time()

        while t == 0 or time.time() - start < t:
            if self._check_state(initial_state):
                time.sleep(period)
            else:
                return False
        return True

    def _do_transition(self, new_state, new_param=None):
        logging.debug('Actor state transition: %s -> %s', self._state, new_state)
        self._state = new_state
        self._param = new_param

    def _refresh_state(self):
        with self._lock:
            if self._new_state is not None:
                self._do_transition(self._new_state, self._new_param)
                self._new_state = None
                self._new_param = None

        return self._state

    def _check_state(self, expected_state):
        state = self._refresh_state()
        return not self._stop_event.is_set() and state == expected_state
