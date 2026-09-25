

class Vector:
    def __init__(self, values):
        self.values = tuple(values)
    
    def __add__(self, other):
        if len(self.values) != len(other.values):
            raise ValueError("Os vetores precisam ter a mesma dimensão.")

        return Vector(
            a + b
            for a, b in zip(self.values, other.values)
        )
    
    def __neg__(self):
        return Vector(-x for x in self.values)

    def __rmul__(self, scalar):
        return Vector(
            scalar * x
            for x in self.values
        )
    
    def __eq__(self, other):
        return self.values == other.values

    def __repr__(self):
        return f"Vector {self.values}"