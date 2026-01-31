import time
from sb3_contrib import MaskablePPO

from environment.env_init import PackingEnvironment
from gym_env import HybridPackingEnv
from environment.visualisation import visualize_environment
import time
from sb3_contrib import MaskablePPO

from environment.env_init import PackingEnvironment
from gym_env import HybridPackingEnv
from environment.visualisation import visualize_environment


# =====================================
# Load trained checkpoint
# =====================================

checkpoint_path = "./checkpoints/binpack_ppo_200000_steps.zip"

model = MaskablePPO.load(checkpoint_path)

# =====================================
# Create environment
# =====================================

base_env = PackingEnvironment(
    container_dims=(3.0, 3.0, 3.0),
    seed=42
)

env = HybridPackingEnv(
    base_env=base_env,
    max_candidates=50
)

# =====================================
# Reset environment
# =====================================

obs, _ = env.reset()

total_boxes = len(env.env.boxes)
print(f"\n Total boxes detected: {total_boxes}\n")

done = False
step = 0
total_reward = 0.0

# =====================================
# Simulation loop
# =====================================

while not done:
    step += 1

    action, _ = model.predict(obs, deterministic=True)
    obs, reward, done, _, _ = env.step(action)
    total_reward += reward

    placed = len(env.env.placed_boxes)
    remaining = len(env.env.boxes)

    print(
        f"Step {step:02d} | "
        f"Placed: {placed} | "
        f"Remaining: {remaining} | "
        f"Reward: {reward:.4f}"
    )

    # 🔥 visualize physical environment
    visualize_environment(env.env)

    time.sleep(0.5)   # slow animation


# =====================================
# Final report
# =====================================

placed_boxes = len(env.env.placed_boxes)

print("\n==============================")
print(" PACKING SIMULATION RESULT")
print("==============================")
print(f"Total boxes available : {total_boxes}")
print(f"Boxes placed          : {placed_boxes}")
print(f"Boxes remaining       : {total_boxes - placed_boxes}")
print(f"Placement ratio       : {placed_boxes / total_boxes:.2f}")
print("==============================\n")

print("Final stacking plan:\n")

for i, box in enumerate(env.env.placed_boxes):
    print(
        f"{i+1:02d} → "
        f"Box {box['id']} "
        f"at {box['position']} "
        f"dims={box['dims']}"
    )
