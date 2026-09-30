

class VectorSubspace:
    def __init__(self, parent_space, condition):
        self.parent_space = parent_space
        self.condition = condition
    
    def contains(self, vector):
        return (
            self.parent_space.contains(vector)
            and self.condition(vector)
        )