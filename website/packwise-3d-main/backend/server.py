import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Any  # Changed to Any to allow strings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# CHANGED: items is now List[List[Any]] to accept [w, h, d, weight, fragile, id_string]
class PackRequest(BaseModel):
    bin: List[float]
    items: List[List[Any]]


class Box:
    def __init__(self, w, h, d, weight, fragile, id):
        self.w = w
        self.h = h
        self.d = d
        self.weight = weight
        self.fragile = fragile
        self.id = id  # Store the unique ID string
        self.position = None


def intersect(b1, pos1, b2, pos2):
    return (
            pos1[0] < pos2[0] + b2.w and pos1[0] + b1.w > pos2[0] and
            pos1[1] < pos2[1] + b2.h and pos1[1] + b1.h > pos2[1] and
            pos1[2] < pos2[2] + b2.d and pos1[2] + b1.d > pos2[2]
    )


@app.post("/pack")
def pack_items(req: PackRequest):
    bin_w, bin_h, bin_d = req.bin

    boxes = []
    for i, item in enumerate(req.items):
        # Expecting: [w, h, d, weight, fragile, id]
        # Fallback to "Item N" if no ID is provided
        custom_id = item[5] if len(item) > 5 else f"Item {i + 1}"
        boxes.append(Box(item[0], item[1], item[2], item[3], bool(item[4]), custom_id))

    # Sort: Fragile last, Heaviest first, Largest first
    boxes.sort(key=lambda x: (x.fragile, -x.weight, -(x.w * x.h * x.d)))

    packed_boxes = []

    for box in boxes:
        best_pos = None
        # Start at origin + corners of existing boxes
        candidate_points = [(0, 0, 0)]
        for pb in packed_boxes:
            px, py, pz = pb.position
            pw, ph, pd = pb.w, pb.h, pb.d
            candidate_points.append((px + pw, py, pz))
            candidate_points.append((px, py + ph, pz))
            candidate_points.append((px, py, pz + pd))
            candidate_points.append((px, py + ph, pz))  # Stack logic

        candidate_points.sort(key=lambda p: (p[1], p[2], p[0]))

        placed = False
        orientations = [(box.w, box.h, box.d), (box.d, box.h, box.w)]

        for w, h, d in orientations:
            if placed: break
            for x, y, z in candidate_points:
                if x + w > bin_w or y + h > bin_h or z + d > bin_d: continue

                collision = False
                for pb in packed_boxes:
                    if intersect(type('obj', (object,), {'w': w, 'h': h, 'd': d}), (x, y, z), pb, pb.position):
                        collision = True
                        break

                if not collision:
                    box.w, box.h, box.d = w, h, d
                    box.position = [x, y, z]
                    packed_boxes.append(box)
                    placed = True
                    break

    return {"packed_items": [{
        "id": box.id,  # Return the ID
        "dimensions": [box.w, box.h, box.d],
        "position": box.position,
        "weight": box.weight,
        "fragile": box.fragile
    } for box in packed_boxes]}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)