from PIL import Image
from fastapi import APIRouter, Body, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.params import Form, File
import io


from database.untrained_repos import untrained_insert_new_product, untrained_find_by_productId, \
    untrained_delete_by_productId
from database.trained_repos import trained_find_by_id, trained_find_by_productId, trained_insert_new_product, \
    delete_trained_product, trained_find_all_in_query
from domain.dto import PrepareTrainingProductRequest, ResponseSuccessModel, ResponseErrorModel

from engine_service.extractor_exec import extractor_exec_product_image_db
from engine_service.search_engine_context import se_context

router = APIRouter()



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
            return ResponseErrorModel(None, "Product already exists.")

        count = await delete_trained_product(dto.product_id)
        if count == 0:
            return ResponseErrorModel(None, "Failed to change")

    await trained_insert_new_product(dto)
    await extractor_exec_product_image_db(dto.dict())
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
