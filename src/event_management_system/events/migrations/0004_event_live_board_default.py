# Generated by Django 4.1.2 on 2022-11-10 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_event_disabled_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='live_board_default',
            field=models.CharField(default='', max_length=4096),
        ),
    ]