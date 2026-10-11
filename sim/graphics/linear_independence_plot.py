import matplotlib.pyplot as plt

from matplotlib.widgets import Slider

from sim.calculations.linear_independence import LinearIndependence
from sim.calculations.vector import Vector


class LinearIndependencePlot:

    def __init__(self):
        self.v1 = Vector(1, 1, 1)
        self.v2 = Vector(1, 2, 3)
        self.v3 = Vector(2, -1, 1)

        self.fig = plt.figure(
            figsize=(12, 8)
        )

        self.ax = self.fig.add_subplot(
            111,
            projection="3d",
        )

        plt.subplots_adjust(
            left=0.06,
            right=0.72,
            bottom=0.37,
        )

        self.sliders = []

        self.create_controls()

        self.info_ax = self.fig.add_axes([
            0.75,
            0.08,
            0.23,
            0.80,
        ])

        self.info_ax.axis("off")

        self.update()

    def create_slider(
        self,
        x,
        y,
        label,
        value,
    ):
        ax = self.fig.add_axes([
            x,
            y,
            0.23,
            0.022,
        ])

        slider = Slider(
            ax,
            label,
            -5,
            5,
            valinit=value,
            valstep=1,
        )

        slider.on_changed(
            self.on_change
        )

        self.sliders.append(
            slider
        )

        return slider

    def create_controls(self):
        ys = (
            0.27,
            0.23,
            0.19,
        )

        # v1
        self.v1x = self.create_slider(
            0.06, ys[0], "v1x", 1
        )

        self.v1y = self.create_slider(
            0.06, ys[1], "v1y", 1
        )

        self.v1z = self.create_slider(
            0.06, ys[2], "v1z", 1
        )

        # v2
        self.v2x = self.create_slider(
            0.31, ys[0], "v2x", 1
        )

        self.v2y = self.create_slider(
            0.31, ys[1], "v2y", 2
        )

        self.v2z = self.create_slider(
            0.31, ys[2], "v2z", 3
        )

        # v3
        self.v3x = self.create_slider(
            0.56, ys[0], "v3x", 2
        )

        self.v3y = self.create_slider(
            0.56, ys[1], "v3y", -1
        )

        self.v3z = self.create_slider(
            0.56, ys[2], "v3z", 1
        )

    def on_change(self, _):
        self.v1 = Vector(
            self.v1x.val,
            self.v1y.val,
            self.v1z.val,
        )

        self.v2 = Vector(
            self.v2x.val,
            self.v2y.val,
            self.v2z.val,
        )

        self.v3 = Vector(
            self.v3x.val,
            self.v3y.val,
            self.v3z.val,
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

    def update(self):
        self.ax.clear()

        self.info_ax.clear()
        self.info_ax.axis("off")

        analyzer = LinearIndependence(
            self.v1,
            self.v2,
            self.v3,
        )

        result = analyzer.analyze()

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

        state = (
            "LI"
            if result.independent
            else "LD"
        )

        text = (
            f"RESULTADO: {state}\n\n"

            f"Posto = {result.rank}\n"
            f"Nº vetores = "
            f"{result.vector_count}\n\n"

            f"det(A) = "
            f"{result.determinant}\n\n"
        )

        if (
            result.dependence_relation
            is not None
        ):
            text += (
                "Relação não trivial:\n\n"
                f"{result.dependence_relation}\n\n"
                "Esses coeficientes "
                "produzem zero."
            )
        else:
            text += (
                "Somente a solução "
                "trivial produz zero."
            )

        self.info_ax.text(
            0,
            1,
            text,
            va="top",
            fontsize=11,
        )

        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.ax.set_zlim(-6, 6)

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")

        self.ax.set_title(
            f"Dependência / independência linear\n"
            f"{state}"
        )

        self.ax.legend()

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()


if __name__ == "__main__":
    LinearIndependencePlot().show()