import numpy as np
import random
from dataclasses import dataclass
from typing import List, Dict


# =========================
# Box Definition
# =========================

@dataclass
class Box:
    id: int
    length: float
    width: float
    height: float
    weight: float
    fragile: bool
    priority: int

    @property
    def volume(self) -> float:
        return self.length * self.width * self.height


# =========================
# Container Definition
# =========================

@dataclass
class Container:
    length: float
    width: float
    height: float

    def volume(self) -> float:
        return self.length * self.width * self.height


# =========================
# Packing Environment
# =========================

class PackingEnvironment:
    """
    Environment initialization for 3D bin packing.

    Handles:
    - Container creation
    - Box generation
    - Environment reset
    """

    def __init__(
        self,
        container_dims=(12.0, 2.4, 2.6),
        max_boxes=30,
        seed=None
    ):
        self.container_dims = container_dims
        self.max_boxes = max_boxes

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)

        self.container = Container(*container_dims)
        self.boxes: List[Box] = []
        self.placed_boxes = []

    # =========================
    # Generate Boxes
    # =========================

    def _generate_random_box(self, box_id: int) -> Box:
        """
        Generate a single random box following schema.
        """

        length = round(random.uniform(0.2, 1.2), 2)
        width  = round(random.uniform(0.2, 1.0), 2)
        height = round(random.uniform(0.15, 0.8), 2)

        weight = round(random.uniform(2, 40), 1)

        fragile = random.random() < 0.25  # 25% fragile

        priority = random.randint(1, 5)  # 1 = earliest delivery

        return Box(
            id=box_id,
            length=length,
            width=width,
            height=height,
            weight=weight,
            fragile=fragile,
            priority=priority
        )

    # =========================
    # Load from JSON
    # =========================

    def load_boxes_from_json(self, data: Dict):
        """
        Load boxes exactly from provided JSON schema.
        """

        self.boxes = []

        for box in data["boxes"]:
            self.boxes.append(
                Box(
                    id=box["id"],
                    length=box["dims"][0],
                    width=box["dims"][1],
                    height=box["dims"][2],
                    weight=box["weight"],
                    fragile=box["fragile"],
                    priority=box["priority"]
                )
            )

    # =========================
    # Random Scenario
    # =========================

    def generate_random_scenario(self):
        """
        Create a randomized episode with diverse boxes.
        """

        self.boxes = []

        for i in range(self.max_boxes):
            self.boxes.append(self._generate_random_box(i))

        self.placed_boxes = []

    # =========================
    # Reset Environment
    # =========================

    def reset(self, mode="random", json_data=None):
        """
        Reset environment.

        mode:
        - "random"
        - "json"
        """

        self.placed_boxes = []

        if mode == "random":
            self.generate_random_scenario()

        elif mode == "json":
            if json_data is None:
                raise ValueError("JSON data required for json mode")
            self.load_boxes_from_json(json_data)

        else:
            raise ValueError("Invalid reset mode")

        return self.get_state()

    # =========================
    # State Representation
    # =========================

    def get_state(self):
        """
        Returns initial state structure (used later by RL).
        """

        return {
            "container": {
                "dims": self.container_dims,
                "volume": self.container.volume()
            },
            "remaining_boxes": [
                {
                    "id": b.id,
                    "dims": [b.length, b.width, b.height],
                    "weight": b.weight,
                    "fragile": b.fragile,
                    "priority": b.priority,
                    "volume": b.volume
                }
                for b in self.boxes
            ],
            "placed_boxes": []
        }
