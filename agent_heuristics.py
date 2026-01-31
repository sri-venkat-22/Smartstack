import itertools
import numpy as np


# Rotation Generator

def generate_rotations(dims):
    """
    Generate all 6 unique box rotations.
    dims = (l, w, h)
    """
    return list(set(itertools.permutations(dims, 3)))


# AABB Collision Check


def boxes_overlap(box1, box2):
    """
    Axis-Aligned Bounding Box collision test.
    """

    (x1, y1, z1), (l1, w1, h1) = box1
    (x2, y2, z2), (l2, w2, h2) = box2

    return (
        x1 < x2 + l2 and x1 + l1 > x2 and
        y1 < y2 + w2 and y1 + w1 > y2 and
        z1 < z2 + h2 and z1 + h1 > z2
    )


# Container Bounds Check

def inside_container(position, dims, container_dims):
    x, y, z = position
    l, w, h = dims
    L, W, H = container_dims

    return (
        x + l <= L and
        y + w <= W and
        z + h <= H
    )

# Stability Check (Simple)

def is_stable(position, dims, placed_boxes, threshold=0.6):
    """
    Box is stable if:
    - on floor
    OR
    - sufficiently supported by boxes beneath
    """

    x, y, z = position
    l, w, h = dims

    if z == 0:
        return True

    supported_area = 0.0
    bottom_area = l * w

    for pb in placed_boxes:
        px, py, pz = pb["position"]
        pl, pw, ph = pb["dims"]

        # must touch exactly below
        if abs((pz + ph) - z) > 1e-6:
            continue

        # overlap area
        dx = max(0, min(x + l, px + pl) - max(x, px))
        dy = max(0, min(y + w, py + pw) - max(y, py))

        supported_area += dx * dy

    return supported_area / bottom_area >= threshold


# Extreme Point Generator

def update_extreme_points(extreme_points, placed_box):
    """
    Add new extreme points from placed box.
    """

    x, y, z = placed_box["position"]
    l, w, h = placed_box["dims"]

    new_points = [
        (x + l, y, z),
        (x, y + w, z),
        (x, y, z + h)
    ]

    for p in new_points:
        if p not in extreme_points:
            extreme_points.append(p)

    return extreme_points

# Candidate Generator
def generate_candidates(
    remaining_boxes,
    placed_boxes,
    container_dims,
    extreme_points
):
    """
    Core hybrid heuristic step.
    """

    candidates = []

    for box in remaining_boxes:

        dims = (box.length, box.width, box.height)
        rotations = generate_rotations(dims)

        for rot in rotations:
            for ep in extreme_points:

                position = ep

                # bounds
                if not inside_container(position, rot, container_dims):
                    continue

                #  collision
                collision = False
                for pb in placed_boxes:
                    if boxes_overlap(
                        (position, rot),
                        (pb["position"], pb["dims"])
                    ):
                        collision = True
                        break

                if collision:
                    continue

                #  stability
                if not is_stable(position, rot, placed_boxes):
                    continue

                # candidate accepted
                candidates.append({
                    "box_id": box.id,
                    "dims": rot,
                    "position": position,
                    "weight": box.weight,
                    "fragile": box.fragile,
                    "priority": box.priority
                })

    return candidates
