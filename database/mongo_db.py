import motor.motor_asyncio
from bson import ObjectId

import config.variable
from domain.models import BaseProductModel

client = motor.motor_asyncio.AsyncIOMotorClient(config.variable.MONGO_DB_CLIENT)
database = client.get_database('search_image_engine_db')


