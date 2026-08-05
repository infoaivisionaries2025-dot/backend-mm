from .storage import StorageService


class MediaService:
    """Compatibility shim for article image upload processing."""

    def __init__(self, upload_type="cover", folder=None):
        self.upload_type = upload_type
        self.folder = folder
        self.storage = StorageService()

    def process_and_upload(self, image_file):
        res = self.storage.upload(image_file, folder=self.folder)
        url = res.get("url", "")
        return {
            "url": url,
            "public_id": res.get("public_id", ""),
            "storage": res.get("storage", "local"),
            "thumbnail_url": res.get("thumbnail_url", url),
            "medium_url": res.get("medium_url", url),
            "large_url": res.get("large_url", url),
            "width": res.get("width"),
            "height": res.get("height"),
            "size": res.get("size", getattr(image_file, "size", None)),
            "format": res.get("format", ""),
        }

    def upload_single(self, image_file):
        res = self.storage.upload(image_file, folder=self.folder)
        return {
            "url": res.get("url", ""),
            "public_id": res.get("public_id", ""),
            "storage": res.get("storage", "local"),
            "width": res.get("width"),
            "height": res.get("height"),
            "size": res.get("size", getattr(image_file, "size", None)),
            "format": res.get("format", ""),
        }

