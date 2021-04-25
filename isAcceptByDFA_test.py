from nfa import NFA
from dfa import DFA


def test_isAcceptByDFA_1():
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
    dfa = nfa.createEquivalentDFA()
    last_states, is_valid = dfa.isAcceptByDFA('a')
    assert is_valid
    last_states, is_valid = dfa.isAcceptByDFA('aba')
    assert is_valid
    last_states, is_valid = dfa.isAcceptByDFA('abaa')
    assert is_valid
    last_states, is_valid = dfa.isAcceptByDFA('abaabaa')
    assert is_valid
    last_states, is_valid = dfa.isAcceptByDFA('ababaa')
    assert is_valid
    last_states, is_valid = dfa.isAcceptByDFA('ababaabaa')
    assert is_valid
    last_states, is_valid = dfa.isAcceptByDFA('ab')
    assert not is_valid
    last_states, is_valid = dfa.isAcceptByDFA('abb')
    assert not is_valid
    last_states, is_valid = dfa.isAcceptByDFA('abab')
    assert not is_valid
    last_states, is_valid = dfa.isAcceptByDFA('abc')
    assert not is_valid
    last_states, is_valid = dfa.isAcceptByDFA('aa')
    assert not is_valid
    last_states, is_valid = dfa.isAcceptByDFA('cabc')
    assert not is_valid
