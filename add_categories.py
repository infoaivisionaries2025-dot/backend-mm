import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.core.management import call_command

call_command('seed_categories')
print("Done.")
