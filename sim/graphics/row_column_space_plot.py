import matplotlib.pyplot as plt

from sim.calculations.matrix import Matrix


class RowColumnSpacePlot:

    def __init__(self):
        self.A = Matrix([
            [1, 2, -1],
            [2, 4, 1],
            [3, 6, 3],
        ])

        self.fig = plt.figure(
            figsize=(12, 7)
        )

        self.ax_rows = self.fig.add_subplot(
            121,
            projection="3d",
        )

        self.ax_cols = self.fig.add_subplot(
            122,
            projection="3d",
        )

        self.update()

    def draw_vectors(
        self,
        ax,
        vectors,
        title,
    ):
        ax.clear()

        for index, vector in enumerate(
            vectors,
            start=1,
        ):
            x, y, z = vector.values

            ax.quiver(
                0,
                0,
                0,
                x,
                y,
                z,
                label=f"v{index}",
            )

        ax.set_xlim(-7, 7)
        ax.set_ylim(-7, 7)
        ax.set_zlim(-7, 7)

        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

        ax.set_title(title)

        ax.legend()

    def update(self):
        rows = (
            self.A
            .rows_as_vectors()
        )

        columns = (
            self.A
            .columns_as_vectors()
        )

        self.draw_vectors(
            self.ax_rows,
            rows,
            (
                "Espaço linha\n"
                f"dim = "
                f"{self.A.row_space().dimension}"
            ),
        )

        self.draw_vectors(
            self.ax_cols,
            columns,
            (
                "Espaço coluna\n"
                f"dim = "
                f"{self.A.column_space().dimension}"
            ),
        )

        reduced, pivots = (
            self.A.rref()
        )

        self.fig.suptitle(
            "Espaço linha e espaço coluna\n"
            f"posto(A) = {self.A.rank()}\n"
            f"pivôs = {pivots}"
        )

        self.fig.canvas.draw_idle()

    def show(self):
        plt.show()


if __name__ == "__main__":
    RowColumnSpacePlot().show()