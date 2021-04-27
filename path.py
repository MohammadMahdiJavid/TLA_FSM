class Path:
    def __init__(self, state, curr_label, path):
        self.state = state
        self.label = curr_label
        self.path = path

    def __hash__(self) -> int:
        return hash(self.state) ^ hash(self.label)

    def __eq__(self, o: object) -> bool:
        return self.state == o.state and \
            self.label == o.curr_label

    def __repr__(self):
        return f'''state : {self.state}, label : {self.label}, path : {str(self.path)}'''

    def __str__(self) -> str:
        return self.__repr__()
