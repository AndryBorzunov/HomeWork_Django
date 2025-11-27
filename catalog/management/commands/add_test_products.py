from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Load data to the database from fixture"

    def handle(self, *args, **options):
        # Удаляем существующие записи
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загрузка данных из фикстуры
        call_command("loaddata", "catalog_fixture.json")
        self.stdout.write(self.style.SUCCESS("Successfully load data from fixture"))
