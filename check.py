from nfa import NFA
from dfa import DFA
# from automata.fa.dfa import DFA
states = "{q0, q1, q2, q3, q4}"
#  "{, q1, q2}
# input_symbols = "{a, b}"
# final_states = '{q1, q3}'
# transition_count = 6
# transitions = ['q0, q1, a',
#                'q1, q2, b',
#                'q1, q3,',  # lambda transition
#                'q3, q4, b',
#                'q2, q3, a',
#                "q4, q2, a"]
# initial_state = "q0"
# nfa = NFA(states=states,
#           input_symbols=input_symbols,
#           transitions=transitions,
#           initial_state=initial_state,
#           final_states=final_states,)

# dfa = nfa.createEquivalentDFA()
# dfa.minify()

states = "{q0, q1, q2, q3, q4, q5}"
#  "{, q1, q2}
input_symbols = "{0, 1}"
final_states = '{q3, q5}'
transition_count = 6
transitions = ['q0, q1, 0',
               'q1, q0, 0',
               'q1, q3, 1',  # lambda transition
               'q0, q3, 1',
               'q2, q1, 0',
               'q2, q4, 1',
               "q4, q3, 0",
               "q4, q3, 1",
               "q3, q5, 0",
               "q3, q5, 1",
               "q5, q5, 0",
               "q5, q5, 1"]
initial_state = "q0"
dfa = DFA(states=states,
          input_symbols=input_symbols,
          transitions=transitions,
          initial_state=initial_state,
          final_states=final_states)
new_dfa = dfa.minify()

# @staticmethod
    # def _stringify_states(states):
        # """Stringify the given set of states as a single state name."""
        # return '{{{}}}'.format(','.join(sorted(states)))


states = "{q0, q1, q2, q3, q4}"
#  "{, q1, q2}
input_symbols = "{a, b}"
final_states = '{q4}'
transition_count = 8
transitions = ['q0, q1, a',
               'q0, q3, b',
               'q1, q2, b',
               'q1, q4, a',  # lambda transition
               'q3, q2, a',
               'q3, q4, b',
               "q4, q4, a",
               "q4, q4, b"]
initial_state = "q0"
# hw1


states = "{q0, q1, q2, q3, q4, q5}"
#  "{, q1, q2}
input_symbols = "{a, b}"
final_states = '{q1, q2}'
transition_count = 7
transitions = ['q0, q1, a',
               'q0, q2, a',
               'q2, q5, b',
               'q5, q2, a',  # lambda transition
               'q1, q3, a',
               'q3, q4, a',
               "q4, q1, b"]
initial_state = "q0"
# hw1

states = "{q0, q1, q2, q3, q4, q5}"
#  "{, q1, q2}
input_symbols = "{a, b}"
final_states = '{q3, q5}'
transition_count = 7
transitions = ['q0, q1, a',
               'q0, q2, a',
               'q2, q1, b',
               'q1, q3, b',
               'q1, q4, b',
               'q3, q1, b',
               "q4, q5, a"]
initial_state = "q0"
# hw2

states = "{q0, q1, q2}"
#  "{, q1, q2}
input_symbols = "{a, b, c}"
final_states = '{q2}'
transition_count = 6
transitions = ['q0, q1, a',
               'q1, q0, b',
               'q1, q1, a',
               'q1, q2, c',
               'q2, q2, c']
initial_state = "q0"
# hw2

states = "{q0, q1, q2, q3, q4}"
#  "{, q1, q2}
input_symbols = "{a, b}"
final_states = '{q4}'
transition_count = 6
transitions = ['q0, q1,',
               'q0, q2,',
               'q2, q3, a',
               'q1, q1, b',
               'q1, q4, a',
               'q3, q4, b'
               ]
initial_state = "q0"

# chapter 3_2 last page

