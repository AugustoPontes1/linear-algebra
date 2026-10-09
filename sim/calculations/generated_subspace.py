from dataclasses import dataclass

import sympy as sp

from sim.calculations.vector import Vector


@dataclass
class SpanSolution:
    belongs: bool
    coefficients: tuple | None
    unique: bool
    parameters: tuple


class GeneratedSubspace:
    def __init__(self, *generators):
        if not generators:
            raise ValueError(
                "Forneça pelo menos um vetor gerador."
            )
        
        dimension = len(generators[0])
        
        if any(
            len(vector) != dimension
            for vector in generators
        ):
            raise ValueError(
                "Todos os vetores devem pertencer "
                "ao mesmo R^n."
            )
            
        self.generators = tuple(generators)
        self.ambient_dimension = dimension
    
    @property
    def matrix(self):
        """
        Coloca os vetores geradores como colunas.
        
        [v1 v2 ... vn]
        """
        
        return sp.Matrix.hstack(
            *[
                sp.Matrix(vector.values)
                for vector in self.generators
            ]
        )
    
    @property
    def dimension(self):
        return self.matrix.rank()
    
    def contains(self, vector):
        if len(vector) != self.ambient_dimension:
            return False
        
        A = self.matrix
        b = sp.Matrix(vector.values)
        
        return A.rank() == A.row_join(b).rank()
    
    def solve_coefficients(self, vector):
        """
        Resolve
        
        a1*v1 + ... + an*vn = vector
        """
        
        if len(vector) != self.ambient_dimension:
            return SpanSolution(
                False,
                None,
                False,
                (),
            )
        
        A = self.matrix
        b = sp.Matrix(vector.values)
        
        solution_set = sp.linsolve(
            (A, b)
        )

        if solution_set == sp.EmptySet:
            return SpanSolution(
                False,
                None,
                False,
                (),
            )
        
        solution = tuple(
            next(iter(solution_set))
        )
        
        parameters = sorted(
            {
                symbol
                for expression in solution
                for symbol
                in expression.free_symbols
            },
            key=str
        )
        
        return SpanSolution(
            belongs=True,
            coefficients=solution,
            unique= not parameters,
            parameters=tuple(parameters),
        )
    
    def independent_generators(self):
        columns = self.matrix.columnspace()
        
        return [
            Vector(
                *tuple(column)
            )
            for column in columns
        ]
    
    def equals(self, other):
        if(
            self.ambient_dimension
            != other.ambient_dimension
        ):
            return False
        
        first_inside = all(
            other.contains(vector)
            for vector in self.generators
        )
        
        second_inside = all(
            self.contains(vector)
            for vector in other.generators
        )
        
        return (
            first_inside
            and second_inside
        )
    
    def augmented_matrix(self, vector):
        return self.matrix.row_join(
            sp.Matrix(vector.values)
        )
