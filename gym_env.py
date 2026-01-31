import gymnasium as gym
import numpy as np

from agent_heuristics import generate_candidates, update_extreme_points
from encoding import encode_candidates


class HybridPackingEnv(gym.Env):
    """
    Efficient hybrid RL environment for 3D bin packing.
    """

    def __init__(
        self,
        base_env,
        max_candidates=50,
        max_boxes=50
    ):
        super().__init__()

        self.env = base_env
        self.max_candidates = max_candidates
        self.max_boxes = max_boxes

        # -------------------------
        # Action space
        # -------------------------
        self.action_space = gym.spaces.Discrete(max_candidates)

        # -------------------------
        # Observation space
        # -------------------------
        self.observation_space = gym.spaces.Dict({
            "candidates": gym.spaces.Box(
                0.0, 1.5,
                shape=(max_candidates, 10),
                dtype=np.float32
            ),
            "mask": gym.spaces.Box(
                0, 1,
                shape=(max_candidates,),
                dtype=np.int8
            ),
            "global": gym.spaces.Box(
                0.0, 1.0,
                shape=(5,),
                dtype=np.float32
            ),
            "remaining": gym.spaces.Box(
                0.0, 1.0,
                shape=(4,),
                dtype=np.float32
            )
        })

        self.reset()

    # ==================================================
    # Encoders
    # ==================================================

    def _encode_global(self):
        if not self.env.placed_boxes:
            return np.zeros(5, dtype=np.float32)

        L, W, H = self.env.container_dims
        total_volume = L * W * H

        volumes = [np.prod(pb["dims"]) for pb in self.env.placed_boxes]
        heights = [
            pb["position"][2] + pb["dims"][2]
            for pb in self.env.placed_boxes
        ]

        return np.array([
            sum(volumes) / total_volume,
            max(heights) / H,
            np.mean(heights) / H,
            len(self.env.placed_boxes) / self.max_boxes,
            len(self.env.boxes) / self.max_boxes
        ], dtype=np.float32)

    def _encode_remaining(self):
        if not self.env.boxes:
            return np.zeros(4, dtype=np.float32)

        volumes = [
            b.length * b.width * b.height
            for b in self.env.boxes
        ]

        weights = [b.weight for b in self.env.boxes]
        fragile_ratio = sum(b.fragile for b in self.env.boxes) / len(self.env.boxes)

        return np.array([
            np.mean(volumes),
            np.max(volumes),
            np.mean(weights) / 50,
            fragile_ratio
        ], dtype=np.float32)

    # ==================================================
    # Core Helpers
    # ==================================================

    def _build_observation(self):
        C = np.zeros((self.max_candidates, 10), dtype=np.float32)
        mask = np.zeros(self.max_candidates, dtype=np.int8)
        self._last_mask = mask
        n = min(len(self.C), self.max_candidates)
        if n > 0:
            C[:n] = self.C[:n]
            mask[:n] = 1

        return {
            "candidates": C,
            "mask": mask,
            "global": self._encode_global(),
            "remaining": self._encode_remaining()
        }

    def _update_candidates(self):
        self.candidates = generate_candidates(
            self.env.boxes,
            self.env.placed_boxes,
            self.env.container_dims,
            self.extreme_points
        )

        self.C = encode_candidates(
            self.candidates,
            self.env.placed_boxes,
            self.env.container_dims
        )

    # ==================================================
    # Gym API
    # ==================================================

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.env.reset(mode="random")
        self.extreme_points = [(0, 0, 0)]

        self._update_candidates()

        return self._build_observation(), {}
    def action_masks(self):
            return self._last_mask
    def step(self, action):

        # invalid action (masked)
        if action >= len(self.candidates):
            return self._build_observation(), -1.0, True, False, {}

        chosen = self.candidates[action]

        placed = {
            "id": chosen["box_id"],
            "dims": chosen["dims"],
            "position": chosen["position"],
            "fragile": chosen["fragile"],
            "weight": chosen["weight"],
            "priority": chosen["priority"]
        }

        self.env.placed_boxes.append(placed)
        self.env.boxes = [
            b for b in self.env.boxes if b.id != chosen["box_id"]
        ]

        self.extreme_points = update_extreme_points(
            self.extreme_points,
            placed
        )

        # -------------------------
        # Reward shaping
        # -------------------------
        volume_gain = np.prod(chosen["dims"])
        container_volume = np.prod(self.env.container_dims)

        height = placed["position"][2] + placed["dims"][2]

        reward = (
            volume_gain / container_volume
            - 0.01 * height
        )

        # -------------------------
        # Next step
        # -------------------------
        self._update_candidates()

        done = (
            len(self.env.boxes) == 0
            or len(self.candidates) == 0
        )

        if done and len(self.env.boxes) > 0:
            reward -= 0.5  # failed packing

        return self._build_observation(), reward, done, False, {}

if __name__ == "__main__":
    # Example usage
    base_env = PackingEnvironment(container_dims=(5, 5, 5), num_boxes=10, seed=42)
    env = HybridPackingEnv(base_env)

    obs, _ = env.reset()
    done = False

    while not done:
        action = env.action_space.sample()
        obs, reward, done, _, _ = env.step(action)
        print(f"Action: {action}, Reward: {reward}, Done: {done}")