import uuid
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from pydantic import BaseModel, Field


class BaseProductModel(BaseModel):
    id: str = Field(None, alias="id")
    product_id: str = Field(...)
    product_name: Optional[str] = Field(None)
    image_urls: Optional[List[str]] = []

    class Config:
        json_schema_extra = {
            "example": {
                "id": "1",
                "product_id": "1",
                "product_name": "product_name",
                "image_urls": ["https://image1.jpg", "https://image2.jpg"]
            }
        }


