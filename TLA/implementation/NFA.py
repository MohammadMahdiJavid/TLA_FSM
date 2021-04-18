from .FA import FA
from .automaton import Automaton


class NFA (FA):
    '''
        Non-Deterministic Finite Automata
    '''

    def __init__(self, states, transitions, initial_states, final_states, input_symbs):
        super(FA, self).__init__(states, transitions,
                                 initial_states, final_states, input_symbs)
