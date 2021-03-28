from fastapi import UploadFile
from sqlalchemy.orm import Session

from .. import models
from ..file_service import upload_image


async def create_image(db: Session, post_id: int, image: UploadFile):
    image_url = await upload_image(image)

    db_item = models.Images(
        url=image_url,
        post_id=post_id
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
