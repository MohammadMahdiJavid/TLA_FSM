import os
import graphviz
from fa import FA
from automata.fa.dfa import DFA
import queue
import itertools


class DFA(FA):
    def __init__(self, states, transitions, initial_state, final_states, input_symbols):
        super().__init__(states, transitions,
                         initial_state, final_states, input_symbols)

    def _get_next_current_state(self, current_state, input_symbol):
        """
            Follow the transition for the given input symbol on the current state.

            Raise an error if the transition does not exist.
        """

        return next(iter(self.transitions[current_state][input_symbol]))


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

    @staticmethod
    def _parse_set(string_set):
        return "{" + ", ".join(string_set) + "}"

    @staticmethod
    def _parse_transitions(dfa_transitions):
        result = []
        for start, paths in dfa_transitions.items():
            for label, target in paths.items():
                result.append(", ".join([start, next(iter(target)), label]))
        return result

    @staticmethod
    def _stringify_states(states):
        """Stringify the given set of states as a single state name."""
        return '{{{}}}'.format(','.join(sorted(states)))

    def MakeSimpleDFA(self):
        """
        Create a minimal DFA which accepts the same inputs as this DFA.

        First, non-reachable states are removed.
        Then, similiar states are merged.
        Its algorithm is based on Myphill-Nerode theorem
        https://www.tutorialspoint.com/automata_theory/dfa_minimization.htm
        """
        new_dfa = DFA(self._parse_set(self.states), self._parse_transitions(self.transitions), str(
            self.initial_state), self._parse_set(self.final_states), self._parse_set(self.input_symbols))
        new_dfa._remove_unreachable_states()
        states_table = new_dfa.initialize_states_table()
        new_dfa.check_final_and_non_finals(states_table)
        new_dfa.check_remained_mergable_tuple(states_table)
        new_dfa.union_unchecked_marked_states(states_table)
        return new_dfa

    def retrieve_reachable_states(self):
        """Compute the states which are reachable from the initial state."""
        reachable_states = set()
        states_to_check = queue.Queue()
        states_checked = set()
        states_to_check.put(self.initial_state)
        while not states_to_check.empty():
            state = states_to_check.get()
            reachable_states.add(state)
            for symbol, dst_state in self.transitions[state].items():
                if next(iter(dst_state)) not in states_checked:
                    states_to_check.put(next(iter(dst_state)))
            states_checked.add(state)
        return reachable_states

    def _remove_unreachable_states(self):
        """Remove states which are not reachable from the initial state."""
        reachable_states = self.retrieve_reachable_states()
        unreachable_states = self.states - reachable_states
        for state in unreachable_states:
            self.states.remove(state)
            del self.transitions[state]


    def initialize_states_table(self):
        """
        Create a "markable table" with all combinatations of two states.

        This is a dict with frozensets of states as keys and `False` as value.
        """
        states_list = list(self.states)
        table = {}
        for i in range(len(states_list)):
            for j in range(i+1, len(states_list)):
                table[frozenset((states_list[j], states_list[i]))] = False
        return table

    def check_final_and_non_finals(self, table):
        """Mark pairs of states if one is final and one is not."""
        for s in table:
            x = list(s)
            if (x[0] in self.final_states and x[1] not in self.final_states) \
                    or (x[1] in self.final_states and x[0] not in self.final_states):
                table[s] = True
        # for s in table.keys():
        #     if any((x in self.final_states for x in s)):
        #         if any((x not in self.final_states for x in s)):
        #             table[s] = True

    def check_remained_mergable_tuple(self, table):
        """
        Mark additional state pairs.

        A non-marked pair of two states q, q_ will be marked
        if there is an input_symbol a for which the pair
        transition(q, a), transition(q_, a) is marked.
        """
        can_iterate = True
        while can_iterate:
            can_iterate = False
            for s in self.get_unchecked_combinations(table):
                x = tuple(s)
                for symbol in self.input_symbols:
                    reach_0 = self._get_next_current_state(x[0], symbol)
                    reach_1 = self._get_next_current_state(x[1], symbol)
                    combination = frozenset({
                        reach_0, reach_1
                    })
                    if combination in table and table[combination]:
                        table[s] = True
                        can_iterate = True
                        break

    def get_unchecked_combinations(self, table):
        unchecked = []
        for f_set in table:
            if not table[f_set]:
                unchecked.append(f_set)
        return unchecked

    def union_unchecked_marked_states(self, table):
        """Join all overlapping non-marked pairs of states to a new state."""
        non_marked_states = set(self.get_unchecked_combinations(table))
        can_iterate = True
        while can_iterate:
            can_iterate = False
            for f_union, s_union in itertools.combinations(non_marked_states, 2):
                # check if they are seperated
                if s_union.isdisjoint(f_union):
                    continue
                # merge them!
                unioned_f_s = f_union.union(s_union)
                # remove the old ones
                non_marked_states.remove(f_union)
                non_marked_states.remove(s_union)
                # add the new one
                non_marked_states.add(unioned_f_s)
                # set the changed flag
                can_iterate = True
                break
        # finally adjust the DFA
        for s in non_marked_states:
            stringified = DFA._stringify_states(s)
            # add the new state
            self.states.add(stringified)
            # copy the transitions from one of the states
            self.transitions[stringified] = self.transitions[tuple(s)[0]]
            # replace all occurrences of the old states
            for state in s:
                self.states.remove(state)
                del self.transitions[state]
                for src_state, transition in self.transitions.items():
                    for symbol in transition.keys():
                        if next(iter(transition[symbol])) == state:
                            transition[symbol] = {stringified}
                if state in self.final_states:
                    self.final_states.add(stringified)
                    self.final_states.remove(state)
                if state == self.initial_state:
                    self.initial_state = stringified
