from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=256)),
                (
                    'slug',
                    models.SlugField(max_length=50, unique=True),
                ),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=256)),
                (
                    'slug',
                    models.SlugField(max_length=50, unique=True),
                ),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('name', models.CharField(max_length=256)),
                ('year', models.PositiveSmallIntegerField()),
                ('description', models.TextField(blank=True)),
                (
                    'category',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='titles',
                        to='reviews.category',
                    ),
                ),
                (
                    'genre',
                    models.ManyToManyField(
                        related_name='titles',
                        to='reviews.genre',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ('id',),
            },
        ),
    ]
