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
    assert not nfa.isAcceptByNFA("")
    assert nfa.isAcceptByNFA("abb")
    assert not nfa.isAcceptByNFA("abaa")
    assert nfa.isAcceptByNFA("abab")
    assert nfa.isAcceptByNFA("aaaaaa")
    new_dfa = nfa.createEquivalentDFA()
    # nfa.showSchematicNFA("nfa-diagram")
    assert not new_dfa.isAcceptByDFA("")
    assert new_dfa.isAcceptByDFA("abb")
    assert not new_dfa.isAcceptByDFA("abaa")
    assert new_dfa.isAcceptByDFA("abab")
    assert new_dfa.isAcceptByDFA("aaaaaa")
    minimized_dfa = new_dfa.MakeSimpleDFA()
    # new_dfa.showSchematicDFA("dfa-diagram")
#     regex = nfa.findRegExp()

