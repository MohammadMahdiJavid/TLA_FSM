from ..implementation.NFA import *


def input_test_1():
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
    initial_states = ["q0"]
    nfa = NFA(states=states,
              input_symbs=input_symbols,
              transitions=transitions,
              initial_states=initial_states,
              final_states=final_states)
