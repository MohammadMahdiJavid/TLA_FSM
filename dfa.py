from fa import FA


class DFA(FA):
    def __init__(self, states, transitions, initial_state, final_states, input_symbols):
        super().__init__(states, transitions,
                         initial_state, final_states, input_symbols)
