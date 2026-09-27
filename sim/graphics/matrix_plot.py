import matplotlib.pyplot as plt 
from matplotlib.widgets import Slider, RadioButtons
from sim.calculations.matrix import Matrix


class MatrixSpacePlot:
    def __init__(self):
        self.A = Matrix(
            [1, 2],
            [3, 4],
        )

        self.B = Matrix([
            [2, -1],
            [0, 3]
        ])

        self.scalar = 2

        self.mode = "Soma"

        self.fig, self.axes = plt.subplots(
            2,
            2,
            figsize=(10, 8)
        )

        plt.subplots_adjust(
            left=0.08,
            right=0.78,
            bottom=0.40,
            top=0.90,
            wspace=0.35,
            hspace=0.35,
        )

        self.create_controls()
        self.update()

    def create_controls(self):
        ...