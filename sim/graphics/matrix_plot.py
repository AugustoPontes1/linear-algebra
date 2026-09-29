import matplotlib

matplotlib.use("qtagg")

import matplotlib.pyplot as plt 

from matplotlib.widgets import Slider, RadioButtons
from sim.calculations.matrix import Matrix


class MatrixSpacePlot:
    def __init__(self):
        self.A = Matrix([
            [1, 2],
            [3, 4],
        ])

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
        self.sliders_A = []
        self.sliders_B = []
        
        labels = [
            "11",
            "12",
            "21",
            "22",
        ]
        
        initial_A = [1, 2, 3, 4]
        initial_B = [2, -1,  0, 3]

        y_positions = [
            0.30,
            0.26,
            0.22,
            0.18,
        ]
        
        # Matrix A
        for label, value, y in zip(
            labels,
            initial_A,
            y_positions
        ):
            ax = self.fig.add_axes([
                0.08,
                y,
                0.28,
                0.025
            ])
            
            slider = Slider(
                ax,
                f"A{label}",
                -5,
                5,
                valinit=value,
                valstep=1
            )
            
            slider.on_changed(self.on_change)
            
            self.sliders_A.append(slider)
        
        # Matrix B
        for label, value, y in zip(
            labels,
            initial_B,
            y_positions
        ):
            ax = self.fig.add_axes([
                0.43,
                y,
                0.28,
                0.025,
            ])
            
            slider = Slider(
                ax,
                f"B{label}",
                -5,
                5,
                valinit=value,
                valstep=1,
            )
            
            slider.on_changed(self.on_change)
            
            self.sliders_B.append(slider)
        
        # Scalar
        ax_scalar = self.fig.add_axes([
            0.08,
            0.10,
            0.63,
            0.03,
        ])
        
        self.slider_scalar = Slider(
            ax_scalar,
            "a",
            -3,
            3,
            valinit=2,
            valstep=1,
        )
        
        self.slider_scalar.on_changed(
            self.on_change
        )
        
        # Modes
        ax_radio = self.fig.add_axes([
            0.81, 
            0.55,
            0.17,
            0.22,
        ])
        
        self.radio = RadioButtons(
            ax_radio,
            (
                "Soma",
                "Distributiva",
                "Oposto",
            )
        )
        
        self.radio.on_clicked(
            self.change_mode
        )
        
    def get_matrix(self, sliders):
        values = [
            slider.val
            for slider in sliders
        ]
        
        return Matrix([
            [values[0], values[1]],
            [values[2], values[3]],
        ])
        
    def on_change(self, _):
        self.A = self.get_matrix(
            self.sliders_A
        )
        
        self.B = self.get_matrix(
            self.sliders_B
        )
        
        self.scalar = (
            self.slider_scalar.val
        )
        
        self.update()
    
    def change_mode(self, mode):
        self.mode = mode
        self.update()
    
    def draw_matrix(
        self,
        ax,
        matrix,
        title,
    ):
        ax.clear()
        
        values = matrix.values
        
        ax.imshow(
            values,
            vmin=-30,
            vmax=30,
        )
        
        rows, columns = matrix.shape
        
        for i in range(rows):
            for j in range(columns):
                ax.text(
                    j,
                    i,
                    f"{values[i][j]:g}",
                    ha="center",
                    va="center",
                    fontsize=16
                )
        
        ax.set_xticks(
            range(columns)
        )
        
        ax.set_yticks(
            range(rows)
        )
        
        ax.set_title(title)
    
    def clear_axes(self):
        for ax in self.axes.flat:
            ax.clear()
            ax.axis("off")
    
    def update(self):
        self.clear_axes()
        
        if self.mode == "Soma":
            self.plot_sum()
        
        elif self.mode == "Distributiva":
            self.plot_distributive()
        
        elif self.mode == "Oposto":
            self.plot_opposite()
        
        self.fig.canvas.draw_idle()
    
    def plot_sum(self):
        result = self.A + self.B
        
        self.draw_matrix(
            self.axes[0, 0],
            self.A,
            "A",
        )
        
        self.draw_matrix(
            self.axes[0, 1],
            self.B,
            "B",
        )
        
        self.draw_matrix(
            self.axes[1, 0],
            result,
            "A + B",
        )
        
        reverse = self.B + self.A
        
        self.draw_matrix(
            self.axes[1, 1],
            reverse,
            "B + A",
        )
        
        valid = result == reverse
        
        self.fig.suptitle(
            "Comutatividade\n"
            "A + B = B + A\n"
            f"Propriedade satisfeita: {valid}"
        )
    
    def plot_distributive(self):
        left = self.scalar * (
            self.A + self.B
        )
        
        right = (
            self.scalar * self.A
            + self.scalar * self.B
        )
        
        self.draw_matrix(
            self.axes[0, 0],
            self.A,
            "A",
        )
        
        self.draw_matrix(
            self.axes[0, 1],
            self.B,
            "B",
        )
        
        self.draw_matrix(
            self.axes[1, 0],
            left,
            "a(A + B)",
        )
        
        self.draw_matrix(
            self.axes[1, 1],
            right,
            "aA + aB",
        )
        
        valid = left == right
        
        self.fig.suptitle(
            f"Distributividade - a = {self.scalar:g}\n"
            "a(A + B) = aA + aB\n"
            f"Propriedade satisfeita: {valid}"
        )
    
    def plot_opposite(self):
        opposite = -self.A
        
        zero = self.A + opposite
        
        self.draw_matrix(
            self.axes[0, 0],
            self.A,
            "A",
        )
        
        self.draw_matrix(
            self.axes[0, 1],
            opposite,
            "-A",
        )
        
        self.draw_matrix(
            self.axes[1, 0],
            zero,
            "A + (-A)",
        )
        
        expected_zero = Matrix([
            [0, 0],
            [0, 0],
        ])
        
        self.draw_matrix(
            self.axes[1, 1],
            expected_zero,
            "Matriz nula",
        )
        
        self.fig.suptitle(
            "Elemento oposto\n"
            "A + (-A) = 0"
        )
    
    def show(self):
        plt.show()

if __name__ == "__main__":
    plot = MatrixSpacePlot()
    plot.show()