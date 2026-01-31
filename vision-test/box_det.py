import cv2
import numpy as np


class BoxDetector:
    def detect(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (7, 7), 0)

        edges = cv2.Canny(blur, 50, 150)

        # close gaps in edges
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        boxes = []
        box_id = 0

        for cnt in contours:

            # approximate contour to polygon
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)

            # we want roughly rectangular shapes
            if len(approx) < 4:
                continue

            x, y, w, h = cv2.boundingRect(approx)

            area = w * h
            aspect_ratio = w / float(h)

            if area < 8000:
                continue

            if aspect_ratio < 0.3 or aspect_ratio > 4.0:
                continue

            boxes.append({
                "box_id": box_id,
                "bbox": [x, y, x + w, y + h]
            })

            box_id += 1

        return boxes
