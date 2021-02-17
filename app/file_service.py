import random

from fastapi import UploadFile

from app.custom_expetion import ImageException
import os

allowed_MIME = ["image/jpeg", "image/png"]


# TODO(any): implemant save file in cloud service

def save_file(data: bytes, extension: str):
    name = get_random_string(10) + "." + extension
    file = open(name, "wb")
    file.write(data)
    file.close()
    return name


def get_random_string(length):
    sample_letters = 'abcdefghijklmnopqrstuvwxyz1234567890'
    result_str = ''.join((random.choice(sample_letters) for i in range(length)))
    return result_str


def check_image(image: UploadFile):
    if image.content_type not in allowed_MIME:
        raise ImageException()


async def upload_image(image: UploadFile):
    check_image(image)
    data = await image.read()
    extension = image.filename.split('.')[-1]
    image_url = save_file(data, extension)
    return image_url


async def reupload_image(oldFileSrc: str, image: UploadFile):
    if oldFileSrc != "":
        os.remove(oldFileSrc)
    return await upload_image(image)
