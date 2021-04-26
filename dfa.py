import os
import graphviz
from fa import FA
from automata.fa.dfa import DFA


class DFA(FA):
    def __init__(self, states, transitions, initial_state, final_states, input_symbols):
        super().__init__(states, transitions,
                         initial_state, final_states, input_symbols)

    def _get_next_current_state(self, current_state, input_symbol):
        """
            Follow the transition for the given input symbol on the current state.

            Raise an error if the transition does not exist.
        """

        return self.transitions[current_state][input_symbol]

    def _check_for_input_rejection(self, current_state):
        """Raise an error if the given config indicates rejected input."""
        # if current_state not in self.final_states:
        # return len(current_state & self.final_states) > 0
        # return
        pass

    def _isAcceptByDFA_stepwise(self, input_str):
        """
            Check if the given string is accepted by this DFA.
            Yield the current configuration of the DFA at each step.
        """
        current_state = self.initial_state
        yield current_state, True

        for input_symbol in input_str:
            if input_symbol in self.transitions[current_state]:
                current_state = next(
                    iter(self.transitions[current_state][input_symbol]))
                yield current_state, True
            else:
                yield current_state, False

        yield current_state, current_state in self.final_states

    def isAcceptByDFA(self, input_str):
        """
            Check if the given string is accepted by this automaton.
            Return the automaton's final configuration if this string is valid.
        """
        validation_generator = self._isAcceptByDFA_stepwise(input_str)
        for last_states, is_valid in validation_generator:
            if not is_valid:
                return last_states, False
        return last_states, True

    def showSchematicDFA(self, filename):
        g = graphviz.Digraph(format='png')
        g.node('fake', style='invisible')
        for state in self.states:
            if state == self.initial_state:
                if state in self.final_states:
                    g.node(state, root='true',
                           shape='doublecircle')
                else:
                    g.node(state, root='true')
            elif state in self.final_states:
                g.node(state, shape='doublecircle')
            else:
                g.node(state)

        g.edge('fake', self.initial_state, style='bold')
        for start in self.transitions:
            for label in self.transitions[start]:
                for dst in self.transitions[start][label]:
                    g.edge(start, dst, label=label)

        DIRECTORY_NAME = "Outputs"
        if not os.path.exists(DIRECTORY_NAME):
            os.makedirs(DIRECTORY_NAME)

        g.render(directory='.\\Outputs\\', view=True,
                 format='png', filename=filename + '.gv')
        g.render(directory='.\\Outputs\\', view=True,
                 format='pdf', filename=filename + '.gv')
