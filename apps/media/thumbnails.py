import logging
from django.conf import settings
from .processors import ImageProcessor
from PIL import Image

logger = logging.getLogger(__name__)

class ThumbnailGenerator:
    """Generate multiple thumbnail variants for an image."""

    def __init__(self, sizes=None):
        self.sizes = sizes or getattr(
            settings, 
            'MEDIA_THUMBNAIL_SIZES', 
            {'thumbnail': 300, 'medium': 800, 'large': 1600}
        )

    def generate(self, file_obj):
        """
        Generate variants based on configured sizes.
        Skips sizes that are larger than the source image.
        """
        results = {}
        
        try:
            with Image.open(file_obj) as img:
                orig_width, orig_height = img.size
            max_orig_dim = max(orig_width, orig_height)
        except Exception as e:
            logger.error(f"Failed to read image dimensions for thumbnails: {str(e)}")
            raise
            
        file_obj.seek(0)

        for name, size in self.sizes.items():
            if size >= max_orig_dim and name != 'large':
                # Skip smaller variants if original is already small
                logger.info(f"Skipping variant '{name}' ({size}px) as source is {max_orig_dim}px.")
                continue
                
            processor = ImageProcessor(max_dimension=size)
            try:
                # Need to read from original file_obj for each variant
                file_obj.seek(0)
                variant_data = processor.process(file_obj)
                results[name] = variant_data
            except Exception as e:
                logger.error(f"Failed to generate thumbnail '{name}': {str(e)}")
                raise

        # Reset file_obj when done
        file_obj.seek(0)
        
        return results
