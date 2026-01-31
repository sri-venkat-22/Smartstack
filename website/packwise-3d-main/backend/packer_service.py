# # # from py3dbp import Packer, Bin, Item

# # # def pack_items(bin_dims, items):
# # #     packer = Packer()

# # #     packer.addBin(
# # #         Bin("Main Bin", tuple(bin_dims), 100)
# # #     )

# # #     for i, dims in enumerate(items):
# # #         packer.addItem(
# # #             Item(
# # #                 name=f"Item {i+1}",
# # #                 partno=f"P{i+1}",
# # #                 typeof="cube",
# # #                 WHD=tuple(dims),
# # #                 weight=1,
# # #                 level=1,
# # #                 loadbear=100,
# # #                 updown=True,
# # #                 color="blue"
# # #             )
# # #         )

# # #     packer.pack()

# # #     packed = []
# # #     for item in packer.bins[0].items:
# # #         packed.append({
# # #             "name": item.name,
# # #             "position": item.position,
# # #             "dimensions": [item.width, item.height, item.depth]
# # #         })

# # #     return {
# # #         "bin": bin_dims,
# # #         "packed_items": packed
# # #     }




# # from py3dbp import Packer, Bin, Item


# # def pack_items(bin_dims, items):
# #     packer = Packer()

# #     # ---- Add Bin ----
# #     packer.addBin(
# #         Bin("Main Bin", tuple(bin_dims), 100)
# #     )

# #     # ---- IMPROVED HEURISTIC ----
# #     # 1. Attach metadata
# #     indexed_items = []
# #     for i, dims in enumerate(items):
# #         w, h, d = dims

# #         # Largest footprint first (prevents vertical pillars)
# #         footprint = max(
# #             w * d,  # width × depth
# #             h * d,  # height × depth
# #             w * h   # width × height
# #         )

# #         indexed_items.append({
# #             "index": i,
# #             "dims": (w, h, d),
# #             "footprint": footprint
# #         })

# #     # 2. Sort by footprint (descending)
# #     indexed_items.sort(key=lambda x: x["footprint"], reverse=True)

# #     # 3. Add items in sorted order
# #     for item in indexed_items:
# #         i = item["index"]
# #         w, h, d = item["dims"]

# #         packer.addItem(
# #             Item(
# #                 name=f"Item {i+1}",
# #                 partno=f"P{i+1}",
# #                 typeof="cube",
# #                 WHD=(w, h, d),
# #                 weight=1,
# #                 level=1,
# #                 loadbear=100,
# #                 updown=True,
# #                 color="blue"
# #             )
# #         )

# #     # ---- PACK ----
# #     packer.pack()

# #     # ---- OUTPUT FORMAT ----
# #     packed = []
# #     for item in packer.bins[0].items:
# #         packed.append({
# #             "name": item.name,
# #             "position": list(item.position),
# #             "dimensions": [item.width, item.height, item.depth]
# #         })

# #     return {
# #         "bin": bin_dims,
# #         "packed_items": packed
# #     }




# from py3dbp import Packer, Bin, Item
# import random
# import math


# def score_packing(bin_dims, packed_items):
#     """
#     Lower score = better packing
#     """
#     bin_volume = bin_dims[0] * bin_dims[1] * bin_dims[2]

#     used_volume = 0
#     max_height_used = 0
#     vertical_pillars = 0

#     for item in packed_items:
#         w, h, d = item["dimensions"]
#         x, y, z = item["position"]

#         used_volume += w * h * d
#         max_height_used = max(max_height_used, z + h)

#         # Detect tall vertical blockers
#         if h > bin_dims[1] * 0.6 and z == 0:
#             vertical_pillars += 1

#     empty_volume = bin_volume - used_volume

#     # Final heuristic score
#     score = (
#         empty_volume * 1.5 +
#         max_height_used * 2.0 +
#         vertical_pillars * 50.0
#     )

#     return score


# def run_single_pack(bin_dims, items):
#     packer = Packer()
#     packer.add_bin(Bin("Main Bin", tuple(bin_dims), 100))

#     for i, dims in enumerate(items):
#         w, h, d = dims
#         packer.addItem(
#             Item(
#                 name=f"Item {i+1}",
#                 partno=f"P{i+1}",
#                 typeof="cube",
#                 WHD=(w, h, d),
#                 weight=1,
#                 level=1,
#                 loadbear=100,
#                 updown=True,
#                 color="blue"
#             )
#         )

