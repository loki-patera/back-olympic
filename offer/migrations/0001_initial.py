# Generated by Django 5.2.1 on 2025-05-14 08:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Offer",
            fields=[
                ("id_offer", models.SmallAutoField(primary_key=True, serialize=False)),
                (
                    "type",
                    models.CharField(
                        max_length=50, unique=True, verbose_name="Type d'offre"
                    ),
                ),
                (
                    "number_seats",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(1)],
                        verbose_name="Nombre de places",
                    ),
                ),
                (
                    "discount",
                    models.PositiveSmallIntegerField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="Réduction (%)",
                    ),
                ),
            ],
            options={
                "verbose_name": "Offre",
                "verbose_name_plural": "Offres",
            },
        ),
    ]
