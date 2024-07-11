import datetime
import os
import shutil
from datetime import time

from bson import ObjectId

from config.variable import RETRIVAL_DB_FEATURE_FOLDER
from database.mongo_db import database
from domain.models import BaseProductModel

trained_collection = database.get_collection('trained_product')


def trained_product_helper(product) -> BaseProductModel:
    return BaseProductModel(
        id=str(product['_id']),
        product_id=product['product_id'],
        product_name=product['product_name'],
        image_urls=product['image_urls'],
        created_date=product.get('created_date', '10/07/2024')
    )


async def trained_insert_new_product(entity):
    document = {
        "product_id": entity.product_id,
        "product_name": entity.product_name,
        "image_urls": entity.image_urls,
        "created_date": datetime.datetime.now()
    }
    await trained_collection.insert_one(document)


async def trained_find_by_id(id) -> BaseProductModel:
    product = await trained_collection.find_one({'_id': ObjectId(id)})
    if product:
        return trained_product_helper(product)


async def trained_find_by_productId(product_id) -> BaseProductModel:
    product = await trained_collection.find_one({'product_id': product_id})
    if product:
        return trained_product_helper(product)


async def trained_find_all_in_query(product_ids: list):
    products = []
    async for p in trained_collection.find({"product_id": {"$in": product_ids}}):
        products.append(trained_product_helper(p))
    return products


async def delete_trained_product(product_id: str):
    product = await trained_collection.delete_one({'product_id': product_id})

    img_folder_path = os.path.join(RETRIVAL_DB_FEATURE_FOLDER, product_id)
    if os.path.exists(img_folder_path):
        shutil.rmtree(img_folder_path)

    return product.deleted_count


async def trained_find_all(page: int, limit: int):
    products = []
    async for p in trained_collection.find().skip(page * limit).limit(limit).sort("created_date", -1):
        products.append(trained_product_helper(p))
    return products


#count of total product
async def trained_count_all():
    return await trained_collection.count_documents({})
