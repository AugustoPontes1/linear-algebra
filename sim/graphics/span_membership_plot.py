import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import Slider

from sim.calculations.generated_subspace import GeneratedSubspace
from sim.calculations.vector import Vector


class SpanMembershipPlot:
    def __init__(self):
        self.v1 = Vector(1, 1, 1)
        self.v2 = Vector(1, 2, 3)
        self.v3 = Vector(2, -1, 1)

        self.space = GeneratedSubspace(
            self.v1,
            self.v2,
            self.v3,
        )

        self.target = Vector(
            1,
            -2,
            5,
        )

        self.fig = plt.figure(
            figsize=(11, 8)
        )

        self.ax = self.fig.add_subplot(
            111,
            projection="3d"
        )

        plt.subplots_adjust(
            right=0.72,
            bottom=0.25,
        )

        self.create_controls()

        self.info_ax = self.fig.add_axes([
            0.74,
            0.08,
            0.24,
            0.80,
        ])

        self.info_ax.axis("off")

        self.update()

    def create_slider(
        self,
        y,
        label,
        value,
    ):
        ax = self.fig.add_axes([
            0.08,
            y,
            0.55,
            0.025,
        ])

        slider = Slider(
            ax,
            label,
            -8,
            8,
            valinit=value,
            valstep=1,
        )

        slider.on_changed(
            self.on_change
        )

        return slider

    def create_controls(self):
        self.sx = self.create_slider(
            0.17,
            "x",
            1,
        )

        self.sy = self.create_slider(
            0.12,
            "y",
            -2,
        )

        self.sz = self.create_slider(
            0.07,
            "z",
            5,
        )

    def on_change(self, _):
        self.target = Vector(
            self.sx.val,
            self.sy.val,
            self.sz.val,
        )

        self.update()

    def draw_vector(
        self,
        vector,
        label,
    ):

        x, y, z = vector.values

        self.ax.quiver(
            0,
            0,
            0,
            x,
            y,
            z,
            label=label,
        )

    def draw_span(self):
        basis = (
            self.space
            .independent_generators()
        )

        dimension = self.space.dimension

        if dimension == 1:
            b = np.array(
                basis[0].values,
                dtype=float,
            )

            t = np.linspace(
                -5,
                5,
                100,
            )

            points = np.outer(
                t,
                b,
            )

            self.ax.plot(
                points[:, 0],
                points[:, 1],
                points[:, 2],
            )
        elif dimension == 2:
            b1 = np.array(
                basis[1].values,
                dtype=float,
            )

            b2 = np.array(
                basis[1].values,
                dtype=float,
            )

            s = np.linspace(-4, 4, 15)
            t = np.linspace(-4, 4, 15)

            S, T = np.meshgrid(
                s,
                t,
            )

            X = (
                S * b1[0]
                + T * b2[0]
            )

            Y = (
                S * b1[1]
                + T * b2[1]
            )

            Z = (
                S * b1[2]
                + T * b2[2]
            )

            self.ax.plot_surface(
                X,
                Y,
                Z,
                alpha=0.20,
            )

    def update(self):
        self.ax.clear()

        self.info_ax.clear()
        self.info_ax.axis("off")

        self.draw_span()

        self.draw_vector(
            self.v1,
            f"v1={self.v1.values}",        
        )

        self.draw_vector(
            self.v2,
            f"v2={self.v2.values}",
        )

        self.draw_vector(
            self.v3,
            f"v3={self.v3.values}",
        )

        self.draw_vector(
            self.target,
            f"p={self.target.values}",
        )

        solution = (
            self.space
            .solve_coefficients(
                self.target
            )
        )

        if solution.belongs:
            text = (
                "PERTENCE AO SPAN\n\n"
                f"p = {self.target.values}\n\n"
                f"dim(W) = "
                f"{self.space.dimension}\n\n"
                f"Coeficientes:\n"
                f"{solution.coefficients}\n\n"
                f"Solução única: "
                f"{solution.unique}"                
            )

        else:
            text = (
                "NÃO PERTENCE AO SPAN\n\n"
                f"p = {self.target.values}\n\n"
                "O sistema linear não "
                "possui solução."            
            )

        self.info_ax.text(
            0,
            1,
            text,
            va="top",
            fontsize=11,
        )

        self.ax.set_xlim(-8, 8)
        self.ax.set_ylim(-8, 8)
        self.ax.set_zlim(-8, 8)

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")

        self.ax.set_title(
            "Subespaço gerado / combinação linear"
        )

        self.ax.legend()

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()


if __name__ == "__main__":
    SpanMembershipPlot().show()
