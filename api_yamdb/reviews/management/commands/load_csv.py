import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from reviews.models import Category, Genre, Title


class Command(BaseCommand):
    help = 'Импортирует категории, жанры, произведения и связи жанров из CSV.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            default=None,
            help='Путь к каталогу с CSV-файлами.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        data_path = self._get_data_path(options['path'])
        self._load_categories(data_path / 'category.csv')
        self._load_genres(data_path / 'genre.csv')
        self._load_titles(data_path / 'titles.csv')
        self._load_genre_titles(data_path / 'genre_title.csv')
        self.stdout.write(self.style.SUCCESS('CSV-данные загружены.'))

    def _get_data_path(self, custom_path):
        if custom_path:
            path = Path(custom_path)
        else:
            path = Path(__file__).resolve().parents[4] / 'static' / 'data'
        if not path.is_dir():
            raise CommandError(f'Каталог не найден: {path}')
        return path

    @staticmethod
    def _read_csv(path):
        if not path.is_file():
            raise CommandError(f'Файл не найден: {path}')
        with path.open(encoding='utf-8', newline='') as file:
            return list(csv.DictReader(file))

    def _load_categories(self, path):
        for row in self._read_csv(path):
            Category.objects.update_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'slug': row['slug'],
                },
            )

    def _load_genres(self, path):
        for row in self._read_csv(path):
            Genre.objects.update_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'slug': row['slug'],
                },
            )

    def _load_titles(self, path):
        categories = {
            category.id: category
            for category in Category.objects.all()
        }

        for row in self._read_csv(path):
            category = (
                categories.get(int(row['category']))
                if row['category']
                else None
            )

            Title.objects.update_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'year': int(row['year']),
                    'description': row['description'],
                    'category': category,
                },
            )

    def _load_genre_titles(self, path):
        titles = {title.id: title for title in Title.objects.all()}
        genres = {genre.id: genre for genre in Genre.objects.all()}
        for row in self._read_csv(path):
            title = titles.get(int(row['title_id']))
            genre = genres.get(int(row['genre_id']))
            if title is not None and genre is not None:
                title.genre.add(genre)
