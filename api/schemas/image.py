from uuid import UUID

from pydantic import BaseModel


class ImageResponseSchema(BaseModel):
    image_uuid: UUID
    image_url: str
    filename: str
    file_size: float
    upload_time: str


class ImageListResponseSchema(BaseModel):
    images: list[ImageResponseSchema]
