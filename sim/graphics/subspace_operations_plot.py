import matplotlib.pyplot as plt

from matplotlib.widgets import RadioButtons

from sim.calculations.examples import SPACE_PAIRS
from sim.calculations.utils.r3_utils import draw_subspace


class SubspaceOperationsPlot:
    def __init__(self):
        self.pair_name = (
            "Q8: U + V"
        )
        
        self.fig = plt.figure(
            figsize=(11, 8)
        )
        
        self.ax = self.fig.add_subplot(
            111,
            projection="3d",
        )
        
        plt.subplots_adjust(
            right=0.72
        )
        
        self.create_controls()
        self.update()
    
    def create_controls(self):
        ax_radio = self.fig.add_axes([
            0.74,
            0.45,
            0.24,
            0.40,
        ])
        
        self.radio = RadioButtons(
            ax_radio,
            tuple(
                SPACE_PAIRS.keys()
            ),
        )
        
        self.radio.on_clicked(
            self.change_pair
        )
        
    def change_pair(self, name):
        self.pair_name = name
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
        W1, W2 = SPACE_PAIRS[
            self.pair_name
        ]
        
        self.ax.clear()
        
        draw_subspace(
            self.ax,
            W1,
        )
        
        draw_subspace(
            self.ax,
            W2,
        )
        
        u = W1.sample_vectors()[0]
        v = W2.sample_vectors()[0]
        
        result = u + v
        
        self.draw_vector(
            u,
            f"u ∈ {W1.name}",
        )
        
        self.draw_vector(
            u,
            f"u ∈ {W2.name}"
        )
        
        self.draw_vector(
            result,
            "u+v",
        )
        
        sum_space = W1.sum(W2)
        
        intersection_dimension = (
            W1.intersection_dimension(
                W2
            )
        )
        
        direct = (
            W1.is_direct_sum_with(
                W2
            )
        )
        
        counterexample = (
            W1.union_counterexample(
                W2
            )
        )
        
        union_closed = (
            counterexample is None
        )
        
        self.ax.set_title(
            f"{self.pair_name}\n"
            f"dim(W1)={W1.dimension} | "
            f"dim(W2)={W2.dimension}\n"
            f"dim(W1+W2)="
            f"{sum_space.dimension}\n"
            f"dim(W1∩W2)="
            f"{intersection_dimension}\n"
            f"Soma direta: {direct}\n"
            f"União passou no teste de "
            f"fechamento: {union_closed}",
            y=1.05,
            x=-0.01,
            fontsize=9
        )
        
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.ax.set_zlim(-5, 5)
        
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        
        self.ax.legend()
        
        self.fig.canvas.draw_idle()
        
    def show(self):
        plt.show()

if __name__ == "__main__":
    SubspaceOperationsPlot().show()
