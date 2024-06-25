from bson import ObjectId

from database.mongo_db import database
from domain.models import BaseProductModel

trained_collection = database.get_collection('trained_product')


def trained_product_helper(product) -> BaseProductModel:
    return BaseProductModel(
        id=str(product['_id']),
        product_id=product['product_id'],
        product_name=product['product_name'],
        image_urls=product['image_urls']
    )


async def trained_insert_new_product(entity):
    document = {
        "product_id": entity.product_id,
        "product_name": entity.product_name,
        "image_urls": entity.image_urls
    }
    product = await trained_collection.insert_one(document)



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
    return product.deleted_count