from .automaton import Automaton
import re


class FA (Automaton):
    def __init__(self, states, transitions, initial_states, final_states, input_symbs):
        self.states = FA.parse_input(
            states, transitions, initial_states, final_states, input_symbs)
        # self.states = states.copy()
        # self.initial_states = initial_states.copy()
        # self.final_states = final_states.copy()
        # self.input_symbs = input_symbs.copy()

    @classmethod
    def remove_paranthesis(string):
        chars = ['(', ')', '{', '}', '[', ']']
        for char in chars:
            string = string.strip(char)
        return string

    @classmethod
    def parse_input(cls, states, transitions, initial_states, final_states, input_symbs):
        states = re.findall("[a-zA-Z0-9]")
