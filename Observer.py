

class Observer():
    def __init__(self):
        self.label = []
        self.action = []
    def add_action(self, name, func):
        self.label.append(name)
        self.action.append(func)

    def execute(self, item):
        """Connect the labels of the menu and its function."""
        for i in range(len(self.action)):
            if item.labelstr == self.label[i]:
                self.action[i]()
