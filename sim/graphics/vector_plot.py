import matplotlib.pyplot as plt

from matplotlib.widgets import Slider, RadioButtons

from sim.calculations.vector import Vector


class VectorSpacePlot:
    def __init__(self):
        self.u = Vector(2, 1)
        self.v = Vector(1, 3)
        self.scalar = 2

        self.mode = "Soma"

        self.fig, self.ax = plt.subplots(figsize=(10, 7))

        # Deixa espaço para os controles
        plt.subplots_adjust(
            left=0.10,
            bottom=0.35,
            right=0.78
        )

        self.create_controls()
        self.update()

    def create_controls(self):
        # Sliders
        ax_ux = self.fig.add_axes([0.10, 0.25, 0.55, 0.03])
        ax_uy = self.fig.add_axes([0.10, 0.21, 0.55, 0.03])

        ax_vx = self.fig.add_axes([0.10, 0.16, 0.55, 0.03])
        ax_vy = self.fig.add_axes([0.10, 0.12, 0.55, 0.03])

        ax_scalar = self.fig.add_axes([0.10, 0.06, 0.55, 0.03])

        self.slider_ux = Slider(
            ax_ux,
            "uₓ",
            -5,
            5,
            valinit=2,
            valstep=1
        )

        self.slider_uy = Slider(
            ax_uy,
            "uᵧ",
            -5,
            5,
            valinit=1,
            valstep=1
        )

        self.slider_vx = Slider(
            ax_vx,
            "vₓ",
            -5,
            5,
            valinit=1,
            valstep=1
        )

        self.slider_vy = Slider(
            ax_vy,
            "vᵧ",
            -5,
            5,
            valinit=3,
            valstep=1
        )

        self.slider_scalar = Slider(
            ax_scalar,
            "a",
            -3,
            3,
            valinit=2,
            valstep=1
        )

        for slider in [
            self.slider_ux,
            self.slider_uy,
            self.slider_vx,
            self.slider_vy,
            self.slider_scalar,
        ]:
            slider.on_changed(self.on_change)

        # Seleção da regra
        ax_radio = self.fig.add_axes(
            [0.81, 0.55, 0.17, 0.25]
        )

        self.radio = RadioButtons(
            ax_radio,
            (
                "Soma",
                "Distributiva",
                "Oposto"
            )
        )

        self.radio.on_clicked(self.change_mode)

    def on_change(self, _):
        self.u = Vector(
            self.slider_ux.val,
            self.slider_uy.val
        )

        self.v = Vector(
            self.slider_vx.val,
            self.slider_vy.val
        )

        self.scalar = self.slider_scalar.val

        self.update()

    def change_mode(self, mode):
        self.mode = mode
        self.update()

    def draw_vector(
        self,
        vector,
        label,
        origin=(0, 0),
    ):
        x, y = vector.values

        self.ax.quiver(
            origin[0],
            origin[1],
            x,
            y,
            angles="xy",
            scale_units="xy",
            scale=1,
            label=label
        )

        self.ax.text(
            origin[0] + x,
            origin[1] + y,
            f"  {label}"
        )

    def setup_axis(self):
        self.ax.clear()

        self.ax.axhline(0)
        self.ax.axvline(0)

        self.ax.set_xlim(-12, 12)
        self.ax.set_ylim(-12, 12)

        self.ax.set_aspect("equal")

        self.ax.grid(True)

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

    def update(self):
        self.setup_axis()

        if self.mode == "Soma":
            self.plot_sum()

        elif self.mode == "Distributiva":
            self.plot_distributive()

        elif self.mode == "Oposto":
            self.plot_opposite()

        self.ax.legend()

        self.fig.canvas.draw_idle()

    def plot_sum(self):
        result = self.u + self.v

        self.draw_vector(
            self.u,
            f"u = {self.u.values}"
        )

        self.draw_vector(
            self.v,
            f"v = {self.v.values}"
        )

        self.draw_vector(
            result,
            f"u + v = {result.values}"
        )

        self.ax.set_title(
            "Soma de vetores / Comutatividade\n"
            f"u + v = {result.values}"
        )

    def plot_distributive(self):
        left = self.scalar * (self.u + self.v)

        right = (
            self.scalar * self.u
            + self.scalar * self.v
        )

        self.draw_vector(
            self.u,
            f"u = {self.u.values}"
        )

        self.draw_vector(
            self.v,
            f"v = {self.v.values}"
        )

        self.draw_vector(
            left,
            f"a(u+v) = {left.values}"
        )

        self.ax.set_title(
            "Distributividade\n"
            "a(u + v) = au + av\n"
            f"{left.values} = {right.values}"
        )

    def plot_opposite(self):
        opposite = -self.u
        zero = self.u + opposite

        self.draw_vector(
            self.u,
            f"u = {self.u.values}"
        )

        self.draw_vector(
            opposite,
            f"-u = {opposite.values}"
        )

        self.ax.set_title(
            "Vetor oposto e vetor nulo\n"
            f"u + (-u) = {zero.values}"
        )

    def show(self):
        plt.show()


if __name__ == "__main__":
    plot = VectorSpacePlot()
    plot.show()