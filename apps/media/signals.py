import logging
from django.db import transaction
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from apps.articles.models import Article
from apps.media.tasks import cleanup_old_image

logger = logging.getLogger(__name__)

@receiver(pre_save, sender=Article)
def handle_cover_image_change(sender, instance, **kwargs):
    if not instance.pk or getattr(instance, '_state', None) and instance._state.adding:
        return

    try:
        old_instance = Article.objects.get(pk=instance.pk)
        if old_instance.cover_image and old_instance.cover_image != instance.cover_image:
            old_image_url = old_instance.cover_image
            logger.info(f"Article {instance.pk} cover image changed. Queuing deletion for {old_image_url}")
            transaction.on_commit(lambda: cleanup_old_image.delay(old_image_url))
    except Article.DoesNotExist:
        pass

@receiver(post_delete, sender=Article)
def handle_article_delete(sender, instance, **kwargs):
    if instance.cover_image:
        logger.info(f"Article {instance.pk} deleted. Queuing deletion for cover image {instance.cover_image} and its variants.")
        cleanup_old_image.delay(instance.cover_image)
        if getattr(instance, 'cover_image_thumbnail', None):
            cleanup_old_image.delay(instance.cover_image_thumbnail)
        if getattr(instance, 'cover_image_medium', None):
            cleanup_old_image.delay(instance.cover_image_medium)
        if getattr(instance, 'cover_image_large', None):
            cleanup_old_image.delay(instance.cover_image_large)
