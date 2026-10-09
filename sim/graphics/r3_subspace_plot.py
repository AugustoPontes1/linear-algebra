import matplotlib.pyplot as plt

from matplotlib.widgets import RadioButtons, Slider

from sim.calculations.examples import R3_SPACES
from sim.calculations.vector import Vector
from sim.calculations.utils.r3_utils import draw_subspace


class R3SubspacePlot:
    def __init__(self):
        self.space_name = "Q8 - U"

        self.c1 = 1
        self.c2 = 1

        self.d1 = -1
        self.d2 = 2

        self.scalar = 2

        self.mode = "Soma"

        self.fig = plt.figure(
            figsize=(11, 8)
        )

        self.ax = self.fig.add_subplot(
            111,
            projection="3d",
        )

        plt.subplots_adjust(
            right=0.74,
            bottom=0.28,
        )

        self.create_controls()
        self.update()

    def create_slider(
        self,
        y,
        label,
        initial,
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
            -3,
            3,
            valinit=initial,
            valstep=1,
        )

        slider.on_changed(
            self.on_change
        )

        return slider

    def create_controls(self):
        self.s_c1 = self.create_slider(
            0.20,
            "u₁",
            1,
        )

        self.s_c2 = self.create_slider(
            0.16,
            "u₂",
            1,
        )

        self.s_d1 = self.create_slider(
            0.12,
            "v₁",
            -1,
        )

        self.s_d2 = self.create_slider(
            0.08,
            "v₂",
            2,
        )

        self.s_scalar = self.create_slider(
            0.04,
            "a",
            2,
        )

        ax_space = self.fig.add_axes([
            0.77,
            0.47,
            0.21,
            0.40,
        ])

        self.radio_space = RadioButtons(
            ax_space,
            tuple(R3_SPACES.keys()),
        )

        self.radio_space.on_clicked(
            self.change_space
        )

        ax_mode = self.fig.add_axes([
            0.77,
            0.28,
            0.20,
            0.12,
        ])

        self.radio_mode = RadioButtons(
            ax_mode,
            (
                "Soma",
                "Escalar",
            ),
        )

        self.radio_mode.on_clicked(
            self.change_mode
        )

    def change_space(self, name):
        self.space_name = name
        self.update()

    def change_mode(self, mode):
        self.mode = mode
        self.update()

    def on_change(self, _):
        self.c1 = self.s_c1.val
        self.c2 = self.s_c2.val
        
        self.d1 = self.s_d1.val
        self.d2 = self.s_d2.val
        
        self.scalar = (
            self.s_scalar.val
        )
        
        self.update()
        
    def make_vector(
        self,
        space,
        c1,
        c2,
    ):
        basis = (
            space.independent_basis()
        )
        
        if len(basis) == 1:
            return c1 * basis[0]
        
        return (
            c1 * basis[0]
            + c2 * basis[1]
        )
        
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
        space = R3_SPACES[
            self.space_name
        ]
        
        u = self.make_vector(
            space,
            self.c1,
            self.c2,
        )
        
        v = self.make_vector(
            space,
            self.d1,
            self.d2,
        )
        
        self.ax.clear()
        
        draw_subspace(
            self.ax,
            space,
        )
        
        self.draw_vector(
            u,
            f"u={u.values}",
        )
        
        if self.mode == "Soma":
            result = u + v
            
            self.draw_vector(
                v,
                f"v={v.values}",
            )
            
            self.draw_vector(
                result,
                f"u+v={result.values}",
            )
            
            valid = space.contains(
                result
            )
            
            title = (
                "Fechamento da soma "
                f"u+v ∈ W: {valid}"
            )
        else:
            result = (
                self.scalar * u
            )
            
            self.draw_vector(
                result,
                f"au={result.values}",
            )
            
            valid = space.contains(
                result
            )
            
            title = (
                "Fechamento por escalar\n"
                f"au ∈ W: {valid}"
            )
            
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.ax.set_zlim(-6, 6)
        
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        
        self.ax.set_title(
            f"{self.space_name}\n"
            f"{title}"
        )
        
        self.ax.legend()
        
        self.fig.canvas.draw_idle()
        
    def show(self):
        plt.show()


if __name__ == "__main__":
    R3SubspacePlot().show()
