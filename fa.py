from automaton import Automaton
import re


class FA (Automaton):
    def __init__(self, states, transitions, initial_state, final_states, input_symbols):
        self.states, self.transitions, self.initial_state, self.final_states, self.input_symbols = FA.parse_input(
            states, transitions, final_states, input_symbols)

    @classmethod
    def remove_paranthesis(cls, string):
        chars = ['(', ')', '{', '}', '[', ']']
        for char in chars:
            string = string.strip(char)
        return string

    @classmethod
    def remove_space_comma(cls, string):
        strings = string.split(',')
        return set(string.strip(' ') for string in strings)

    @classmethod
    def parse_transitions(cls, transitions):
        result = {}
        for transition in transitions:
            start, target, label = transition.split(',')
            target = target.strip(' ')
            if not label is "":
                label = label.strip()
            result[start] = result.get(start, {})
            if label in result[start]:
                result[start][label].add(target)
            else:
                result[start][label] = {target}
        return result

    @classmethod
    def parse_input(cls, states, transitions, final_states, input_symbols):
        states = cls.remove_space_comma(cls.remove_paranthesis(states))
        input_symbols = cls.remove_space_comma(cls.remove_paranthesis(
            input_symbols))
        final_states = cls.remove_space_comma(
            cls.remove_paranthesis(final_states))
        transitions = cls.parse_transitions(transitions)
        return states, transitions, 'q0', final_states, input_symbols
