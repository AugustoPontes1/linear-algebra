from dataclasses import dataclass
from typing import Callable

from sim.calculations.vector import Vector


@dataclass
class VectorOperations:
    name: str
    add: Callable
    scalar_mul: Callable
    zero: Vector | None
    opposite: Callable | None

def normal_add(u, v):
    return u + v

def normal_scalar(a, u):
    return a * u

def normal_opposite(u):
    return -u

def question_1_add(u, v):
    x1, x2 = u.values
    y1, y2 = v.values
    
    return Vector(
        x1 + y1,
        0,
    )
    
def question_2a_add(u, v):
    x1, x2 = u.values
    y1, y2 = v.values
    
    return Vector(
        x1,
        x2 + y2,
    )

def question_2b_scalar(a, u):
    x1, x2 = u.values
    
    return Vector(
        a * x1,
        0,
    )

def question_2c_add(u, v):
    x1, x2 = u.values
    y1, y2 = v.values
    
    return Vector(
        x1 + y1 + 1,
        x2 + y2
    )

def question_2c_opposite(u):
    x, y = u.values
    
    return Vector(
        -x - 2,
        -y,
    )

PRESETS = {
    "Usual": VectorOperations(
        name="Usual",
        add=normal_add,
        scalar_mul=normal_scalar,
        zero=Vector(0, 0),
        opposite=normal_opposite,
    ),

    "Questão 1": VectorOperations(
        name="Questão 1",
        add=question_1_add,
        scalar_mul=normal_scalar,
        zero=None,
        opposite=None,
    ),

    "Questão 2(a)": VectorOperations(
        name="Questão 2(a)",
        add=question_2a_add,
        scalar_mul=normal_scalar,
        zero=None,
        opposite=None,
    ),

    "Questão 2(b)": VectorOperations(
        name="Questão 2(b)",
        add=normal_add,
        scalar_mul=question_2b_scalar,
        zero=Vector(0, 0),
        opposite=normal_opposite,
    ),

    "Questão 2(c)": VectorOperations(
        name="Questão 2(c)",
        add=question_2c_add,
        scalar_mul=normal_scalar,
        zero=Vector(-1, 0),
        opposite=question_2c_opposite,
    ),
}