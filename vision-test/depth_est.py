import torch
import cv2
import numpy as np


class DepthEstimator:
    def __init__(self, device=None):
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.model = torch.hub.load(
            "intel-isl/MiDaS", "DPT_Hybrid"
        ).to(self.device)

        self.model.eval()

        transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
        self.transform = transforms.dpt_transform

    def estimate(self, image_rgb):
        """
        Returns normalized depth map
        """
        input_batch = self.transform(image_rgb).to(self.device)

        with torch.no_grad():
            prediction = self.model(input_batch)

        depth_map = prediction.squeeze().cpu().numpy()
        depth_map = cv2.normalize(depth_map, None, 0, 1, cv2.NORM_MINMAX)

        return depth_map
