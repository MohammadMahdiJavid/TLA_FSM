
from nfa import NFA


def test_showSchematicNFA_1():
    states = "{q0, q1, q2, q3, q4}"
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
    nfa.showSchematicNFA()


def test_showSchematicNFA_2():
    states = "{q0, q1, q2, q3, q4, q5, q6}"
    input_symbols = "{a, b}"
    final_states = '{q1, q3, q6}'
    transition_count = 9
    transitions = ['q0, q1, a',
                   'q1, q1, b',
                   'q1, q2,',
                   'q2, q3, a',
                   'q3, q2, a',
                   'q3, q4, b',
                   'q2, q5, b',
                   'q5, q6, a',
                   'q6, q1, b']
    initial_state = "q0"
    nfa = NFA(states=states,
              input_symbols=input_symbols,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,)
    nfa.showSchematicNFA()
