from automata.fa.dfa import DFA
from nfa import NFA


class Main:

    @staticmethod
    def run_nfa(obj: NFA):
        inp = input("which function to run? ").lower()
        while inp != "Exit":
            if inp == "isAcceptByNFA".lower():
                obj.isAcceptByNFA()
            elif inp == "createEquivalentDFA".lower():
                obj.createEquivalentDFA()
            elif inp == "findRegExp".lower():
                obj.findRegExp()
            elif inp == "showSchematicNFA":
                obj.showSchematicNFA()
            inp = input("which function to run? ").lower()

    def run_dfa(obj: DFA):
        inp = input("which function to run? ").lower()
        while inp != "Exit":
            if inp == "isAcceptByDFA".lower():
                obj.isAcceptByDFA()
            elif inp == "makeSimpleDFA".lower():
                obj.makeSimpleDFA()
            elif inp == "showSchematicDFA":
                obj.showSchematicDFA()
            inp = input("which function to run? ").lower()

    @staticmethod
    def nfa_initialize():
        states = input("states? (e.g. {q0, q1})? ")
        input_symbols = input("language? (e.g. {a, b})? ")
        transition_count = int(input("transition count? "))
        transitions = []
        for i in range(transition_count):
            transitions.append(input("transition? (e.g. q0,q1,a)? "))
        final_states = input("language? (e.g. {a, b})? ")
        nfa = NFA(

        )

    @staticmethod
    def dfa_initialize():
        states = input("states? (e.g. {q0, q1})? ")
        input_symbols = input("language? (e.g. {a, b})? ")
        transition_count = int(input("transition count? "))
        transitions = []
        for i in range(transition_count):
            transitions.append(input("transition? (e.g. q0,q1,a)? "))
        final_states = input("language? (e.g. {a, b})? ")

    @staticmethod
    def getInputs():
        inp = input("NFA or DFA? ").lower()
        while inp != 'nfa' or inp != 'dfa':
            if inp == 'nfa':
                Main.nfa_initialize()
            elif inp == 'dfa':
                Main.dfa_initialize()
            inp = input("NFA or DFA? ").lower()


def main():
    Main.getInputs()


if __name__ == '__main__':
    main()
