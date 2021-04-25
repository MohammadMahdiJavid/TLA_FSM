from nfa import NFA


def test_accept_string():
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
    last_states, is_valid = nfa.isAcceptByNFA('')
    assert not is_valid
    last_states, is_valid = nfa.isAcceptByNFA('a')
    assert is_valid
    last_states, is_valid = nfa.isAcceptByNFA('aba')
    assert is_valid
    last_states, is_valid = nfa.isAcceptByNFA('abaa')
    assert is_valid
    last_states, is_valid = nfa.isAcceptByNFA('abaabaa')
    assert is_valid
    last_states, is_valid = nfa.isAcceptByNFA('ababaa')
    assert is_valid
    last_states, is_valid = nfa.isAcceptByNFA('ababaabaa')
    assert is_valid
    last_states, is_valid = nfa.isAcceptByNFA('ab')
    assert not is_valid
    last_states, is_valid = nfa.isAcceptByNFA('abb')
    assert not is_valid
    last_states, is_valid = nfa.isAcceptByNFA('abab')
    assert not is_valid
    last_states, is_valid = nfa.isAcceptByNFA('abc')
    assert not is_valid
    last_states, is_valid = nfa.isAcceptByNFA('aa')
    assert not is_valid
    last_states, is_valid = nfa.isAcceptByNFA('cabc')
    assert not is_valid
