import math

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.widgets import RadioButtons, Slider

from sim.calculations.vector import Vector
from sim.calculations.vector_space import RealVectorSpace
from sim.calculations.sub_space import VectorSubspace


class SubspacePlot:
    def __init__(self):
        self.r2 = RealVectorSpace(2)
        
        # General equation:
        #
        # y = mx + c
        #
        # m -> angular coeficient
        # c -> displacement
        self.sets = {
            "y = 2x": {
                "m": 2,
                "c": 0,
            },
            "y = -x": {
                "m": -1,
                "c": 0,
            },
            "y = 2x + 1": {
                "m": 2,
                "c": 1
            }
        }
        
        self.current_set_name = "y = 2x"
        
        self.mode = "Soma"
        
        self.ux = 1
        self.vx = 2
        
        self.a = 2
        self.b = -1
        
        self.fig, self.ax = plt.subplots(
            figsize=(11, 8)
        )
        
        plt.subplots_adjust(
            left=0.08,
            right=0.72,
            bottom=0.32,
            top=0.90,
        )
        
        self.create_controls()
        
        self.update()
    
    # --------------------------------------------------
    # Actual Subspace
    # --------------------------------------------------
    
    def get_current_parameters(self):
        data = self.sets[
            self.current_set_name
        ]
        
        return data["m"], data["c"]
    
    def make_subspace(self):
        m, c = self.get_current_parameters()
        
        return VectorSubspace(
            self.r2,
            lambda v: math.isclose(
                v.values[1],
                m * v.values[0] + c,
                abs_tol=1e-9
            ),
        )
    
    def make_vector(self, x):
        """
        Automatically creates an element
        that belongs to the current set
        
        if W: y = 2x and x = 3:
        (3, 6)
        """
        
        m, c = self.get_current_parameters()
        
        y = m * x + c
        
        return Vector(x, y)

    # --------------------------------------------------
    # Interface
    # --------------------------------------------------    

    def create_controls(self):
        # u_x
        ax_ux = self.fig.add_axes([
            0.10,
            0.23,
            0.55,
            0.03,
        ])
        
        self.slider_ux = Slider(
            ax_ux,
            "ux",
            -4,
            4,
            valinit=self.ux,
            valstep=1,
        )
        
        # v_x
        ax_vx = self.fig.add_axes([
            0.10,
            0.18,
            0.55,
            0.03
        ])
        
        self.slider_vx = Slider(
            ax_vx,
            "vx",
            -4,
            4,
            valinit=self.vx,
            valstep=1,
        )
        
        # a
        ax_a = self.fig.add_axes([
            0.10,
            0.12,
            0.55,
            0.03,
        ])
        
        self.slider_a = Slider(
            ax_a,
            "a",
            -3,
            3,
            valinit=self.a,
            valstep=0.5,
        )
        
        # b
        ax_b = self.fig.add_axes([
            0.10,
            0.07,
            0.55,
            0.03,
        ])
        
        self.slider_b = Slider(
            ax_b,
            "b",
            -3,
            3,
            valinit=self.b,
            valstep=0.5,
        )
        
        for slider in (
            self.slider_ux,
            self.slider_vx,
            self.slider_a,
            self.slider_b,
        ):
            slider.on_changed(
                self.on_change
            )
        
        # Set selection
        ax_set = self.fig.add_axes([
            0.76,
            0.68,
            0.21,
            0.18,
        ])
        
        self.radio_set = RadioButtons(
            ax_set,
            (
                "y = 2x",
                "y = -x",
                "y = 2x + 1",
            ),
        )
        
        self.radio_set.on_clicked(
            self.change_set
        )
        
        # Operation selection
        ax_mode = self.fig.add_axes([
            0.76,
            0.46,
            0.21,
            0.16,
        ])
        
        self.radio_mode = RadioButtons(
            ax_mode,
            (
                "Soma",
                "Escalar",
                "Combinação",
            ),
        )
        
        self.radio_mode.on_clicked(
            self.change_mode
        )
        
        # Information area
        self.info_ax = self.fig.add_axes([
            0.75,
            0.08,
            0.23,
            0.30,
        ])
        
        self.info_ax.axis("off")
    
    # --------------------------------------------------

    def on_change(self, _):
        self.ux = self.slider_ux.val
        self.vx = self.slider_vx.val
        
        self.a = self.slider_a.val
        self.b = self.slider_b.val
        
        self.update()
    
    def change_set(self, name):
        self.current_set_name = name
        
        self.update()
    
    def change_mode(self, mode):
        self.mode = mode
        
        self.update()
    
    # --------------------------------------------------
    # Draw
    # --------------------------------------------------

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
            label=label,
        )
        
        self.ax.text(
            origin[0] + x,
            origin[1] + y,
            f"  {label}",
        )
    
    def calculate_limit(
        self,
        *vectors,
    ):
        values = []
        
        for vector in vectors:
            values.extend(
                abs(value)
                for value in vector.values
            )
        
        maximum = max(
            values,
            default=5,
        )
        
        return max(
            5,
            maximum * 1.30,
        )
    
    def setup_axis(
        self,
        limit,
    ):
        self.ax.clear()
        
        self.ax.axhline(
            0,
            linewidth=1
        )
        
        self.ax.axvline(
            0,
            linewidth=1,
        )
        
        self.ax.set_xlim(
            -limit,
            limit,
        )
        
        self.ax.set_ylim(
            -limit,
            limit,
        )
        
        self.ax.set_aspect(
            "equal",
            adjustable="box"
        )
        
        self.ax.grid(True)
        
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
    
    def draw_set(self, limit):
        m, c = self.get_current_parameters()
        
        # Keeps the line on its limit
        # of the visible vertical area
        x_limit = limit / max(
            1,
            abs(m),
        )
        
        xs = np.linspace(
            -x_limit,
            x_limit,
            200,
        )
        
        ys = m * xs + c
        
        self.ax.plot(
            xs,
            ys,
            label=self.current_set_name,
        )
        
    # --------------------------------------------------
    # Verifications
    # --------------------------------------------------

    def is_inside(self, vector):
        subspace = self.make_subspace()
        
        return subspace.contains(
            vector
        )
    
    def get_zero(self):
        return self.r2.zero()
    
    def update_information(
        self,
        u,
        v,
    ):
        self.info_ax.clear()
        self.info_ax.axis("off")
        
        zero = self.get_zero()
        
        zero_test = self.is_inside(
            zero
        )
        
        sum_result = u + v
        
        sum_test = self.is_inside(
            sum_result
        )
        
        scalar_result = self.a * u
        
        scalar_test = self.is_inside(
            scalar_result
        )
                
        combination = (
            self.a * u
            + self.b * v
        )
        
        combination_test = (
            self.is_inside(combination)
        )
        
        text = (
            f"Conjunto:\n"
            f"{self.current_set_name}\n\n"

            f"u = {u.values}\n"
            f"v = {v.values}\n\n"

            f"Testes atuais:\n\n"

            f"0 ∈ W: "
            f"{zero_test}\n\n"

            f"u + v ∈ W: "
            f"{sum_test}\n\n"

            f"a·u ∈ W: "
            f"{scalar_test}\n\n"

            f"a·u + b·v ∈ W: "
            f"{combination_test}"
        )
        
        self.info_ax.text(
            0,
            1,
            text,
            va="top",
            fontsize=11,
        )

    # --------------------------------------------------
    # Modos
    # --------------------------------------------------

    def plot_sum(
        self,
        u,
        v,
    ):
        result = u + v
        
        limit = self.calculate_limit(
            u,
            v,
            result,
        )
        
        self.setup_axis(limit)
        self.draw_set(limit)
        
        self.draw_vector(
            u,
            f"u={u.values}"
        )
        
        self.draw_vector(
            v,
            f"u+v={result.values}",
        )
        
        inside = self.is_inside(
            result
        )
        
        self.ax.set_title(
            "Fechamento da soma\n"
            "u, v ∈ W  ⇒  u + v ∈ W\n"
            f"Resultado pertence ao conjunto: {inside}"
        )

    def plot_scalar(
        self,
        u,
    ):
        result = self.a * u
        
        limit = self.calculate_limit(
            u,
            result,
        )
        
        self.setup_axis(limit)
        self.draw_set(limit)
        
        self.draw_vector(
            u,
            f"u={u.values}"
        )
        
        self.draw_vector(
            result,
            f"u={u.values}",
        )
        
        self.draw_vector(
            result,
            f"{self.a:g}u={result.values}",
        )
        
        inside = self.is_inside(
            result
        )
        
        self.ax.set_title(
            "Fechamento por escalar\n"
            "u ∈ W  ⇒  au ∈ W\n"
            f"a = {self.a:g} | "
            f"resultado pertence: {inside}"
        )
    
    def plot_combination(
        self,
        u,
        v
    ):
        result = (
            self.a * u
            + self.b * v
        )
        
        limit = self.calculate_limit(
            u,
            v,
            result,
        )
        
        self.setup_axis(limit)
        self.draw_set(limit)
        
        self.draw_vector(
            u,
            f"u={u.values}",
        )
        
        self.draw_vector(
            v,
            f"v={v.values}",
        )
        
        self.draw_vector(
            result,
            (
              f"{self.a:g}u"
              f"+ {self.b:g}v"  
              f"= {result.values}"
            ),
        )
        
        inside = self.is_inside(
            result
        )
        
        self.ax.set_title(
            "Combinação linear\n"
            "au + bv\n"
            f"Resultado pertence ao conjunto: {inside}"
        )

    # --------------------------------------------------
    # Main update
    # --------------------------------------------------
    
    def update(self):
        u = self.make_vector(
            self.ux
        )
        
        v = self.make_vector(
            self.vx
        )
        
        if self.mode == "Soma":
            self.plot_sum(
                u,
                v,
            )
        
        elif self.mode == "Escalar":
            self.plot_scalar(
                u,
            )
        
        elif self.mode == "Escalar":
            self.plot_scalar(
                u,
            )
        
        elif self.mode == "Combinação":
            self.plot_combination(
                u,
                v,
            )
        
        self.update_information(
            u,
            v,
        )
        
        self.ax.legend(
            loc="upper left"
        )
        
        self.fig.canvas.draw_idle()
        
    def show(self):
        plt.show()

if __name__ == "__main__":
    plot = SubspacePlot()
    plot.show()