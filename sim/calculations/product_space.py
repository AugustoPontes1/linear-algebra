

class ProductElement:
    def __init__(self, u, v):
        self.u = u
        self.v = v

    def __add_(self, other):
        return ProductElement(
            self.u + other.u,
            self.v + other.v,
        )

    def __neg__(self):
        return ProductElement(
            -self.u,
            -self.v,
        )

    def __rmul__(self, scalar):
        return ProductElement(
            scalar * self.u,
            scalar * self.v,
        )

    def __eq__(self, other):
        return (
            isinstance(other, ProductElement)
            and self.u == other.u
            and self.v == other.v
        )

    def __repr__(self):
        return (
            f"({self.u}, {self.v})"
        )
