import hashlib
import pathlib
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


def get_thumb(document, width, height, crop):

    if document.file.type.startswith("image"):
        thumb_file_name = os.path.join(
            MEDIA_ROOT, f"{document.file.hash}_thumb_{width}_{height}_{crop}.png",
        )
        path = pathlib.Path(thumb_file_name)
        if not path.is_file():
            image = Image.open(os.path.join(MEDIA_ROOT, document.file.path))
            if crop:
                thumbnail = image.crop((0, 0, width, height))
            else:
                thumbnail = image.resize((width, height))
            thumbnail.save(thumb_file_name)
        return thumb_file_name
    return None
