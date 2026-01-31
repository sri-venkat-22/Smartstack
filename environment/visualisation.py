import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import random


# =========================
# Draw Cuboid
# =========================

def draw_cuboid(ax, origin, size, color, alpha=0.6):
    """
    Draw a 3D cuboid.

    origin = (x, y, z)
    size   = (l, w, h)
    """

    x, y, z = origin
    l, w, h = size

    # 8 vertices
    vertices = [
        [x, y, z],
        [x + l, y, z],
        [x + l, y + w, z],
        [x, y + w, z],
        [x, y, z + h],
        [x + l, y, z + h],
        [x + l, y + w, z + h],
        [x, y + w, z + h]
    ]

    # faces
    faces = [
        [vertices[j] for j in [0, 1, 2, 3]],
        [vertices[j] for j in [4, 5, 6, 7]],
        [vertices[j] for j in [0, 1, 5, 4]],
        [vertices[j] for j in [2, 3, 7, 6]],
        [vertices[j] for j in [1, 2, 6, 5]],
        [vertices[j] for j in [0, 3, 7, 4]],
    ]

    ax.add_collection3d(
        Poly3DCollection(
            faces,
            facecolors=color,
            linewidths=1,
            edgecolors="black",
            alpha=alpha
        )
    )


# =========================
# Container Visualization
# =========================
def draw_container(ax, container_dims):
    L, W, H = container_dims
    draw_cuboid(
        ax,
        origin=(0, 0, 0),
        size=(L, W, H),
        color="lightgray",   # MUST be real color
        alpha=0.05
    )

# =========================
# Plot Environment
# =========================

def visualize_environment(env):
    """
    Visualize current environment state.
    """

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection="3d")

    # container
    draw_container(ax, env.container_dims)

    # placed boxes
    for b in env.placed_boxes:
        color = "red" if b["fragile"] else "skyblue"
        draw_cuboid(
            ax,
            origin=b["position"],
            size=b["dims"],
            color=color,
            alpha=0.8
        )


    # axis settings
    ax.set_xlim(0, env.container_dims[0])
    ax.set_ylim(0, env.container_dims[1])
    ax.set_zlim(0, env.container_dims[2])

    ax.set_xlabel("Length (m)")
    ax.set_ylabel("Width (m)")
    ax.set_zlabel("Height (m)")

    ax.set_title("3D Bin Packing Environment")

    plt.tight_layout()
    plt.show()
