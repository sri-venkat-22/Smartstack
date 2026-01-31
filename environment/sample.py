from env_init import PackingEnvironment

env = PackingEnvironment(seed=42)

json_data = {
    "boxes": [
        {
            "id": 21,
            "dims": [0.6, 0.4, 0.3],
            "weight": 12,
            "fragile": True,
            "priority": 2
        },
        {
            "id": 22,
            "dims": [0.8, 0.5, 0.4],
            "weight": 18,
            "fragile": False,
            "priority": 1
        }
    ]
}

state = env.reset(mode="json", json_data=json_data)

print(state)
