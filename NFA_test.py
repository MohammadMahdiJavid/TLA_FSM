
from nfa import NFA


def test_parsing1():
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
    assert True


def test_parsing2():
    states = "{q0, q1, q2, q3, q4}"
    input_symbols = "{a, b}"
    final_states = '{q1, q3}'
    transition_count = 6
    transitions = ['q0, q1, a',
                   'q1, q2, b',
                   'q1, q3,',  # lambda transition
                   'q3, q4, b',
                   'q2, q3, a',
                   "q4, q2, a",
                   'q0, q2, a']
    initial_state = "q0"
    nfa = NFA(states=states,
              input_symbols=input_symbols,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,)
    assert True


def test_NFA_Validation1():
    '''
        Valid NFA
    '''
    states = "{q0, q1, q2, q3, q4}"
    input_symbols = "{a, b}"
    final_states = '{q1, q3}'
    transition_count = 6
    transitions = ['q0, q1, a',
                   'q1, q2, b',
                   'q1, q3,',  # lambda transition
                   'q3, q4, b',
                   'q2, q3, a',
                   "q4, q2, a",
                   'q0, q2, a']
    initial_state = "q0"
    nfa = NFA(states=states,
              input_symbols=input_symbols,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,)
    assert nfa.validate()


def test_NFA_Validation2():
    '''
        Invalid Transition with C symbol
    '''
    states = "{q0, q1, q2, q3, q4}"
    input_symbols = "{a, b}"
    final_states = '{q1, q3}'
    transition_count = 6
    transitions = ['q0, q1, c',
                   'q1, q2, b',
                   'q1, q3,',  # lambda transition
                   'q3, q4, b',
                   'q2, q3, a',
                   "q4, q2, a",
                   'q0, q2, a']
    initial_state = "q0"
    nfa = NFA(states=states,
              input_symbols=input_symbols,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,)
    assert not nfa.validate()


def test_NFA_Validation3():
    '''
        Final States and all states are the same
    '''
    states = "{q0, q1, q2, q3, q4}"
    input_symbols = "{a, b}"
    final_states = '{q0, q1, q2, q3, q4}'
    transition_count = 6
    transitions = ['q0, q1, a',
                   'q1, q2, b',
                   'q1, q3,',  # lambda transition
                   'q3, q4, b',
                   'q2, q3, a',
                   "q4, q2, a",
                   'q0, q2, a']
    initial_state = "q0"
    nfa = NFA(states=states,
              input_symbols=input_symbols,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,)
    assert nfa.validate()


def test_NFA_Validation4():
    '''
        Final State is not in the states
    '''
    states = "{q0, q1, q2, q3, q4}"
    input_symbols = "{a, b}"
    final_states = '{q1, q5}'
    transition_count = 6
    transitions = ['q0, q1, a',
                   'q1, q2, b',
                   'q1, q3,',  # lambda transition
                   'q3, q4, b',
                   'q2, q3, a',
                   "q4, q2, a",
                   'q0, q2, a']
    initial_state = "q0"
    nfa = NFA(states=states,
              input_symbols=input_symbols,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,)
    assert not nfa.validate()
