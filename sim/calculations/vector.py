import math
from numbers import Real


class Vector:
    def __init__(self, *values):
        if not values:
            raise ValueError(
                "O vetor precisa ter pelo menos uma componente."
            )
        
        if not all(isinstance(x, Real) for x in values):
            raise TypeError(
                "Todas as compontes precisam ser números reais."
            )

        self.values = tuple(values)

    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented

        if len(self.values) != len(other.values):
            raise ValueError("Os vetores precisam ter a mesma dimensão.")

        return Vector(
            *(
                a + b
                for a, b in zip(self.values, other.values)
            )
        )
    
    def __neg__(self):
        return Vector(
            *(-x for x in self.values)
        )

    def __rmul__(self, scalar):
        return Vector(
            *(
                scalar * x
                for x in self.values
        )
        )
    
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return False
        
        if len(self) != len(other):
            return False
        
        return all(
            math.isclose(a, b, abs_tol=1e-9)
            for a, b in zip(
                self.values,
                other.values
            )           
        )

    def __len__(self):
        return len(self.values)

    def __repr__(self):
        return f"Vector {self.values}"