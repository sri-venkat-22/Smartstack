import numpy as np
from environment.env_init import PackingEnvironment
from agent_heuristics import (
    generate_candidates,
    update_extreme_points
)
from environment.visualisation import visualize_environment

from encoding import encode_candidates


def run_episode(env, episode_id):

    print(f" EPISODE {episode_id}")


    env.reset(mode="random")

    # use first 3 boxes
    env.boxes = env.boxes[:3]

    extreme_points = [(0, 0, 0)]

    # place first box deterministically
    first_box = env.boxes[0]

    placed_box = {
        "id": first_box.id,
        "dims": (first_box.length, first_box.width, first_box.height),
        "position": (0, 0, 0),
        "fragile": first_box.fragile,
        "weight": first_box.weight,
        "priority": first_box.priority
    }

    env.placed_boxes = [placed_box]
    env.boxes = env.boxes[1:]

    extreme_points = update_extreme_points(extreme_points, placed_box)

    # generate candidates
    candidates = generate_candidates(
        remaining_boxes=env.boxes,
        placed_boxes=env.placed_boxes,
        container_dims=env.container_dims,
        extreme_points=extreme_points
    )

    if len(candidates) == 0:
        print("❌ No candidates generated")
        return

    # encode
    C = encode_candidates(
        candidates,
        env.placed_boxes,
        env.container_dims
    )

    # print summary statistics
    print(f"Candidates: {len(candidates)}")
    print("Feature means:", np.round(C.mean(axis=0), 3))
    print("Feature mins :", np.round(C.min(axis=0), 3))
    print("Feature maxs :", np.round(C.max(axis=0), 3))


def test_multiple_episodes():

    env = PackingEnvironment(
        container_dims=(3.0, 3.0, 3.0),
        seed=42
    )

    for ep in range(1, 6):
        run_episode(env, ep)


if __name__ == "__main__":
    test_multiple_episodes()
