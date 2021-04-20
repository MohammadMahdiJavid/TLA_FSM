

from nfa import NFA


def test_Equivale1():
    states = "{q0, q1, q2, q3, q4}"
    #  "{, q1, q2}
    input_symbols = "{a, b}"
    final_states = '{q1, q3}'
    transition_count = 6
    transitions = ['q0, q1, a',
                   'q1, q2, b',
                   'q1, q3,',  # lambda transition
                   'q3, q4, b',
                   'q2, q3, a',
                   "q4, q2, a"]
    initial_state = "q0"
    nfa = NFA(states=states,
              input_symbols=input_symbols,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,)
    NFA.createEquivalentDFA(nfa)
