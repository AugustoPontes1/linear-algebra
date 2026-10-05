import numpy as np
import matplotlib.pyplot as plt

from matplotlib.widgets import RadioButtons, Slider

from sim.calculations.polynoms import Polynomial


class FunctionSpacePlot:
    def __init__(self):
        self.f = Polynomial(0, 0, 1)
        self.g = Polynomial(0, 1, 0)
        
        self.scalar = 2
        self.mode = "Par"
        
        self.fig, self.ax = plt.subplots(
            figsize=(10, 7)
        )
        
        plt.subplots_adjust(
            right=0.76,
            bottom=0.35,
        )
        
        self.create_controls()
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
            0.25,
            0.025,
        ])
        
        slider = Slider(
            ax,
            label,
            -4,
            4,
            valinit=value,
            valstep=1,
        )
        
        slider.on_changed(
            self.on_change
        )
        
        return slider

    def create_controls(self):
        self.f0 = self.create_slider(
            0.08, 0.25, "a₀", 0
        )

        self.f1 = self.create_controls(
            0.08, 0.20, "a₁", 0
        )

        self.f2 = self.create_slider(
            0.08, 0.15, "a₂", 1
        )

        self.g0 = self.create_slider(
            0.40, 0.25, "b₀", 0
        )

        self.g1 = self.create_slider(
            0.40, 0.20, "b₁", 1
        )

        self.g2 = self.create_slider(
            0.40, 0.15, "b₂", 0
        )

        self.scalar_slider = (
            self.create_slider(
                0.08,
                0.08,
                "a",
                2
            )
        )

        ax_radio = self.fig.add_axes([
            0.79,
            0.55,
            0.18,
            0.30,
        ])

        self.radio = RadioButtons(
            ax_radio,
            (
                "Par",
                "Ímpar",
                "f(0)=f(1)",
                "Função zero",
                "f(x²)=f(x)²",                
            ),
        )

        self.radio.on_clicked(
            self.change_mode
        )

    def on_change(self, _):
        self.f = Polynomial(
            self.f0.val,
            self.f1.val,
            self.f2.val,
        )

        self.g = Polynomial(
            self.g0.val,
            self.g1.val,
            self.g2.val,
        )

        self.scalar = (
            self.scalar_slider.val
        )

        self.update()

    def change_mode(self, mode):
        self.mode = mode
        self.update()

    def predicate(self, f):
        xs = np.linspace(
            -3, 
            3,
            101,
        )

        values = f(xs)

        if self.mode == "Par":
            return np.allclose(
                f(-xs),
                values,
            )

        if self.mode == "Ímpar":
            return np.allclose(
                f(-xs),
                values,
            )

        if self.mode == "f(0)=f(1)":
            return np.isclose(
                f(0),
                f(1),
            )

        if self.mode == "Funcao Zero":
            return np.allclose(
                values,
                0,
            )

        if self.mode == "f(x²)=f(x)²":
            return np.allclose(
                f(xs ** 2),
                f(xs) ** 2,
            )

        return False

    def update(self):
        self.ax.clear()

        xs = np.linspace(
            -3,
            3,
            400,
        )

        fg = self.f + self.g
        af = self.scalar * self.f

        self.ax.plot(
            xs,
            self.f(xs),
            label="f(x)",
        )

        self.ax.plot(
            xs,
            self.g(xs),
            label="g(x)",
        )

        self.ax.plot(
            xs,
            fg(xs),
            label="f(x)+g(x)",
        )

        self.ax.plot(
            xs,
            af(xs),
            label="a·f(x)",
        )

        self.ax.plot(
            xs,
            self.f(-xs),
            label="f(-x)",
        )

        self.ax.axhline(0)
        self.ax.axvline(0)
        self.ax.grid(True)

        f_in = self.predicate(self.f)
        g_in = self.predicate(self.g)

        sum_in = self.predicate(fg)
        scalar_in = self.predicate(af)

        self.ax.set_title(
            f"Condição: {self.mode}\n"
            f"f ∈ W: {f_in} | "
            f"g ∈ W: {g_in}\n"
            f"f+g ∈ W: {sum_in} | "
            f"af ∈ W: {scalar_in}"            
        )

        self.ax.legend()

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()


if __name__ == "__main__":
    FunctionSpacePlot().show()