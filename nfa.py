import os
import graphviz
from PySimpleAutomata import automata_IO
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

    def _get_lambda(self, start_state):
        stack = []
        encountered_states = set()
        stack.append(start_state)

        while stack:
            state = stack.pop()
            if state not in encountered_states:
                encountered_states.add(state)
                if not state in self.transitions:
                    continue
                if '' in self.transitions[state]:
                    stack.extend(self.transitions[state][''])

        return encountered_states

    def _get_next_current_states(self, current_states, input_symbol):
        next_current_states = set()

        for current_state in current_states:
            if not current_state in self.transitions:
                continue
            symbol_end_states = self.transitions[current_state].get(
                input_symbol)
            if not symbol_end_states:
                continue
            for end_state in symbol_end_states:
                next_current_states.update(
                    self._get_lambda(end_state))

        return next_current_states

    def _isAcceptByNFA_stepwise(self, input_str):
        current_states = self._get_lambda(self.initial_state)
        yield current_states, True

        for input_symbol in input_str:
            current_states = self._get_next_current_states(
                current_states, input_symbol)
            yield current_states, len(current_states) > 0

        if not (current_states & self.final_states):
            print('the NFA stopped on all non-final states ({})'.format(
                ', '.join(current_states)))
            yield current_states, False

    def isAcceptByNFA(self, input_str):
        validation_generator = self._isAcceptByNFA_stepwise(input_str)
        for last_states, is_valid in validation_generator:
            if not is_valid:
                return False
        return True

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
    def convert_NFA_to_DFA(cls, nfa):
        """
            Initialize this DFA as one equivalent to the given NFA.
            Trap states : $
        """
        dfa_states = set()
        dfa_symbols = nfa.input_symbols
        dfa_transitions = {}
        # equivalent DFA states states
        nfa_initial_states = nfa._get_lambda(nfa.initial_state)
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
        return cls._parse_create_DFA(
            dfa_states, dfa_symbols, dfa_transitions, dfa_initial_state, dfa_final_states)

    def createEquivalentDFA(self):
        return NFA.convert_NFA_to_DFA(self)

    def showSchematicNFA(self):
        g = graphviz.Digraph(format='png')

        fakes = []
        initial_states = {self.initial_state}
        for i in range(len(initial_states)):
            fakes.append('fake' + str(i))
            g.node('fake' + str(i), style='invisible')

        for state in self.states:
            if state in initial_states:
                if state in self.final_states:
                    g.node(str(state), root='true',
                           shape='doublecircle')
                else:
                    g.node(str(state), root='true')
            elif state in self.final_states:
                g.node(str(state), shape='doublecircle')
            else:
                g.node(str(state))

        for initial_state in initial_states:
            g.edge(fakes.pop(), str(initial_state), style='bold')

        for start in self.transitions:
            for label in self.transitions[start]:
                for dst in self.transitions[start][label]:
                    g.edge(start, dst, label if label else "??")

        DIRECTORY_NAME = "Outputs"
        if not os.path.exists(DIRECTORY_NAME):
            os.makedirs(DIRECTORY_NAME)
        filename = max(os.listdir(DIRECTORY_NAME))
        filename = filename.split('.')[0]
        filename = int(filename.split('file')[1]) + 1
        filename = f'file{filename}'

        g.render(directory='.\\Outputs\\', view=True,
                 format='png', filename=filename + '.gv')
        g.render(directory='.\\Outputs\\', view=True,
                 format='pdf', filename=filename + '.gv')

    def IsAcceptByNFA(self, input_str):
        return self.isAcceptByNFA(input_str)

    def _get_next_current_states_path(self, current_states, input_symbol):
        """
            Return the next set of current states given the current set.
        """
        result = set()

        for current_state in current_states:
            next_current_states = set()
            if not current_state.state in self.transitions:
                continue
            symbol_end_states = self.transitions[current_state.state].get(
                input_symbol)
            if not symbol_end_states:
                continue
            for end_state in symbol_end_states:
                next_current_states.update(self._get_lambda(end_state))

            for next in next_current_states:
                l = current_state.path[::]
                l.append(input_symbol)
                result.add(Path(next, input_symbol, l))

        return result

    def _clean_path(self, path):
        pass

    def _add_final(self, result, state):
        result.append("".join(self._clean_path(state.path)) + "*")
        if state.state in self.transitions:
            for label in self.transitions[state.state]:
                for dst in self.transitions[state.state][label]:
                    if state.state == dst:
                        result.append(f"{label}*")

    def findRegExp(self):
        new_initial = False
        for start in self.transitions:  # in-degree 0
            for label, dst in self.transitions[start].items():
                if self.initial_state in dst:
                    new_initial = True
                    break
        if new_initial:
            start_name = 'NEWS'
            self.transitions[start_name] = {"": {self.initial_state}}
            self.initial_state = start_name
            self.states.add(start_name)
        new_final = True
        if len(self.final_states) == 1:  # final state ye done bashe
            if not next(iter(self.final_states)) in self.transitions:  # out-degree 0
                new_final = False
        if new_final:
            for final_state in self.final_states:
                new_final_name = 'NEWF'
                if self.transitions[final_state].get(""):
                    self.transitions[final_state][""].add(new_final_name)
                else:
                    self.transitions[final_state][""] = {new_final_name}
            self.states.add(new_final_name)
            self.final_states = {new_final_name}
        self.state_removal()
        # self.showSchematicNFA()
        key = next(iter(self.transitions.keys()))
        final = set([next(iter(val))
                     for val in self.transitions[key].values() if len(val) != 0]).pop()
        label_final = self._get_final_label(final, key)
        self.transitions[key] = {label_final: {final}}
        # self.showSchematicNFA()

    def _get_final_label(self, final, key):
        result = []
        for label in self.transitions[key]:
            if final in self.transitions[key][label]:
                result.append(f'({label})')
        return " + ".join(result)

    def get_incoming_edges(self, middle_state):
        states = set()
        try :
            for start in self.transitions:
                for alphabet in self.transitions[start]:
                    # middle state tosh nabod
                    if not middle_state in self.transitions[start][alphabet]:
                        continue
                    if start == middle_state:  # self loop
                        continue
                    states.add((start, alphabet))
        except:
            pass
        return states

    def get_outgoing_edges(self, middle_state):
        states = set()
        try :
            for alphabet in self.transitions[middle_state]:
                for dst in self.transitions[middle_state][alphabet]:
                    if dst != middle_state:
                        states.add((dst, alphabet))
        except:
            pass
        return states

    def delete_all_related_to_middle_state(self, middle_state):
        for state in self.transitions:
            for alphaet, neighbors in self.transitions[state].items():
                if middle_state in neighbors:
                    neighbors.remove(middle_state)

    def state_removal(self):
        middle_state = self.pick_non_final_initial_state()
        # self.pick_non_final_initial_state()
        while middle_state:
            '''
                1- self-loop
            '''
            for income in self.get_incoming_edges(middle_state):  # income : (state, label)
                # outgo : (state, label)
                for outgo in self.get_outgoing_edges(middle_state):
                    self.traverese_income_to_outgo(middle_state, income, outgo)
                    # return answer how to go from income to outgo
            self.states.remove(middle_state)
            try :
                del self.transitions[middle_state]
            except :
                pass
            self.delete_all_related_to_middle_state(middle_state)
            middle_state = self.pick_non_final_initial_state()

    def pick_non_final_initial_state(self):
        if len(self.states) < 3:
            return ""
        for state in self.states:
            if state in self.final_states:
                continue
            if state == self.initial_state:
                continue
            return state

    def get_self_loop_string(self, state):
        alphabets = set()
        for label, dst in self.transitions[state].items():
            if state in dst:
                alphabets.add(label)
        return "" if len(alphabets) == 0 else \
            f"({alphabets.pop()})*" if len(alphabets) == 1 else \
            f"({ ' + '.join(alphabets)})*"

    def traverese_income_to_outgo(self, middle_state, income, outgo):
        loop_inside = self.get_self_loop_string(middle_state)
        new_connected_label = f"{income[1]}{loop_inside}{outgo[1]}"
        start_state = self.transitions[income[0]]
        if new_connected_label in start_state:
            start_state[new_connected_label].add(outgo[0])
        else:
            start_state[new_connected_label] = {outgo[0]}
