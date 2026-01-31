# from fastapi import FastAPI
# from pydantic import BaseModel
# from typing import List

# from packer_service import pack_items

# app = FastAPI(title="Packwise 3D API")

# class PackRequest(BaseModel):
#     bin: List[float]
#     items: List[List[float]]

# @app.post("/pack")
# def pack_endpoint(req: PackRequest):
#     return pack_items(req.bin, req.items)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from packer_service import pack_items

app = FastAPI(title="Packwise 3D API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PackRequest(BaseModel):
    bin: List[float]
    items: List[List[float]]

@app.post("/pack")
def pack_endpoint(req: PackRequest):
    return pack_items(req.bin, req.items)
