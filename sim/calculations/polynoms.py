

class Polynomial:
    def __init__(self, *coefficients):
        self.coefficients = tuple(coefficients)
    
    def __add__(self, other):
        return Polynomial(
            *(
                a + b
                for a, b
                in zip(
                    self.coefficients,
                    other.coefficients
                )
            )   
        )
    
    def __rmul__(self, scalar):
        return Polynomial(
            *(scalar * a for a in self.coefficients)
        )
    
    def __neg__(self):
        return Polynomial(
            *(-a for a in self.coefficients)
        )
    
    def __eq__(self, other):
        return self.coefficients == other.coefficients