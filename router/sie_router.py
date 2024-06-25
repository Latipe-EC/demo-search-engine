from PIL import Image
from fastapi import APIRouter, Body, Request, UploadFile
from fastapi.encoders import jsonable_encoder
from fastapi.params import Form, File
import io

from database.untrained_repos import untrained_insert_new_product
from database.trained_repos import trained_find_by_id, trained_find_by_productId, trained_insert_new_product, \
    delete_trained_product, trained_find_all_in_query
from domain.dto import PrepareTrainingProductRequest, ResponseSuccessModel, ResponseErrorModel

from engine_service.extractor_exec import extractor_exec_product_image_db
from engine_service.search_engine import SearchEngine

router = APIRouter()
se = SearchEngine()


@router.get("/search")
async def search():
    return {"message": "Hello World"}


@router.post("")
async def create_untrained_product(dto: PrepareTrainingProductRequest = Body(...)):
    product = await trained_find_by_productId(dto.product_id)
    print(product)
    if product and dto.skip == False:
        return ResponseErrorModel(None, "Product already exists.")

    count = await delete_trained_product(dto.product_id)
    if count == 0:
        return ResponseErrorModel(None, "Failed to change")

    await trained_insert_new_product(dto)
    await extractor_exec_product_image_db(dto.dict())

    return ResponseSuccessModel(None, "Product added successfully.")



@router.post("/search")
async def search(image_request: UploadFile = File(...), size: int = Form(9)):
    img_file = await image_request.read()
    img = Image.open(io.BytesIO(img_file))

    if se is None:
        raise ResponseErrorModel(None, "Search engine is not initialized yet. Please wait and try again.", 500)

    results, _ = se.search(img, size)
    print(results)

    product_ids = []
    for i in range(len(results)):
        product_id = results[i].parent.name
        product_ids.append(product_id)
        print(product_ids)

    products = await trained_find_all_in_query(product_ids)

    return ResponseSuccessModel(products, "Search completed successfully.")
