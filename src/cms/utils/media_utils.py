import hashlib
import pathlib
import math
import os

from PIL import Image

from cms.models.media.file import File
from backend.settings import MEDIA_ROOT

file_root = MEDIA_ROOT


def delete_document(document):
    file = document.file
    delete_old_file(file)
    document.delete()


def attach_file(document, file):
    sha = hashlib.sha256()
    for chunk in file.chunks():
        sha.update(chunk)
    file_hash = sha.hexdigest()
    existing_file = File.objects.filter(hash=file_hash).first()
    if existing_file:
        file_ref = existing_file
    else:
        with open(os.path.join(MEDIA_ROOT, file_hash), "wb+") as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        file_ref = File()
        file_ref.hash = file_hash
        file_ref.path = file_hash
        file_ref.type = file.content_type
        file_ref.save()

    try:
        old_file = document.file
        delete_old_file(old_file)
    except File.DoesNotExist:
        pass
    document.file = file_ref


def delete_old_file(file):
    if file and file.documents.count() <= 1:
        file.delete()


def get_thumbnail(file, width, height, crop):
    if file.type.startswith("image"):
        thumb_file_name = os.path.join(
            MEDIA_ROOT, f"{file.hash}_thumb_{width}_{height}_{crop}",
        )
        path = pathlib.Path(thumb_file_name)
        if not path.is_file() or True:
            try:
                image = Image.open(os.path.join(MEDIA_ROOT, file.path))
                if crop:
                    original_width = image.width
                    original_height = image.height
                    width_ratio = original_width / width
                    height_ratio = original_height / height
                    if width_ratio < height_ratio:
                        resized_image = image.resize(
                            (width, math.ceil(original_height / width_ratio))
                        )
                    else:
                        resized_image = image.resize(
                            (math.ceil(original_width / height_ratio), height)
                        )
                    offset_x = math.floor(resized_image.width - width) / 2
                    offset_y = math.floor(resized_image.height - height) / 2
                    print(resized_image.width, resized_image.height)
                    thumbnail = resized_image.crop(
                        (offset_x, offset_y, width + offset_x, height + offset_y)
                    )
                else:
                    thumbnail = image.resize((width, height))
                thumbnail.save(thumb_file_name, image.format)
            except IOError:
                return None

        return thumb_file_name
    return None
