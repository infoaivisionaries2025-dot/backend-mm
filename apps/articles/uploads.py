"""
Article image upload utilities.

This module provides backwards-compatible wrappers around the new
MediaService pipeline. New code should use MediaService directly.
"""
import logging

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ValidationError

from apps.media.services import MediaService
from apps.media.storage import StorageService

logger = logging.getLogger(__name__)


def is_cloudinary_configured():
    """Check if Cloudinary storage is configured."""
    return StorageService().use_cloudinary


def upload_article_image(image_file, upload_type="cover"):
    """
    Validate, optimise, and upload an article image.

    This is a backwards-compatible wrapper. Internally it delegates
    to MediaService which handles validation, Pillow processing,
    thumbnail generation, and storage upload.

    Args:
        image_file: Django UploadedFile instance.
        upload_type: One of 'cover', 'editor', 'gallery'.

    Returns:
        dict with at minimum {'url': str, 'public_id': str, 'storage': str}.
        For 'cover' uploads also includes thumbnail/medium/large URLs
        and image metadata.

    Raises:
        ValueError: If the file fails validation.
        ImproperlyConfigured: If storage backend is unavailable.
        RuntimeError: If the upload fails.
    """
    if not is_cloudinary_configured() and not getattr(settings, "DEBUG", True):
        raise ImproperlyConfigured("Cloudinary is required for image uploads in production.")

    folder = "articles/covers" if upload_type == "cover" else "articles/inline"
    service = MediaService(upload_type=upload_type, folder=folder)

    try:
        if upload_type == "cover":
            result = service.process_and_upload(image_file)
        else:
            result = service.upload_single(image_file)
    except ValidationError as exc:
        # Convert Django ValidationError to ValueError for backwards compat
        raise ValueError(str(exc.message if hasattr(exc, 'message') else exc)) from exc
    except Exception as exc:
        logger.exception("Image upload failed for type '%s'", upload_type)
        if "Cloudinary" in str(exc) or "cloudinary" in str(exc).lower():
            raise RuntimeError(f"Cloud storage upload failed: {exc}") from exc
        raise

    return result
