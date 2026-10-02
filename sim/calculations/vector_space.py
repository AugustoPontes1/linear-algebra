from numbers import Real

from sim.calculations.vector import Vector
from sim.calculations.rules import VectorSpaceRules


class RealVectorSpace:
    def __init__(self, dimension):
        if dimension <= 0:
            raise ValueError(
                "A dimensão precisa ser positiva."
            )

        self.dimension = dimension

    def contains(self, vector):
        return(
            isinstance(vector, Vector)
            and len(vector) == self.dimension
            and all(
                isinstance(x, (int, Real))
                for x in vector.values
            )
        )

    def zero(self):
        return Vector(*([0] * self.dimension))
    
    def __repr__(self):
        return f"R^{self.dimension}"    


class VectorSpaceValidator:
    @staticmethod
    def validate(space, u, v, w, a, b):
        return {
            "closure_sum":
                VectorSpaceRules.closure_sum(space, u, v),
            
            "closure_scalar":
                VectorSpaceRules.closure_scalar(space, a, u),
            
            "associative_sum":
                VectorSpaceRules.associative_sum(u, v, w),
            
            "commutative_sum":
                VectorSpaceRules.commutative_sum(u,v),
            
            "null_vector":
                VectorSpaceRules.null_vector(space, u),
            
            "opposite_vector":
                VectorSpaceRules.opposite_vector(space, u),
            
            "distributive_vector":
                VectorSpaceRules.distributive_vector(a, u, v),
            
            "distributive_scalar":
                VectorSpaceRules.distributive_scalars(a, b, v),
            
            "associative_scalars":
                VectorSpaceRules.associative_scalars(a, b, v),
            
            "scalar_identity":
                VectorSpaceRules.scalar_identity(v),
        }
