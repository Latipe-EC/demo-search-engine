

from fastapi import FastAPI, Depends, security
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import trained_repos
from router.dashboard import dashboard
from router.sie_router import router

from config.variable import SERVER_PORT
from router.sie_router import router


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router, prefix="/api/v1/sie", tags=["Search Image Engine API v1"])
app.include_router(dashboard, prefix='/sie/admin', tags=["Dashboard"])



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


@app.get("/sie/admin/query")
async def read_index():
    return FileResponse('static/query.html')

@app.exception_handler(404)
async def custom_404_handler(_, __):
    return FileResponse('static/404.html')

@app.exception_handler(405)
async def custom_404_handler(_, __):
    return FileResponse('static/404.html')

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=SERVER_PORT, reload=True)