from bson import ObjectId

from database.mongo_db import database
from domain.dto import PrepareTrainingProductRequest
from domain.models import BaseProductModel

untrained_product = database.get_collection('untrained_product')


def untrained_product_helper(product) -> BaseProductModel:
    return BaseProductModel(
        id=str(product['_id']),
        product_id=product['product_id'],
        product_name=product['product_name'],
        image_urls=product['image_urls']
    )


async def untrained_insert_new_product(entity: PrepareTrainingProductRequest) -> BaseProductModel:
    document = {
        "product_id": entity.product_id,
        "product_name": entity.product_name,
        "image_urls": entity.image_urls
    }

    product = await untrained_product.insert_one(document)
    new_entity = await untrained_product.find_one({"_id": product.inserted_id})
    return untrained_product_helper(new_entity)


async def untrained_find_by_id(product_id) -> BaseProductModel:
    product = await untrained_product.find_one({'_id': ObjectId(product_id)})

    if product:
        return untrained_product_helper(product)


async def untrained_find_all():
    products = []

    async for p in untrained_product.find():
        products.append(untrained_product_helper(p))

    return products
