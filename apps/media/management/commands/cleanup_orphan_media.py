from django.core.management.base import BaseCommand
import logging
from apps.articles.models import Article
from apps.users.models import CustomUser

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Find and optionally remove media files not referenced by any database record.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            default=True,
            help='Just report, do not delete'
        )
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Actually delete orphan media'
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        if options['delete']:
            dry_run = False

        article_covers = Article.objects.exclude(cover_image='').values_list('cover_image', flat=True)
        user_avatars = CustomUser.objects.exclude(avatar='').values_list('avatar', flat=True)
        
        referenced_count = article_covers.count() + user_avatars.count()
        
        logger.info(f"Total referenced images found: {referenced_count}")
        self.stdout.write(self.style.SUCCESS(f"Total referenced images found: {referenced_count}"))
        
        message = "Note: Full orphan detection requires listing all files in storage (Cloudinary API or S3 list). Full orphan detection requires storage provider API access."
        logger.info(message)
        self.stdout.write(self.style.WARNING(message))
        
        if not dry_run:
            self.stdout.write(self.style.WARNING("Deletion mode is not fully implemented for orphans yet."))
