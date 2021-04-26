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

    def minify(self):
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
        states_table = new_dfa._create_markable_states_table()
        new_dfa._mark_states_table_first(states_table)
        new_dfa._mark_states_table_second(states_table)
        new_dfa._join_non_marked_states(states_table)
        return new_dfa

    def _compute_reachable_states(self):
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
        reachable_states = self._compute_reachable_states()
        unreachable_states = self.states - reachable_states
        for state in unreachable_states:
            self.states.remove(state)
            del self.transitions[state]

    def _compute_reachable_states(self):
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

    def _create_markable_states_table(self):
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

    def _mark_states_table_first(self, table):
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

    def _mark_states_table_second(self, table):
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
                        reach_0 , reach_1
                    })
                    if combination in table and table[combination]:
                        table[s] = True
                        can_iterate = True
                        break
    def get_unchecked_combinations(self , table):
        unchecked = []
        for f_set in table:
            if not table[f_set]:
                unchecked.append(f_set)
        return unchecked
    def _join_non_marked_states(self, table):
        """Join all overlapping non-marked pairs of states to a new state."""
        non_marked_states = set(self.get_unchecked_combinations(table))
        changed = True
        while changed:
            changed = False
            for s, s2 in itertools.combinations(non_marked_states, 2):
                if s2.isdisjoint(s):
                    continue
                # merge them!
                s3 = s.union(s2)
                # remove the old ones
                non_marked_states.remove(s)
                non_marked_states.remove(s2)
                # add the new one
                non_marked_states.add(s3)
                # set the changed flag
                changed = True
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
                        if transition[symbol] == state:
                            transition[symbol] = stringified
                if state in self.final_states:
                    self.final_states.add(stringified)
                    self.final_states.remove(state)
                if state == self.initial_state:
                    self.initial_state = stringified
