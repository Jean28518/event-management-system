# Generated by Django 4.1 on 2022-08-05 12:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_user_user_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('surname', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('website', models.URLField()),
                ('company', models.CharField(max_length=100)),
                ('over_18', models.BooleanField()),
                ('password', models.CharField(max_length=256)),
                ('private_pin', models.CharField(max_length=100)),
                ('user_role', models.CharField(choices=[('CO', 'Contact'), ('AT', 'Attendant'), ('OR', 'Organisatior'), ('AD', 'Admin')], default='CO', max_length=2)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
