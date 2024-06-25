from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field


class PrepareTrainingProductRequest(BaseModel):
    product_id: str
    product_name: str
    image_urls: List[str]
    skip: Optional[bool] = Field(False)

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "1",
                "product_name": "Product 1",
                "image_urls": ["https://image1.jpg", "https://image2.jpg"],
                "skip": False
            }
        }


def ResponseSuccessModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ResponseErrorModel(data, message, code=400):
    return {
        "data": data,
        "code": code,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}
