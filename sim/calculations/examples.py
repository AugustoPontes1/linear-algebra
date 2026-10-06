from sim.calculations.linear_subspace import LinearSubspaceRn
from sim.calculations.vector import Vector


Q8_U = LinearSubspaceRn(
    "U",
    [
        Vector(1, 0, 1),
        Vector(0, 1, 0),
    ],
)

Q8_V = LinearSubspaceRn(
    "V",
    [
        Vector(0, 0, 1),
    ],
)

Q8_W = LinearSubspaceRn(
    "W",
    [
        Vector(1, 0, -1),
        Vector(0, 1, -1),
    ],
)

Q9_W1 = LinearSubspaceRn(
    "W1",
    [
        Vector(1, -1, 0),
        Vector(0, 0, 1),
    ],
)

Q9_W2 = LinearSubspaceRn(
    "W2",
    [
        Vector(1, -1, 0),
        Vector(0, 2, 1),
    ],
)

Q10_W1 = LinearSubspaceRn(
    "W1",
    [
        Vector(1, 1, 0),
        Vector(0, 0, 1),
    ],
)

Q10_W2 = LinearSubspaceRn(
    "W2",
    [
        Vector(1, 0, 1),
        Vector(0, 1, 1),
    ]
)

R3_SPACES = {
    "Q8 - U": Q8_U,
    "Q8 - V": Q8_V,
    "Q8 - W": Q8_W,

    "Q9 - W1": Q9_W1,
    "Q9 - W2": Q9_W2,

    "Q10 - W1": Q10_W1,
    "Q10 - W2": Q10_W2,    
}