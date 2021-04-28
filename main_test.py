from nfa import NFA

def test_check_whole():
    states = "{q0, q1, q2, q3, q4, q5, q6}"
    input_symbols = "{a, b}"
    final_states = '{q1, q3, q6}'
    transition_count = 0
    transitions = [
            "q0,q1,a",
            "q1,q1,b",
            "q1,q2,",
            "q2,q3,a",
            "q3,q2,a",
            "q3,q4,b",
            "q2,q5,b",
            "q5,q6,a",
            "q6,q1,b"]
    initial_state = "q0"
    nfa = NFA(states=states,
              input_symbols=input_symbols,
              transitions=transitions,
              initial_state=initial_state,
              final_states=final_states,)
    assert not nfa.isAcceptByNFA("")[1]
    assert nfa.isAcceptByNFA("abb")[1]
    assert not nfa.isAcceptByNFA("abaa")[1]
    assert nfa.isAcceptByNFA("abab")[1]
    assert nfa.isAcceptByNFA("aaaaaa")[1]
    new_dfa = nfa.createEquivalentDFA()
    # nfa.showSchematicNFA("nfa-diagram")
    assert not new_dfa.isAcceptByDFA("")[1]
    assert new_dfa.isAcceptByDFA("abb")[1]
    assert not new_dfa.isAcceptByDFA("abaa")[1]
    assert new_dfa.isAcceptByDFA("abab")[1]
    assert new_dfa.isAcceptByDFA("aaaaaa")[1]
    minimized_dfa = new_dfa.MakeSimpleDFA()
    # new_dfa.showSchematicDFA("dfa-diagram")
    regex = nfa.findRegExp()

