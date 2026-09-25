class Matrix:
    def __init__(self, values):
        self.values = values
    
    def __add__(self, other):
        return Matrix([
            [
            a + b
            for a, b in zip(row_a, row_b)
            ]
            for row_a, row_b
            in zip(self.values, other.values)
        ])
    
    def __rmul__(self, scalar):
        return Matrix([
            [scalar * x for x in row]
            for row in self.values
        ])
    
    def __neg__(self):
        return Matrix([
            [-x for x in row]
            for row in self.values
        ])
    
    def __eq__(self, other):
        return self.values == other.values
    
    def __repr__(self):
        return f"Matrix({self.values})"