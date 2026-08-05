import logging
import uuid

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .processors import ImageProcessor

logger = logging.getLogger(__name__)


class StorageService:
    """Storage service that converts images to WebP format and compresses size."""

    def __init__(self):
        cloudinary_storage = getattr(settings, "CLOUDINARY_STORAGE", None)
        cloud_name = getattr(settings, "CLOUDINARY_CLOUD_NAME", None)
        self.use_cloudinary = bool(cloudinary_storage or cloud_name)

    def upload(self, file_obj, folder=None, max_dimension=1600):
        folder = (folder or "articles/images").strip("/")
        processor = ImageProcessor(quality=80, max_dimension=max_dimension)
        processed = processor.process(file_obj)

        processed_buffer = processed["buffer"]
        processed_size = processed["size"]
        width = processed["width"]
        height = processed["height"]

        if self.use_cloudinary:
            try:
                import cloudinary.uploader

                upload_res = cloudinary.uploader.upload(
                    processed_buffer,
                    folder=folder,
                    format="webp",
                    resource_type="image",
                )
                return {
                    "url": upload_res.get("secure_url") or upload_res.get("url"),
                    "public_id": upload_res.get("public_id", ""),
                    "storage": "cloudinary",
                    "width": upload_res.get("width", width),
                    "height": upload_res.get("height", height),
                    "size": upload_res.get("bytes", processed_size),
                    "format": "webp",
                }
            except Exception as exc:
                logger.warning("Cloudinary upload failed, falling back to default_storage: %s", exc)

        # Local or default file storage fallback
        file_name = f"{folder}/{uuid.uuid4().hex}.webp"
        saved_path = default_storage.save(file_name, ContentFile(processed_buffer.getvalue()))
        url = default_storage.url(saved_path)

        return {
            "url": url,
            "public_id": saved_path,
            "storage": "local",
            "width": width,
            "height": height,
            "size": processed_size,
            "format": "webp",
        }


