import asyncio
import json

from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from config.variable import SERVER_PORT
from database.untrained_repos import untrained_insert_new_product, sync_insert_new_product
from domain.dto import PrepareTrainingProductRequest
from router.sie_router import router

import os

os.environ['XLA_FLAGS'] = '--xla_gpu_strict_conv_algorithm_picker=false'
os.environ['CUDA_DIR'] = '/opt/cuda'
os.environ['XLA_FLAGS'] = '--xla_gpu_cuda_data_dir=/opt/cuda'
os.environ['TF_XLA_FLAGS'] = '--tf_xla_auto_jit=2'

app = FastAPI()

app.include_router(router, prefix="/api/v1/sie", tags=["Search Image Engine API v1"])



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def read_root():
    return {"message": "Search Image Engine API v1"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=SERVER_PORT, reload=True)