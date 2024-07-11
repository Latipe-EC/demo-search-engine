import json
from typing import Annotated

from fastapi import FastAPI, HTTPException, Body, responses, status, Form

from fastapi import Request, APIRouter, Query, Depends, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from database import trained_repos
from database.trained_repos import delete_trained_product
from engine_service.se_context import se_context

security = HTTPBasic()

# Định nghĩa thông tin xác thực
USERNAME = "admin"
PASSWORD = "Devdeptrai@2024"

templates = Jinja2Templates(directory="static/templates")
dashboard = APIRouter()


def verification(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@dashboard.get("/dashboard", response_class=HTMLResponse)
async def load_dashboard(request: Request, page: int = 0,
                         size: int = 15, errorCode: int = 0, successCode: int = 0, verification=Depends(verification)):
    products = await trained_repos.trained_find_all(page, size)
    print(products)
    if page == 0:
        current_page = 1
    else:
        current_page = page
    total = await trained_repos.trained_collection.count_documents({})
    total_pages = int(total / size)
    return templates.TemplateResponse(request=request, name="dashboard.html",
                                      context={
                                          "products": products,
                                          "total": total,
                                          "current_page": current_page,
                                          "total_pages": total_pages,
                                          "errorCode": errorCode,
                                          "successCode": successCode
                                      })
@dashboard.post("/dashboard", response_class=HTMLResponse)
async def load_dashboard_post(request: Request, page: int = 0,
                         size: int = 15, errorCode: int = 0, successCode: int = 0, verification=Depends(verification)):
    products = await trained_repos.trained_find_all(page, size)
    print(products)
    if page == 0:
        current_page = 1
    else:
        current_page = page
    total = await trained_repos.trained_collection.count_documents({})
    total_pages = int(total / size)
    return templates.TemplateResponse(request=request, name="dashboard.html",
                                      context={
                                          "products": products,
                                          "total": total,
                                          "current_page": current_page,
                                          "total_pages": total_pages,
                                          "errorCode": errorCode,
                                          "successCode": successCode
                                      })

@dashboard.get("/get-by-id", response_class=HTMLResponse)
async def get_by_id(request: Request, productId: str):
    products = []
    if productId is not None:
        return RedirectResponse(f"/sie/admin/dashboard?errorCode=01")

    p = await trained_repos.trained_find_by_productId(productId)
    if p is not None:
        return RedirectResponse(f"/sie/admin/dashboard?errorCode=01")
    products.append(p)
    current_page = 1

    total = 1
    total_pages = 1
    return templates.TemplateResponse(request=request, name="dashboard.html",
                                      context={
                                          "products": products,
                                          "total": total,
                                          "current_page": current_page,
                                          "total_pages": total_pages
                                      })


@dashboard.post("/delete", response_class=HTMLResponse)
async def del_trained_product(productId: Annotated[str, Form()]):
    if productId is None:
        return RedirectResponse("/sie/admin/dashboard?errorCode=01", status_code=307)
    print(f'DEL:{productId}')
    count = await delete_trained_product(productId)
    if count == 0:
        return RedirectResponse("/sie/admin/dashboard?errorCode=01", status_code=307)
    se_context.update_instance()

    return RedirectResponse("/sie/admin/dashboard?successCode=01", status_code=307)
