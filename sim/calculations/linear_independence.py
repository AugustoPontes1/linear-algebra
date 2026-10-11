from dataclasses import dataclass

import sympy as sp

from sim.calculations.vector import Vector


@dataclass
class IndependenceResult:
    independent: bool
    rank: int
    vector_count: int
    ambient_dimension: int
    dependence_relation: tuple | None
    determinant: object | None


class LinearIndependence:
    def __init__(self, *vectors):
        if not vectors:
            raise ValueError(
                "Forneça pelo menos um vetor."
            )

        dimension = len(vectors[0])

        if any(
            len(vector) != dimension
            for vector in vectors
        ):
            raise ValueError(
                "Todos os vetores devem ter "
                "a mesma dimensão."                
            )

        self.vectors = tuple(vectors)
        self.ambient_dimension = dimension

    @property
    def matrix(self):
        """"
        Vetores como colunas.

        A = [v1 v2 ... vn]
        """

        return sp.Matrix.hstack(
            *[
                sp.Matrix(vector.values)
                for vector in self.vectors
            ]
        )

    @property
    def rank(self):
        return self.matrix.rank()

    def is_independent(self):
        return (
            self.rank
            == len(self.vectors)
        )

    def nullspace(self):
        return self.matrix.nullspace()

    def dependence_relation(self):
        """ 
        Se for LD, devolve um conjunto
        nao trivial de coeficientes:

        a1*v1 + ... + an*vn = 0
        """

        nullspace = self.nullspace()

        if not nullspace:
            return None

        relation = nullspace[0]

        return tuple(
            sp.simplify(value)
            for value in relation
        )

    def determinant(self):
        matrix = self.matrix

        if matrix.rows != matrix.cols:
            return None

        return sp.simplify(
            matrix.det()
        )

    def contains_zero_vector(self):
        return any(
            all(
                value == 0
                for value in vector.valiues
            )
            for vector in self.vectors
        )

    def analyze(self):
        return IndependenceResult(
            independent=self.is_independent(),
            rank=self.rank,
            vector_count=len(self.vectors),
            ambient_dimension=(
                self.ambient_dimension
            ),
            dependence_relation=(
                self.dependence_relation()
            ),
            determinant=self.determinant(),
        )