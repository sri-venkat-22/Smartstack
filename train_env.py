import numpy as np
import os

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.policies import MaskableActorCriticPolicy
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.torch_layers import CombinedExtractor

from environment.env_init import PackingEnvironment
from gym_env import HybridPackingEnv


# =====================================================
# Create environment
# =====================================================

base_env = PackingEnvironment(
    container_dims=(3.0, 3.0, 3.0),
    seed=42
)

env = HybridPackingEnv(
    base_env=base_env,
    max_candidates=50
)


# =====================================================
# Policy kwargs (✅ CORRECT FOR YOUR SB3 VERSION)
# =====================================================

policy_kwargs = dict(
    features_extractor_class=CombinedExtractor,
    net_arch=[256, 256]
)


# =====================================================
# Checkpoint callback
# =====================================================

checkpoint_callback = CheckpointCallback(
    save_freq=20_000,
    save_path="./checkpoints/",
    name_prefix="binpack_ppo"
)


# =====================================================
# Train PPO
# =====================================================

model = MaskablePPO(
    policy=MaskableActorCriticPolicy,
    env=env,
    policy_kwargs=policy_kwargs,   # ✅ FIXED
    verbose=1,
    learning_rate=3e-4,
    n_steps=2048,
    batch_size=256,
    gamma=0.99,
    ent_coef=0.01,
    tensorboard_log="./tensorboard/",
    device="auto"
)

model.learn(
    total_timesteps=500_000,
    callback=checkpoint_callback
)

model.save("binpack_final")
