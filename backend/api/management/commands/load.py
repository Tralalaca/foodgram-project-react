import csv

from api.models import Ingredient, Tag
from django.conf import settings
from django.core.management import BaseCommand

MODELS_FILES = {
    Ingredient: 'ingredients.csv',
    Tag: 'tag.csv'
}


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model, file in MODELS_FILES.items():
            with open(
                    f'{settings.BASE_DIR}/data/{file}',
                    'r', encoding='utf-8',
            ) as table:
                reader = csv.DictReader(table)
                model.objects.bulk_create(
                    model(**data) for data in reader)

        self.stdout.write(self.style.SUCCESS(
            'Загружены вспомогательные элементы')
        )