#     packer.pack()

#     packed = []
#     for item in packer.bins[0].items:
#         packed.append({
#             "name": item.name,
#             "position": list(item.position),
#             "dimensions": [item.width, item.height, item.depth]
#         })

#     return packed


# def pack_items(bin_dims, items):
#     """
#     Phase 1: Multi-run heuristic selection
#     """
#     strategies = []

#     # Strategy 1: Original order
#     strategies.append(items)

#     # Strategy 2: Largest volume first
#     strategies.append(
#         sorted(items, key=lambda d: d[0] * d[1] * d[2], reverse=True)
#     )

#     # Strategy 3: Largest footprint first
#     strategies.append(
#         sorted(
#             items,
#             key=lambda d: max(d[0] * d[2], d[1] * d[2], d[0] * d[1]),
#             reverse=True
#         )
#     )

#     # Strategy 4–6: Random shuffles
#     for _ in range(3):
#         shuffled = items[:]
#         random.shuffle(shuffled)
#         strategies.append(shuffled)

#     best_score = math.inf
#     best_packing = None

#     for strategy in strategies:
#         packed_items = run_single_pack(bin_dims, strategy)

#         if not packed_items:
#             continue

#         score = score_packing(bin_dims, packed_items)

#         if score < best_score:
#             best_score = score
#             best_packing = packed_items

#     return {
#         "bin": bin_dims,
#         "packed_items": best_packing
#     }




from py3dbp import Packer, Bin, Item
import random
import math


# ---------- SCORING FUNCTION ----------
def score_packing(bin_dims, packed_items):
    # Force everything to float (py3dbp uses Decimal internally)
    bw, bh, bd = map(float, bin_dims)
    bin_volume = bw * bh * bd

    used_volume = 0.0
    max_height_used = 0.0
    vertical_pillars = 0

    for item in packed_items:
        w, h, d = map(float, item["dimensions"])
        x, y, z = map(float, item["position"])

        used_volume += w * h * d
        max_height_used = max(max_height_used, z + h)

        # Penalize tall items starting from the floor
        if h > bh * 0.6 and z == 0:
            vertical_pillars += 1

    empty_volume = bin_volume - used_volume

    return (
        empty_volume * 1.5
        + max_height_used * 2.0
        + vertical_pillars * 50.0
    )


# ---------- SINGLE PACK RUN ----------
def run_single_pack(bin_dims, items):
    bw, bh, bd = map(float, bin_dims)

    packer = Packer()
    packer.add_bin(Bin("Main Bin", bw, bh, bd, 100))

    for i, (w, h, d) in enumerate(items):
        packer.add_item(
            Item(
                f"Item {i+1}",
                float(w),
                float(h),
                float(d),
                1
            )
        )

    packer.pack()

    packed = []
    for item in packer.bins[0].items:
        packed.append({
            "name": item.name,
            "position": list(map(float, item.position)),
            "dimensions": [
                float(item.width),
                float(item.height),
                float(item.depth),
            ],
        })

    return packed


# ---------- MULTI-RUN HEURISTIC PACK ----------
def pack_items(bin_dims, items):
    # Ensure input is float-only
    bin_dims = list(map(float, bin_dims))
    items = [list(map(float, i)) for i in items]

    strategies = []

    # Strategy 1: original order
    strategies.append(items)

    # Strategy 2: largest volume first
    strategies.append(
        sorted(items, key=lambda d: d[0] * d[1] * d[2], reverse=True)
    )

    # Strategy 3: largest footprint first
    strategies.append(
        sorted(
            items,
            key=lambda d: max(
                d[0] * d[1],
                d[0] * d[2],
                d[1] * d[2]
            ),
            reverse=True
        )
    )

    # Strategy 4–6: random shuffles
    for _ in range(3):
        shuffled = items[:]
        random.shuffle(shuffled)
        strategies.append(shuffled)

    best_score = math.inf
    best_packing = None

    for strategy in strategies:
        packed_items = run_single_pack(bin_dims, strategy)
        if not packed_items:
            continue

        score = score_packing(bin_dims, packed_items)
        if score < best_score:
            best_score = score
            best_packing = packed_items

    return {
        "bin": bin_dims,
        "packed_items": best_packing
    }
