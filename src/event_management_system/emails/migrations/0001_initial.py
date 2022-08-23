# Generated by Django 3.2.12 on 2022-08-23 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('subject', models.CharField(max_length=100)),
                ('answer_to_email', models.EmailField(max_length=254)),
                ('body', models.CharField(max_length=8192)),
            ],
        ),
    ]