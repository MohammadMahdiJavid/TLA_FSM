from automaton import Automaton


class NFA (FA):
    '''
        Non-Deterministic Finite Automata
    '''

    def __init__(self, states, transition):
        super().__init__(states, transition, initial_states, final_states, input_symbs)
