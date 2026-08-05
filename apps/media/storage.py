from django.conf import settings


class StorageService:
    """Small compatibility wrapper around the configured storage backend."""

    def __init__(self):
        self.use_cloudinary = bool(getattr(settings, "CLOUDINARY_STORAGE", None))

    def upload(self, file_obj, folder=None):
        return {
            "url": "",
            "public_id": "",
            "storage": "cloudinary" if self.use_cloudinary else "local",
        }

