import matplotlib.pyplot as plt

from matplotlib.widgets import RadioButtons, Slider

from sim.calculations.examples import R3_SPACES
from sim.calculations.vector import Vector
from sim.calculations.utils.r3_utils import draw_subspace


class LinearSubspacePlot:
    def __init__(self):
        self.space_name = "Q8 - U"
        self.mode = "Combinação Linear"
        
        self.a = 1
        self.b = 1
        self.c = 0
        
        self.x = 1
        self.y = 1
        self.z = 1
        
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
            bottom=0.32,
            top=0.90,
        )
        
        self.create_controls()
        self.update()
    
    def create_slider(
        self,
        y,
        label,
        minimum,
        maximum,
        initial,
        step=1,
    ):
        axis = self.fig.add_axes([
            0.10,
            y,0.52,
            0.025,
        ])
        
        slider = Slider(
            axis,
            label,
            minimum,
            maximum,
            valinit=initial,
            valstep=step
        )
        
        slider.on_changed(
            self.on_change
        )
        
        return slider
    
    def create_controls(self):
        self.slider_a = self.create_slider(
            0.24,
            "a",
            -4,
            4,
            1,
        )
        
        self.slider_b = self.create_slider(
            0.20,
            "b",
            -4,
            4,
            1
        )
        
        self.slider_c = self.create_slider(
            0.16,
            "c",
            -4,
            4,
            0,
        )
        
        self.slider_x = self.create_slider(
            0.11,
            "x",
            -5,
            5,
            1,
        )
        
        self.slider_y = self.create_slider(
            0.07,
            "y",
            -5,
            5,
            1
        )
        
        self.slider_z = self.create_slider(
            0.03,
            "z",
            -5,
            5,
            1,
        )
        
        space_axis = self.fig.add_axes([
            0.75,
            0.48,
            0.23,
            0.40
        ])

        self.space_radio = RadioButtons(
            space_axis,
            tuple(R3_SPACES.keys())
        )
        
        self.space_radio.on_clicked(
            self.change_space
        )
        
        mode_axis = self.fig.add_axes([
            0.75,
            0.29,
            0.23,
            0.12,
        ])
        
        self.mode_radio = RadioButtons(
            mode_axis,
            (
                "Combinação linear",
                "Pertinência",
            )
        )
        
        self.mode_radio.on_clicked(
            self.change_mode
        )
        
        self.info_ax = self.fig.add_axes([
            0.75,
            0.03,
            0.23,
            0.20,
        ])
        
        self.info_ax.axis("off")
    
    def on_change(self, _):
        self.a = self.slider_a.val
        self.b = self.slider_b.val
        self.c = self.slider_c.val
        
        self.x = self.slider_x.val
        self.y = self.slider_y.val
        self.z = self.slider_z.val
        
        self.update()
    
    def change_space(self, name):
        self.space_name = name
        self.update()
    
    def change_mode(self, mode):
        self.mode = mode
        self.update()
    
    def draw_vector(
        self,
        vector,
        label,
        origin
    ):
        x, y, z = vector.values
        
        self.ax.quiver(
            origin[0].
            origin[1],
            origin[2],
            x,
            y,
            z,
            label=label
        )
    
    def draw_basis(self, space):
        basis = space.independent_basis()
        
        for index, vector in enumerate(
            basis,
            start=1
        ):
            self.draw_vector(
                vector,
                f"b{index}={vector.values}"
            )
    
    def get_linear_combination(
        self,
        space,
    ):
        basis = space.independent_basis()
        
        coefficients = [
            self.a,
            self.b,
            self.c
        ]
        
        coefficients = coefficients[
            :len(basis)
        ]
        
        return (
            space.vector_from_coefficients(
                *coefficients
            )
        )
    
    def plot_linear_combination(
        self,
        space,
    ):
        result = self.get_linear_combination(
            space
        )
        
        self.draw_vector(
            result,
            f"combinação={result.values}",
        )
        
        belongs = space.contains(
            result
        )
        
        basis = space.independent_basis()
        
        coefficients = [
            self.a,
            self.b,
            self.c
        ][:len(basis)]
        
        expression_parts = []
        
        for coefficient, vector in zip(
            coefficients,
            basis,
        ):
            expression_parts.append(
                f"{coefficient:g}{vector.values}"
            )
        
        expression = " + ".join(
            expression_parts
        )
        
        self.info_ax.text(
            0,
            1,
            (
                "COMBINAÇÃO LINEAR\n\n"
                f"{expression}\n\n"
                f"Resultado:\n"
                f"{result.values}\n\n"
                f"Pertence a W: {belongs}"
            ),
            va="top",
            fontsize=10,
        )
        
        self.ax.set_title(
            f"{self.space_name}\n"
            f"Combinação linear dos vetores da base\n"
            f"Resultado ∈ W: {belongs}"
        )
    
    def plot_membership(
        self,
        space,
    ):
        candidate = Vector(
            self.x,
            self.y,
            self.z,
        )
        
        belongs = space.contains(
            candidate
        )
        
        self.draw_vector(
            candidate,
            f"p={candidate.values}",
        )
        
        self.info_ax.text(
            0,
            1,
            (
                "TESTE DE PERTINÊNCIA\n\n"
                f"p = {candidate.values}\n\n"
                f"p ∈ {space.name}?\n\n"
                f"{belongs}"
            ),
            va="top",
            fontsize=11,
        )
        
        self.ax.set_title(
            f"{self.space_name}\n"
            f"p = {candidate.values}\n"
            f"p ∈ W: {belongs}"
        )
    
    def update(self):
        space = R3_SPACES[
            self.space_name
        ]
        
        self.ax.clear()
        
        self.info_ax.clear()
        self.info_ax.axis("off")
        
        draw_subspace(
            self.ax,
            space,
            limit=4,
        )
        
        self.draw_basis(
            space
        )
        
        if self.mode == "Combinação Linear":
            self.plot_linear_combination(
                space
            )
        elif self.mode == "Pertinência":
            self.plot_membership(
                space
            )
        
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.ax.set_zlim(-6, 6)
        
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        
        self.ax.legend(
            loc="upper left"
        )
        
        self.fig.canvas.draw_idle()
        
    def show(self):
        plt.show()
    

if __name__ == "__main__":
    plot = LinearSubspacePlot()
    plot.show()