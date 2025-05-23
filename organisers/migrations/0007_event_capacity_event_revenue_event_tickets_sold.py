# Generated by Django 5.2 on 2025-05-02 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organisers', '0006_alter_event_organizer'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='capacity',
            field=models.PositiveIntegerField(default=100, help_text='Maximum number of tickets available for this event'),
        ),
        migrations.AddField(
            model_name='event',
            name='revenue',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Total revenue generated from ticket sales', max_digits=10),
        ),
        migrations.AddField(
            model_name='event',
            name='tickets_sold',
            field=models.PositiveIntegerField(default=0, help_text='Number of tickets sold so far'),
        ),
    ]
