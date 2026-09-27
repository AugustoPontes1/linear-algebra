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
        return Matrix(
            [
                a + b
                for a, b in zip(row_a, row_b)
            ]
            for row_a, row_b 
            in zip(self.values, other.values)
        )

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
    