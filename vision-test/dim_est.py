import numpy as np


class DimensionEstimator:
    def __init__(self, reference_height=0.30):
        self.reference_height = reference_height  # meters

    def estimate(self, bbox, depth_map):
        x1, y1, x2, y2 = bbox

        crop = depth_map[y1:y2, x1:x2]

        if crop.size == 0:
            return None

        median_depth = float(np.median(crop))

        pixel_height = y2 - y1
        scale = self.reference_height / pixel_height

        width = (x2 - x1) * scale
        height = self.reference_height
        depth = median_depth * 2.0

        return {
            "width": round(width, 3),
            "height": round(height, 3),
            "depth": round(depth, 3)
        }
