import itertools

import numpy as np

from sim.calculations.vector import Vector


class LinearSubspaceRn:

    def __init__(self, name, basis):
        self.name = name
        self.basis = basis
        
        if not basis:
            raise ValueError(
                "Forneça pelo menos um vetor."
            )
        
        dimension = len(basis[0])
        
        if any(
            len(v) != dimension
            for v in basis
        ):
            raise ValueError(
                "Vetores da base precisam "
                "ter a mesma dimensão."
            )
        
        self.ambient_dimension = dimension
    
    def matrix(self):
        return np.column_stack([
            np.array(
                v.values,
                dtype=float,
            )
            for v in self.basis
        ])
    
    @property
    def dimension(self):
        return int(
            np.linalg.matrix_rank(
                self.matrix
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
                    dtype=float
                )
                for v in candidate
            ])