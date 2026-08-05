import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from apps.articles.models import Tag
from django.template.defaultfilters import slugify

tags = [
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Genetics",
    "Startups",
    "Venture Capital",
    "Physics",
    "Chemistry",
    "Software Architecture",
    "Cloud Computing",
    "Web Development",
    "Cybersecurity",
    "Data Engineering",
    "Product Strategy",
    "Digital Marketing",
    "Public Health",
]

created_count = 0
for name in tags:
    slug = slugify(name)
    _, created = Tag.objects.get_or_create(name=name, defaults={'slug': slug})
    if created:
        created_count += 1

print(f"Tags synced successfully ({created_count} new tags created, total: {Tag.objects.count()}).")
