from nfa import NFA
import re


def pattern_check(regex, input_str, nfa):
    states, is_accepted = nfa.IsAcceptByNFA(input_str)
    pattern_is_correct = bool(re.match(regex, input_str))
    return is_accepted is pattern_is_correct


def test_findRegExp_1():
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

    # regex = 'a(b*(bab)*)*'
    nfa.findRegExp()


def test_findRegExp_1():
    states = "{1, 2, 3, 4}"
    input_symbols = "{a, b}"
    final_states = '{3, 4}'
    transition_count = 9
    transitions = [
        '1, 2, a',
        '1, 3, b',
        '2, 1, a',
        '2, 3, ',
        '3, 3, b',
        '3, 4, b',
        '4, 3, a',
        '4, 2, a', ]
    initial_state = "1"
    nfa = NFA(states=states,
              input_symbols=input_symbols,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,)
    nfa.showSchematicNFA()
    nfa.findRegExp()
