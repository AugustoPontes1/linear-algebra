import numpy as np


def draw_subspace(
    ax,
    subspace,
    limit=4,
):
    basis = (
        subspace.independent_basis()
    )

    dimension = subspace.dimension

    if dimension == 1:
        b = np.array(
            basis[0].values,
            dtype=float,
        )
        t = np.linspace(
            -limit,
            limit,
            100,
        )

        points = np.outer(
            t,
            b,
        )

        ax.plot(
            points[:, 0],
            points[:, 1],
            points[:, 2],
            label=subspace.name,
        )

    elif dimension == 2:
        b1 = np.array(
            basis[0].values,
            dtype=float,
        )

        b2 = np.array(
            basis[1].values,
            dtype=float,
        )

        s = np.linspace(
            -limit,
            limit,
            15,
        )

        t = np.linspace(
            -limit,
            limit,
            15,
        )

        S, T = np.meshgrid(
            s,
            t,
        )

        X = (
            S * b1[0]
            + T * b2[0]
        )

        Y = (
            S * b1[1]
            + T * b2[1]
        )

        Z = (
            S * b1[2]
            + T * b2[2]
        )

        ax.plot_surface(
            X,
            Y,
            Z,
            alpha=0.25,
        )