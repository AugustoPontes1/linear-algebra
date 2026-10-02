import math


class Polynomial:
    def __init__(self, *coefficients):
        self.coefficients = tuple(coefficients)
    
    def __add__(self, other):
        if (
            len(self.coefficients)
            != len(other.coefficients)
        ):
            raise ValueError(
                "Polinômios precisam pertencer ao mesmo P_n."
            )

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
        return all(
            math.isclose(
                a,
                b,
                abs_tol=1e-9
            )
            for a, b in zip(
                self.coefficients,
                other.coefficients,
            )
        )

    def __call__(self, x):
        result = 0
        
        for degree, coefficient in enumerate(
            self.coefficients
        ):
            result += (
                coefficient
                * x ** degree
            )
        
        return result
    
    def __repr__(self):
        return (
            f"Polynomial"
            f"{self.coefficients}"
        )