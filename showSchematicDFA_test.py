from nfa import NFA
from dfa import DFA


def test_showSchematicDFA_1():
    states = "{s0, s1, s2, s3, s4}"
    input_symbols = "{5c, 10c, gum}"
    final_states = "{s0, s2}"
    transitions = ['s0, s1, 5c',
                   's1, s2, 5c',
                   's1, s3, 10c',
                   's0, s4, 10c',
                   's4, s3, 5c',
                   's4, s3, 10c',
                   's2, s3, 10c',
                   's2, s3, 5c',
                   's3, s3, 5c',
                   's3, s0, gum']
    initial_state = 's0'
    dfa = DFA(states=states,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,
              input_symbols=input_symbols)
    dfa.showSchematicDFA("file3")


def test_showSchematicDFA_2():
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
    dfa = nfa.createEquivalentDFA()
    dfa.showSchematicDFA('file4')
