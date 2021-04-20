from os import stat
from dfa import DFA
from fa import FA
from automaton import Automaton
import exceptions
import itertools
import queue


class NFA (FA):
    '''
        Non-Deterministic Finite Automata
    '''

    def __init__(self, states, transitions, initial_state, final_states, input_symbols):
        super().__init__(states, transitions,
                         initial_state, final_states, input_symbols)

    def _validate_transition_invalid_symbols(self, start_state, paths):
        for input_symbol in paths.keys():
            if input_symbol not in self.input_symbols and input_symbol != '':
                # raise exceptions.InvalidSymbolError(
                #     'state {} has invalid transition symbol {}'.format(
                #         start_state, input_symbol))
                return False
        return True

    def _validate_transition_end_states(self, start_state, paths):
        """
            Raise an error if transition end states are invalid.
        """
        for end_states in paths.values():
            for end_state in end_states:
                if end_state not in self.states:
                    # raise exceptions.InvalidStateError(
                    #     'end state {} for transition on {} is '
                    #     'not valid'.format(end_state, start_state))
                    return False
        return True

    def validate(self):
        """
            Return True if this NFA is internally consistent.
        """
        for start_state, paths in self.transitions.items():
            if not self._validate_transition_invalid_symbols(start_state, paths):
                return False
            if not self._validate_transition_end_states(start_state, paths):
                return False
        if not self._validate_initial_state():
            return False
        if not self._validate_initial_state_transitions():
            return False
        if not self._validate_final_states():
            return False
        return True

    def _get_lambda_closure(self, start_state):
        """
            Return the lambda closure for the given state.

            The lambda closure of a state q is the set containing q, along with
            every state that can be reached from q by following only lambda
            transitions.
        """
        stack = []
        encountered_states = set()
        stack.append(start_state)

        while stack:
            state = stack.pop()
            if state not in encountered_states:
                encountered_states.add(state)
                if '' in self.transitions[state]:
                    stack.extend(self.transitions[state][''])

        return encountered_states

    def _get_next_current_states(self, current_states, input_symbol):
        """
            Return the next set of current states given the current set.
        """
        next_current_states = set()

        for current_state in current_states:
            symbol_end_states = self.transitions[current_state].get(
                input_symbol)
            if not symbol_end_states:
                continue
            for end_state in symbol_end_states:
                next_current_states.update(
                    self._get_lambda_closure(end_state))

        return next_current_states

    def isAcceptByNFA_stepwise(self, input_str):
        """
            Check if the given string is accepted by this NFA.
            Yield the current configuration of the NFA at each step.
        """
        current_states = self._get_lambda_closure(self.initial_state)
        yield current_states, True

        for input_symbol in input_str:
            current_states = self._get_next_current_states(
                current_states, input_symbol)
            yield current_states, True

        if not (current_states & self.final_states):
            print('the NFA stopped on all non-final states ({})'.format(
                ', '.join(current_states)))
            yield current_states, False

    def isAcceptByNFA(self, input_str):
        """
            Check if the given string is accepted by this automaton.
            Return the automaton's final configuration if this string is valid.
        """
        validation_generator = self.isAcceptByNFA_stepwise(input_str)
        for last_states, is_valid in validation_generator:
            if not is_valid:
                return last_states, False
        return last_states, True

    @classmethod
    def _add_nfa_states_from_queue(cls, nfa, current_states,
                                   current_state_name, dfa_states,
                                   dfa_transitions, dfa_final_states):
        """Add NFA states to DFA as it is constructed from NFA."""
        dfa_states.add(current_state_name)
        dfa_transitions[current_state_name] = {}
        if (current_states & nfa.final_states):
            dfa_final_states.add(current_state_name)

    @staticmethod
    def _stringify_states(states):
        """Stringify the given set of states as a single state name."""
        if not states:
            return "$"
        elif len(states) == 1:
            return next(iter(states))
        else:
            return "{" + ", ".join(sorted(states)) + "}"

    @classmethod
    def _enqueue_next_nfa_current_states(cls, nfa, current_states,
                                         current_state_name, state_queue,
                                         dfa_transitions):
        """Enqueue the next set of current states for the generated DFA."""
        for input_symbol in nfa.input_symbols:
            next_current_states = nfa._get_next_current_states(
                current_states, input_symbol)
            dfa_transitions[current_state_name][input_symbol] = (
                cls._stringify_states(next_current_states))
            state_queue.put(next_current_states)

    @staticmethod
    def _parse_set(string_set):
        '''
            {'q3', 'q1, q3', 'q2, q3'} -> "{q3, {q1, q3}, {q2, q3}}"
        '''
        # result = set()
        # for string in string_set:
        #     if "," in string:
        #         result.add("{" + string + "}")
        #     else:
        #         result.add(string)
        return "{" + ", ".join(string_set) + "}"

    @staticmethod
    def _parse_transitions(dfa_transitions):
        result = []
        for start, paths in dfa_transitions.items():
            for label, target in paths.items():
                result.append(", ".join([start, target, label]))
        return result

    @classmethod
    def _parse_create_DFA(cls, dfa_states, dfa_symbols, dfa_transitions, dfa_initial_state, dfa_final_states):
        dfa_states = cls._parse_set(dfa_states)
        dfa_symbols = cls._parse_set(dfa_symbols)
        dfa_final_states = cls._parse_set(dfa_final_states)
        dfa_transitions = cls._parse_transitions(dfa_transitions)
        return DFA(states=dfa_states, input_symbols=dfa_symbols,
                   transitions=dfa_transitions, initial_state=dfa_initial_state,
                   final_states=dfa_final_states)

    @classmethod
    def createEquivalentDFA(cls, nfa):
        """
            Initialize this DFA as one equivalent to the given NFA.
            Trap states : $
        """
        dfa_states = set()
        dfa_symbols = nfa.input_symbols
        dfa_transitions = {}
        # equivalent DFA states states
        nfa_initial_states = nfa._get_lambda_closure(nfa.initial_state)
        dfa_initial_state = cls._stringify_states(nfa_initial_states)
        dfa_final_states = set()

        state_queue = queue.Queue()
        state_queue.put(nfa_initial_states)
        while not state_queue.empty():
            current_states = state_queue.get()
            current_state_name = cls._stringify_states(current_states)
            # We've been here before and nothing should have changed.
            if current_state_name in dfa_states:
                continue
            cls._add_nfa_states_from_queue(nfa, current_states,
                                           current_state_name, dfa_states,
                                           dfa_transitions, dfa_final_states)
            cls._enqueue_next_nfa_current_states(
                nfa, current_states, current_state_name, state_queue,
                dfa_transitions)
        cls._parse_create_DFA(
            dfa_states, dfa_symbols, dfa_transitions, dfa_initial_state, dfa_final_states)
        return
