# Generated by Django 5.2 on 2025-05-01 15:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='ticket_quantity',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
