import math


class Matrix:
    def __init__(self, values):
        if not values:
            raise ValueError("A matriz nao pode ser vazia")

        columns = len(values[0])

        if any(len(row) != columns for row in values):
            raise ValueError("Todas as linhas devem ter o mesmo tamanho.")

        self.values = tuple(
            tuple(row)
            for row in values
        )

    @property
    def shape(self):
        return (
            len(self.values),
            len(self.values[0])
        )

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError(
                "As matrizes precisam ter a mesma dimensao"
            )
        return Matrix([
            [
                a + b
                for a, b in zip(row_a, row_b)
            ]
            for row_a, row_b 
            in zip(self.values, other.values)
        ])

    def __neg__(self):
        return Matrix([
            [-value for value in row]
            for row in self.values
        ])

    def __rmul__(self, scalar):
        return Matrix([
            [scalar * value for value in row]
            for row in self.values
        ])

    def __eq__(self, other):
        return (
            isinstance(other, Matrix)
            and self.values == other.values
        )

    def __repr__(self):
        return f"Matrix({self.values})"
    
    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise ValueError(
                "Dimensões iincompatíveis."
            )
        
        rows = self.shape[0]
        columns = other.shape[1]
        inner = self.shape[1]
        
        return Matrix([
            [
                sum(
                    self.values[i][k]
                    * other.values[k][j]
                    for k in range(inner)
                )
                for j in range(columns)
            ]
            for i in range(rows)
        ])
    
    def determinant(self):
        if self.shape != (2, 2):
            raise NotImplementedError(
                "Por enquanto, determinante apenas 2x2"
            )
        
        a, b = self.values[0]
        c, d = self.values[1]

        return a * d - b * c

    def is_diagonal(self):
        rows, columns = self.shape
        
        if rows != columns:
            return False
        
        for i in range(rows):
            for j in range(columns):
                if (
                   i != j
                   and not math.isclose(
                       self.values[i][j],
                       0,
                       abs_tol=1e-9,
                   )
                ):
                    return False
        
        return True