
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

    def _validate_initial_state(self):
        """Raise an error if the initial state is invalid."""
        return self.initial_state in self.states

    def _validate_initial_state_transitions(self):
        """Raise an error if the initial state has no transitions defined."""

        return self.initial_state in self.transitions

    def _validate_final_states(self):
        """
            Raise an error if any final states are invalid.
        """
        return not len(self.final_states - self.states) > 0

    def __eq__(self, other):
        """Check if two automata are equal."""
        return vars(self) == vars(other)

    def copy(self):
        """Create a deep copy of the automaton."""
        return self.__class__(**vars(self))
