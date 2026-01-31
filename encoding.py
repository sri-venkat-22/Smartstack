import numpy as np


# Utility: Support Ratio

def compute_support_ratio(candidate, placed_boxes):
    """
    Fraction of bottom face supported.
    """

    x, y, z = candidate["position"]
    l, w, h = candidate["dims"]

    if z == 0:
        return 1.0

    bottom_area = l * w
    supported_area = 0.0

    for pb in placed_boxes:
        px, py, pz = pb["position"]
        pl, pw, ph = pb["dims"]

        # must be directly beneath
        if abs((pz + ph) - z) > 1e-6:
            continue

        dx = max(0, min(x + l, px + pl) - max(x, px))
        dy = max(0, min(y + w, py + pw) - max(y, py))

        supported_area += dx * dy

    return supported_area / bottom_area


# Utility: Local Void Estimation

def compute_local_void(candidate, placed_boxes):
    """
    Approximate empty space above placement.
    """

    x, y, z = candidate["position"]
    l, w, h = candidate["dims"]

    max_neighbor_height = z

    for pb in placed_boxes:
        px, py, pz = pb["position"]
        pl, pw, ph = pb["dims"]

        overlap_x = not (px + pl <= x or px >= x + l)
        overlap_y = not (py + pw <= y or py >= y + w)

        if overlap_x and overlap_y:
            max_neighbor_height = max(max_neighbor_height, pz + ph)

    return max_neighbor_height - z

# Candidate Encoding


def encode_candidates(
    candidates,
    placed_boxes,
    container_dims,
    max_weight=50.0,
    max_priority=5
):
    """
    Converts candidate placements into feature matrix C.
    """

    L, W, H = container_dims
    container_volume = L * W * H

    encoded = []

    for c in candidates:

        l, w, h = c["dims"]
        x, y, z = c["position"]

        # geometric features

        box_volume = (l * w * h) / container_volume
        box_weight = c["weight"] / max_weight

        fragile_flag = 1.0 if c["fragile"] else 0.0
        priority = c["priority"] / max_priority

        # normalized position
        x_n = x / L
        y_n = y / W
        z_n = z / H

        # structural features

        support_ratio = compute_support_ratio(c, placed_boxes)

        local_void = compute_local_void(c, placed_boxes) / H

        # accessibility feature


        # assume door at x = 0
        distance_to_door = x / L

        feature_vector = [
            box_volume,
            box_weight,
            fragile_flag,
            priority,
            x_n, y_n, z_n,
            support_ratio,
            local_void,
            distance_to_door
        ]

        encoded.append(feature_vector)

    return np.array(encoded, dtype=np.float32)
