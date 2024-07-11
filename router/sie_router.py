import io

import requests
from PIL import Image
from fastapi import APIRouter, Body, Request, UploadFile
from fastapi.params import Form, File
from fastapi import BackgroundTasks,HTTPException

from config.variable import X_API_KEY, PRODUCT_SERVICE_URL
from database.trained_repos import trained_find_by_productId, trained_insert_new_product, \
    delete_trained_product, trained_find_all_in_query
from database.untrained_repos import untrained_find_by_productId, \
    untrained_delete_by_productId, untrained_find_all
from domain.dto import PrepareTrainingProductRequest, ResponseSuccessModel, ResponseErrorModel
from engine_service.extractor_exec import extractor_exec_product_image_db
from engine_service.se_context import se_context

router = APIRouter()


@router.post("/webhook/trigger-training")
async def trigger_training(request: Request, background_tasks: BackgroundTasks):
    x_api_key = request.headers.get("x-api-key")

    if x_api_key != X_API_KEY:
        return ResponseErrorModel(None, "Unauthorized", 401)

    background_tasks.add_task(train)

    return ResponseSuccessModel(None, "Training started successfully.")


async def train():
    products = await untrained_find_all()

    product_pretrained = [product for product in products if 'image_urls' in product]
    product_not_pretrained = [product for product in products if 'image_urls' not in product]

    response = requests.post(f'{PRODUCT_SERVICE_URL}/products-es-multiple', headers={
        "Content-Type": "application/json"
    }, json={"product_ids": [product.product_id for product in product_not_pretrained]})

    if response.status_code != 200:
        return ResponseErrorModel(None, "Failed to fetch product details", 500)

    product_pretrained.extend(response.json())

    products = [{'id' if k == 'product_id' else k: v for k, v in product.items()} for product in
                product_pretrained]

    print(f'Start training {len(products)} products')
    for product in products:
        await extractor_exec_product_image_db({
            "product_id": product['id'],
            "product_name": product['product_name'],
            "image_urls": product['image_urls']
        })
        await trained_insert_new_product(PrepareTrainingProductRequest(
            product_id=product['id'],
            product_name=product['product_name'],
            image_urls=product['image_urls']
        ))
        se_context.update_instance()
        print(f"Product {product['id']} trained successfully.")

@router.post("/search")
async def search(image_request: UploadFile = File(...), size: int = Form(9)):
    img_file = await image_request.read()
    img = Image.open(io.BytesIO(img_file))

    if se_context is None:
        raise ResponseErrorModel(None, "Search engine is not initialized yet. Please wait and try again.", 500)

    results, _ = se_context.search(img, size)
    print(results)

    product_ids = []
    for i in range(len(results)):
        product_id = results[i].parent.name
        product_ids.append(product_id)
        print(product_ids)

    products = await trained_find_all_in_query(product_ids)

    return ResponseSuccessModel(products, "Search completed successfully.")


@router.post("/untrained")
async def training_new_product(dto: PrepareTrainingProductRequest = Body(...)):
    product = await trained_find_by_productId(dto.product_id)
    print(product)
    if product:
        if dto.skip is False:
            raise HTTPException(status_code=400, detail="Product already exists")

        count = await delete_trained_product(dto.product_id)
        if count == 0:
            raise HTTPException(status_code=400, detail="Failed to change")

    await trained_insert_new_product(dto)
    await extractor_exec_product_image_db(dto.model_dump())
    se_context.update_instance()

    return ResponseSuccessModel(None, "Product added successfully.")


@router.delete("/trained/product/{product_id}")
async def delete_trained_product_by_id(product_id: str):
    count = await delete_trained_product(product_id)
    if count == 0:
        return ResponseErrorModel(None, "Product not found.", 404)
    se_context.update_instance()
    return ResponseSuccessModel(None, "Product deleted successfully.")


@router.delete("/untrained/product/{product_id}")
async def delete_untrained_product_by_id(product_id: str):
    count = await untrained_delete_by_productId(product_id)
    if count == 0:
        return ResponseErrorModel(None, "Product not found.", 404)

    se_context.update_instance()
    return ResponseSuccessModel(None, "Product deleted successfully.")


@router.get("/trained/product/{product_id}")
async def get_trained_product_by_id(product_id: str):
    product = await trained_find_by_productId(product_id)
    if product is None:
        return ResponseErrorModel(None, "Product not found.", 404)
    return ResponseSuccessModel(product, "Product found successfully.")


@router.get("/untrained/product/{id}")
async def get_untrained_product_by_id(id: str):
    product = await untrained_find_by_productId(id)
    if product is None:
        return ResponseErrorModel(None, "Product not found.", 404)
    return ResponseSuccessModel(product, "Product found successfully.")
