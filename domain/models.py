import uuid
from fastapi.encoders import jsonable_encoder
from typing import List
from pydantic import BaseModel, Field


class BaseProductModel(BaseModel):
    id: str = Field(None, alias="id")
    product_id: str = Field(...)
    product_name: str = Field(...)
    image_urls: List[str]

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "product_id": "1",
                "product_name": "product_name",
                "image_urls": ["https://image1.jpg", "https://image2.jpg"]
            }
        }


