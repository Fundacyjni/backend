from fastapi import UploadFile
from sqlalchemy.orm import Session

from .. import models
from ..file_service import upload_image, reupload_image


def get_image_by_id(db: Session, image_id: int):
    return db.query(models.Images).filter(models.Images.id == image_id).first()


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


def delete_image(db: Session, image: models.Images):
    db.delete(image)
    db.commit()


async def edit_image(db: Session, img: models.Images, image: UploadFile):
    new_url = await reupload_image(img.url, image)
    img.url = new_url
    db.commit()
