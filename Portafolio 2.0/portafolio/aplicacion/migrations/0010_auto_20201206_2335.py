# Generated by Django 3.1.2 on 2020-12-07 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0009_remove_reservando_codigo_reservas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservando',
            name='user',
            field=models.ForeignKey(default='request.user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]