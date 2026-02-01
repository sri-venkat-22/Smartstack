import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Tuple

app = FastAPI()

# 1. Allow the React app to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (good for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 2. Define the data format we expect from React
class PackRequest(BaseModel):
    bin: List[float]  # [width, height, depth]
    items: List[List[float]]  # [[w, h, d, weight, fragile], ...]


class Box:
    def __init__(self, w, h, d, weight, fragile, id):
        self.w = w
        self.h = h
        self.d = d
        self.weight = weight
        self.fragile = fragile
        self.id = id
        self.position = None  # [x, y, z]


def intersect(b1, pos1, b2, pos2):
    return (
            pos1[0] < pos2[0] + b2.w and pos1[0] + b1.w > pos2[0] and
            pos1[1] < pos2[1] + b2.h and pos1[1] + b1.h > pos2[1] and
            pos1[2] < pos2[2] + b2.d and pos1[2] + b1.d > pos2[2]
    )


@app.post("/pack")
def pack_items(req: PackRequest):
    bin_w, bin_h, bin_d = req.bin

    # Create Box objects
    boxes = []
    for i, item in enumerate(req.items):
        # item = [w, h, d, weight, fragile]
        boxes.append(Box(item[0], item[1], item[2], item[3], bool(item[4]), i))

    # --- THE LOGIC ---
    # Sort items so we pack the "Foundation" first:
    # 1. Non-Fragile first (0), Fragile last (1)
    # 2. Heaviest first (descending weight)
    # 3. Largest Volume first (tie-breaker)
    boxes.sort(key=lambda x: (x.fragile, -x.weight, -(x.w * x.h * x.d)))

    packed_boxes = []

    for box in boxes:
        best_pos = None
        min_dist_to_origin = float('inf')

        # Try to place the box at every corner of every existing box (plus origin)
        # This is a simplified "Corner Point" heuristic
        candidate_points = [(0, 0, 0)]
        for pb in packed_boxes:
            px, py, pz = pb.position
            pw, ph, pd = pb.w, pb.h, pb.d
            # Add points at the top-right-front corners of existing boxes
            candidate_points.append((px + pw, py, pz))  # Right
            candidate_points.append((px, py + ph, pz))  # Top
            candidate_points.append((px, py, pz + pd))  # Front
            # Also try stacking directly on top (important for gravity logic)
            candidate_points.append((px, py + ph, pz))

            # Sort points to prefer (0,0,0) / bottom-left-back
        candidate_points.sort(key=lambda p: (p[1], p[2], p[0]))

        placed = False

        # Try both orientations (Standard and Rotated 90 degrees on floor)
        orientations = [
            (box.w, box.h, box.d),
            (box.d, box.h, box.w)  # Rotate on floor
        ]

        for w, h, d in orientations:
            if placed: break

            for x, y, z in candidate_points:
                # 1. Check if fits in Bin
                if x + w > bin_w or y + h > bin_h or z + d > bin_d:
                    continue

                # 2. Check collision with packed boxes
                collision = False
                for pb in packed_boxes:
                    if intersect(
                            type('obj', (object,), {'w': w, 'h': h, 'd': d}), (x, y, z),
                            pb, pb.position
                    ):
                        collision = True
                        break

                if not collision:
                    box.w, box.h, box.d = w, h, d  # Update orientation
                    box.position = [x, y, z]
                    packed_boxes.append(box)
                    placed = True
                    break

    # Format response for React
    result = []
    for box in packed_boxes:
        result.append({
            "name": f"Item {box.id + 1}",
            "dimensions": [box.w, box.h, box.d],
            "position": box.position,
            "weight": box.weight,
            "fragile": box.fragile
        })

    return {"packed_items": result}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)