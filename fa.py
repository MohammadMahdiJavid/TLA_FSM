from automaton import Automaton
import re


class FA (Automaton):
    def __init__(self, states, transitions, initial_state, final_states, input_symbols):
        self.states, self.transitions, self.initial_state, self.final_states, self.input_symbols = FA.parse_input(
            states, transitions, initial_state, final_states, input_symbols)

    @classmethod
    def remove_paranthesis(cls, string):
        chars = ['(', ')', '{', '}', '[', ']']
        # for char in chars:
        #     string = string.strip(char)
        return string[1:len(string) - 1]

    @classmethod
    def remove_space_comma(cls, string):
        strings = string.split(',')
        state_set = set()
        extends = []
        if "{" or "}" in string:
            l = []
            start = False
            for s in strings[::]:
                s_no_space = s.strip()
                if "{" in s:
                    start = True
                if start:
                    l.append(s_no_space)
                    strings.remove(s)
                if "}" in s:
                    start = False
                    extends.append(", ".join(l))
                    l.clear()
        strings.extend(extends)
        return set(string.strip(' ') for string in strings)

    @classmethod
    def remove_space_comma_transitions(cls, string):
        strings = string.split(',')
        state_set = set()
        extends = []
        if "{" or "}" in string:
            l = []
            start = False
            for s in strings[::]:
                s_no_space = s.strip()
                if "{" in s:
                    start = True
                if start:
                    l.append(s_no_space)
                    strings.remove(s)
                if "}" in s:
                    start = False
                    extends.append(", ".join(l))
                    l.clear()
        strings.extend(extends)
        return [string.strip(' ') for string in strings]

    @classmethod
    def parse_transitions(cls, transitions):
        result = {}
        for transition in transitions:
            idx_start = transition.find("{")
            if idx_start != -1:
                idx_start2 = transition.find("{", idx_start + 1)
                if idx_start != 0 and idx_start2 == -1:
                    # start nabashe, faghat target bashe
                    start, label, target = cls.remove_space_comma_transitions(
                        transition)
                if idx_start == 0 and idx_start2 == -1:
                    # start bashe, target nabashe
                    target, label, start = cls.remove_space_comma_transitions(
                        transition)
                if idx_start == 0 and idx_start2 != -1:
                    # start bashe, target bashe
                    label, start, target = cls.remove_space_comma_transitions(
                        transition)
            else:
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
    def parse_input(cls, states, transitions, initial_state, final_states, input_symbols):
        states = cls.remove_space_comma(cls.remove_paranthesis(states))
        input_symbols = cls.remove_space_comma(cls.remove_paranthesis(
            input_symbols))
        final_states = cls.remove_space_comma(
            cls.remove_paranthesis(final_states))
        transitions = cls.parse_transitions(transitions)
        return states, transitions, initial_state, final_states, input_symbols
