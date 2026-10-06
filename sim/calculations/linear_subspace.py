import itertools

import numpy as np

from sim.calculations.vector import Vector


class LinearSubspaceRn:

    def __init__(self, name, basis):
        self.name = name
        self.basis = basis

        if not basis:
            raise ValueError(
            "Forneca pelo menos um vetor"
        )

        dimension = len(basis[0])

        if any(
            len(v) != dimension
            for v in basis
        ):
            raise ValueError(
                "Vetores da base precisam "
                "ter a mesma dimensao"
            )

        self.ambient_dimension = dimension

    def matrix(self):
        return np.column_stack([
            np.array(
                v.values,
                dtype=float
            )
            for v in self.basis
        ])

    @property
    def dimension(self):
        return int(
            np.linalg.matrix_rank(
                self.matrix()
            )
        )

    def contains(self, vector):
        B = self.matrix()

        extended = np.column_stack([
            B,
            np.array(
                vector.values,
                dtype=float,
            ),
        ])

        return (
            np.linalg.matrix_rank(B)
            ==
            np.linalg.matrix_rank(
                extended
            )
        )

    def independent_basis(self):
        selected = []

        for vector in self.basis:
            candidate = (
                selected
                + [vector]
            )

            matrix = np.column_stack([
                np.array(
                    v.values,
                    dtype=float,
                )
                for v in candidate
            ])

            if (
                np.linalg.matrix_rank(
                    matrix
                )
                > len(selected)
            ):
                selected.append(
                    vector
                )

        return selected

    def vector_from_coefficients(
            self,
            *coefficients,
    ):
        basis = self.independent_basis()

        if len(coefficients) != len(basis):
            raise ValueError(
                "Número incorreto de coeficientes."
            )

        result = Vector(
            *(
                [0]
                * self.ambient_dimension
            )
        )

        for coefficient, vector in zip(
            coefficients,
            basis,
        ):
            result = (
                result
                + coefficient * vector
            )

        return result

    def sum(self, other):
        return LinearSubspaceRn(
            f"{self.name}+{other.name}",
            self.basis + other.basis
        )

    def intersection_dimension(
            self,
            other,
    ):
        sum_space = self.sum(
            other
        )

        return (
            self.dimension
            + other.dimension
            - sum_space.dimension
        )

    def is_direct_sum_with(
            self,
            other
    ):
        return (
            self.intersection_dimension(
                other
            )
            == 0
        )

    def sample_vectors(self):
        basis = self.independent_basis()

        vectors = []

        for coefficients in itertools.product(
            (-1, 0, 1),
            repeat=len(basis),
        ):
            if all(
                c == 0
                for c in coefficients
            ):
                continue

            vectors.append(
                self.vector_from_coefficients(
                    *coefficients
                )
            )

        return vectors

    def union_counterexample(
        self,
        other
    ):
        for u in self.sample_vectors():
            for v in other.sample_vectors():
                result = u + v

                if(
                    not self.contains(result)
                    and not other.contais(result)
                ):
                    return (
                        u,
                        v,
                        result,
                    )

        return None