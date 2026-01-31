from environment.env_init import PackingEnvironment
from agent_heuristics import (
    generate_candidates,
    update_extreme_points
)
from environment.visualisation import visualize_environment


def test_heuristics():

    # -----------------------------
    # Create environment
    # -----------------------------
    env = PackingEnvironment(
        container_dims=(3.0, 3.0, 3.0),
        seed=0
    )

    env.reset(mode="random")

    # Use only first 2 boxes for clarity
    env.boxes = env.boxes[:2]

    # -----------------------------
    # Initialize extreme points
    # -----------------------------
    extreme_points = [(0, 0, 0)]

    print("\nInitial Extreme Points:")
    print(extreme_points)

    # -----------------------------
    # Place first box manually
    # -----------------------------
    first_box = env.boxes[0]

    placed_box = {
        "id": first_box.id,
        "dims": (first_box.length, first_box.width, first_box.height),
        "position": (0, 0, 0),
        "fragile": first_box.fragile,
        "weight": first_box.weight,
        "priority": first_box.priority
    }

    env.placed_boxes.append(placed_box)

    # Remove from remaining
    env.boxes = env.boxes[1:]

    # -----------------------------
    # Update extreme points
    # -----------------------------
    extreme_points = update_extreme_points(extreme_points, placed_box)

    print("\nExtreme Points After First Placement:")
    for p in extreme_points:
        print(p)

    # -----------------------------
    # Generate candidates
    # -----------------------------
    candidates = generate_candidates(
        remaining_boxes=env.boxes,
        placed_boxes=env.placed_boxes,
        container_dims=env.container_dims,
        extreme_points=extreme_points
    )

    print("\nGenerated Candidates:")
    for c in candidates:
        print(c)

    print(f"\nTotal candidates: {len(candidates)}")

    # -----------------------------
    # Visualize one candidate
    # -----------------------------
    if len(candidates) > 0:
        candidate = candidates[0]

        env.placed_boxes.append({
            "id": candidate["box_id"],
            "dims": candidate["dims"],
            "position": candidate["position"],
            "fragile": candidate["fragile"],
            "weight": candidate["weight"],
            "priority": candidate["priority"]
        })

        visualize_environment(env)


if __name__ == "__main__":
    test_heuristics()
