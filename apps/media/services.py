class MediaService:
    """Compatibility shim for article image upload processing."""

    def __init__(self, upload_type="cover", folder=None):
        self.upload_type = upload_type
        self.folder = folder

    def process_and_upload(self, image_file):
        return {
            "url": "",
            "public_id": "",
            "storage": "local",
            "thumbnail_url": "",
            "medium_url": "",
            "large_url": "",
            "width": None,
            "height": None,
            "size": getattr(image_file, "size", None),
            "format": "",
        }

    def upload_single(self, image_file):
        return {
            "url": "",
            "public_id": "",
            "storage": "local",
            "width": None,
            "height": None,
            "size": getattr(image_file, "size", None),
            "format": "",
        }
