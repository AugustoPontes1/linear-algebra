import math

import matplotlib.pyplot as plt

from matplotlib.widgets import RadioButtons, Slider
from sim.calculations.matrix import Matrix


class MatrixSubspacePlot:
    def __init__(self):
        self.A = Matrix([
            [1, 0],
            [0, 2],
        ])
        
        self.C = Matrix([
            [2, 0],
            [0, 1],
        ])
        
        self.scalar = 2
        
        self.B = Matrix([
            [1, 0],
            [0, 2],
        ])
        
        self.mode = "Diagonal"
        
        self.fig, self.axes = plt.subplots(
            2,
            2,
            figsize=(10, 8),
        )
        
        plt.subplots_adjust(
            right=0.76,
            bottom=0.38,
        )
        
        self.create_controls()
        self.update()
    
    def predicate(self, matrix):
        if self.mode == "Diagonal":
            return matrix.is_diagonal()
        
        if self.mode == "AB = BA":
            return(
                matrix @ self.B
                == self.B @ matrix
            )
        
        if self.mode == "A² = A":
            return (
                matrix @ matrix
                == matrix
            )
        
        if self.mode == "det(A) = 0":
            return math.isclose(
                matrix.determinant(),
                0,
                abs_tol=1e-9,
            )
        
        return False

    def get_matrix(self, sliders):
        values = [
            slider.val
            for slider in sliders
        ]
        
        return Matrix([
            [values[0], values[1]],
            [values[2], values[3]],
        ])
    
    def create_controls(self):
        self.A_sliders = []
        self.C_sliders = []
        
        labels = (
            "11",
            "12",
            "21",
            "22",
        )
        
        initial_A = (1, 0, 0, 2)
        initial_C = (2, 0, 0, 1)
        
        positions = (
            0.28,
            0.24,
            0.20,
            0.16,
        )
        
        for label, value, y in zip(
            labels,
            initial_A,
            positions,
        ):
            ax = self.fig.add_axes([
                0.08,
                y,
                0.25,
                0.025,
            ])
            
            slider = Slider(
                ax,
                f"A{label}",
                -4,
                4,
                valinit=value,
                valstep=1,
            )
            
            slider.on_changed(
                self.on_change
            )
            
            self.A_sliders.append(slider)
        
        for label, value, y in zip(
            labels,
            initial_C,
            positions,
        ):
            ax = self.fig.add_axes([
                0.42,
                y,
                0.25,
                0.025,
            ])
            
            slider = Slider(
                ax,
                f"C{label}",
                -4,
                4,
                valinit=value,
                valstep=1,
            )
            
            slider.on_changed(
                self.on_change
            )
            
            self.C_sliders.append(slider)
            
        ax_scalar = self.fig.add_axes([
            0.08,
            0.09,
            0.59,
            0.025,
        ])
        
        self.scalar_slider = Slider(
            ax_scalar,
            "a",
            -3,
            3,
            valinit=2,
            valstep=1,
        )
        
        self.scalar_slider.on_changed(
            self.on_change
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
                "Diagonal",
                "AB = BA",
                "A² = A",
                "det(A) = 0",                
            ),
        )
        
        self.radio.on_clicked(
            self.change_mode
        )
    
    def change_mode(self, mode):
        self.mode = mode
        self.update()
    
    def on_change(self, _):
        self.A = self.get_matrix(
            self.A_sliders
        )
        
        self.C = self.get_matrix(
            self.C_sliders
        )
        
        self.scalar = (
            self.scalar_slider.val
        )
        
        self.update()
    
    def draw_matrix(
        self,
        ax,
        matrix,
        title,
    ):
        ax.clear()
        
        ax.imshow(
            matrix.values,
            vmin=-15,
            vmax=15,
        )
        
        for i in range(2):
            for j in range(2):
                ax.text(
                    j,
                    i,
                    f"{matrix.values[i][j]:g}",
                    ha="center",
                    va="center",
                    fontsize=16,
                )
        
        ax.set_title(title)
    
    def update(self):
        sum_matrix = self.A + self.C
        scalar_matrix = self.scalar * self.A
        
        self.draw_matrix(
            self.axes[0, 0],
            self.A,
            "A",
        )
        
        self.draw_matrix(
            self.axes[0, 1],
            self.C,
            "C",
        )
        
        self.draw_matrix(
            self.axes[1, 0],
            sum_matrix,
            "A + C",
        )
        
        self.draw_matrix(
            self.axes[1, 1],
            scalar_matrix,
            "aA",
        )
        
        a_in = self.predicate(self.A)
        c_in = self.predicate(self.C)
        
        sum_in = self.predicate(
            scalar_matrix
        )
        
        scalar_in = self.predicate(
            scalar_matrix
        )
        
        self.fig.suptitle(
            f"Conjunto: {self.mode}\n"
            f"A ∈ W: {a_in} | "
            f"C ∈ W: {c_in}\n"
            f"A+C ∈ W: {sum_in} | "
            f"aA ∈ W: {scalar_in}"            
        )
        
        self.fig.canvas.draw_idle()
    
    def show(self):
        plt.show()


if __name__ == "__main__":
    MatrixSubspacePlot().show()
