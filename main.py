from fastapi import FastAPI
import uvicorn

from config.variable import SERVER_PORT
from router.sie_router import router

app = FastAPI()

app.include_router(router, prefix="/api/v1/sie", tags=["Search Image Engine API v1"])

@app.get("/")
async def read_root():
    return {"message": "Search Image Engine API v1"}


if __name__ == "__main__":
    uvicorn.run("server.app:app", host="0.0.0.0", port=SERVER_PORT, reload=True)