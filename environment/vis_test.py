from env_init import PackingEnvironment
from visualisation import visualize_environment

env = PackingEnvironment(seed=1)

env.reset(mode="random")

# mock some placed boxes
env.placed_boxes = [
    {
        "id": 0,
        "dims": (1.0, 0.5, 0.4),
        "position": (0, 0, 0),
        "fragile": False
    },
    {
        "id": 1,
        "dims": (0.6, 0.4, 0.3),
        "position": (1.0, 0, 0),
        "fragile": True
    }
]

visualize_environment(env)
