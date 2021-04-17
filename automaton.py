
import abc
from exceptions import *


class Automaton:
    """An abstract base class for all automata, including Turing machines."""

    @ abc.abstractmethod
    def __init__(self):
        """
            Initialize a complete automaton.
        """
        raise NotImplementedError

    @ abc.abstractmethod
    def isValid(self):
        """
            Return True if the FA is in the true format
        """
        raise NotImplementedError

    @ abc.abstractmethod
    def read_input_stepwise(self, input_str):
        """
            Return a generator that yields each step while reading input.
        """
        raise NotImplementedError

    def read_input(self, input_str):
        """
        Check if the given string is accepted by this automaton.

        Return the automaton's final configuration if this string is valid.
        """
        validation_generator = self.read_input_stepwise(input_str)
        for config in validation_generator:
            pass
        return config

    def acceptInput(self, input_str):
        """
            Return True if this automaton accepts the given input.
        """
        try:
            self.read_input(input_str)
            return True
        except RejectionError:
            return False

    def _validate_initial_state(self):
        """Raise an error if the initial state is invalid."""
        if self.initial_state not in self.states:
            raise InvalidStateError(
                '{} is not a valid initial state'.format(self.initial_state))

    def _validate_initial_state_transitions(self):
        """Raise an error if the initial state has no transitions defined."""
        if self.initial_state not in self.transitions:
            raise MissingStateError(
                'initial state {} has no transitions defined'.format(
                    self.initial_state))

    def _validate_final_states(self):
        """Raise an error if any final states are invalid."""
        invalid_states = self.final_states - self.states
        if invalid_states:
            raise InvalidStateError(
                'final states are not valid ({})'.format(
                    ', '.join(invalid_states)))

    def copy(self):
        """Create a deep copy of the automaton."""
        return self.__class__(**vars(self))

    def __eq__(self, other):
        """Check if two automata are equal."""
        return vars(self) == vars(other)
