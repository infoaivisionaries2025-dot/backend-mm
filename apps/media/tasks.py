import os
import logging
from celery import shared_task
from django.conf import settings

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3, default_retry_delay=10)
def process_uploaded_image(self, file_path, upload_type, model_name, instance_id):
    from apps.media.services import MediaService
    from apps.articles.models import Article
    from apps.users.models import CustomUser

    try:
        if not os.path.exists(file_path):
            logger.error(f"File not found: {file_path}")
            return False

        with open(file_path, 'rb') as file_obj:
            folder = 'articles/covers' if upload_type == 'cover' else 'users/avatars'
            service = MediaService(upload_type=upload_type, folder=folder)
            result = service.process_and_upload(file_obj)

        if model_name == 'article':
            try:
                article = Article.objects.get(id=instance_id)
                article.cover_image = result.get('original')
                article.cover_image_thumbnail = result.get('thumbnail')
                article.cover_image_medium = result.get('medium')
                article.cover_image_large = result.get('large')
                article.cover_image_width = result.get('width')
                article.cover_image_height = result.get('height')
                article.cover_image_size = result.get('size')
                article.cover_image_format = result.get('format')
                article.save(update_fields=[
                    'cover_image', 'cover_image_thumbnail', 'cover_image_medium',
                    'cover_image_large', 'cover_image_width', 'cover_image_height',
                    'cover_image_size', 'cover_image_format'
                ])
            except Article.DoesNotExist:
                logger.error(f"Article {instance_id} not found")

        elif model_name == 'user':
            try:
                user = CustomUser.objects.get(id=instance_id)
                user.avatar = result.get('original')
                user.avatar_thumbnail = result.get('thumbnail')
                user.save(update_fields=['avatar', 'avatar_thumbnail'])
            except CustomUser.DoesNotExist:
                logger.error(f"User {instance_id} not found")

        os.remove(file_path)
        logger.info(f"Successfully processed image {file_path} for {model_name} {instance_id}")
        return True

    except Exception as exc:
        logger.error(f"Error processing image {file_path}: {exc}")
        try:
            self.retry(exc=exc, countdown=2 ** self.request.retries * 10)
        except self.MaxRetriesExceededError:
            logger.error(f"Max retries exceeded for processing {file_path}")
            if os.path.exists(file_path):
                os.remove(file_path)
            raise


@shared_task
def cleanup_old_image(public_id, storage_type='cloudinary'):
    from apps.media.services import StorageService
    try:
        StorageService.delete(public_id, storage_type=storage_type)
        logger.info(f"Successfully deleted image: {public_id}")
        return True
    except Exception as exc:
        logger.error(f"Error deleting image {public_id}: {exc}")
        return False

@shared_task
def cleanup_orphan_images():
    logger.info("Orphan image cleanup is not yet configured. Use the management command for manual cleanup.")
    return True
