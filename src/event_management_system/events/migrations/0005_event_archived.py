# Generated by Django 4.2.3 on 2023-07-07 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_event_live_board_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='archived',
            field=models.BooleanField(default=False),
        ),
    ]
