class StateChange(Exception):
    def __init__(self, state):
        self.state = state

class StateDone(Exception):
    pass
