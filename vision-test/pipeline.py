import cv2
from depth_est import DepthEstimator
from dim_est import DimensionEstimator
from box_det import BoxDetector


class VisionPipeline:
    def __init__(self):
        self.detector = BoxDetector()
        self.depth_estimator = DepthEstimator()
        self.dimension_estimator = DimensionEstimator()

    def process(self, image_path, visualize=True):
        image = cv2.imread(image_path)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = self.detector.detect(image)
        depth_map = self.depth_estimator.estimate(image_rgb)

        results = []

        for box in boxes:
            x1, y1, x2, y2 = box["bbox"]

            dims = self.dimension_estimator.estimate(
                box["bbox"], depth_map
            )

            if dims:
                results.append({
                    "box_id": box["box_id"],
                    **dims,
                    "bbox": box["bbox"]
                })

                # ---------- DRAW BOUNDING BOX ----------
                cv2.rectangle(
                    image,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    2
                )

                # ---------- DISPLAY DIMENSIONS ----------
                label = f"{dims['width']:.2f} x {dims['height']:.2f} x {dims['depth']:.2f} m"

                cv2.putText(
                    image,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 255, 0),
                    2
                )

        if visualize:
            cv2.imshow("Detected Boxes", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        return results


if __name__ == "__main__":
    pipeline = VisionPipeline()
    boxes = pipeline.process(
        r"C:/Users/Golconda Dwarak/Desktop/Stacking_proj/test/box.jpg"
    )

    print(boxes)
