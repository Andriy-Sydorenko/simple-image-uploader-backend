from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from api.models import Image, User


def get_image_by_uuid(image_uuid: str, db: Session) -> Optional[Image]:
    query = select(Image).filter(Image.uuid == UUID(image_uuid))
    result = db.execute(query)
    image = result.scalars().first()
    return image


def get_images_by_user_id(user_id: int, db: Session) -> list[Image]:
    query = select(Image).filter(Image.user_id == user_id)
    result = db.execute(query)
    images = result.scalars().all()
    return list(images)


def create_image(file_name: str, file_size, image_url: str, user: User, db: Session) -> Image:
    image = Image(filename=file_name, file_size=file_size, url=image_url)
    if user:
        image.user_id = user.id
    db.add(image)
    db.commit()
    db.refresh(image)
    return image
