# Generated by Django 3.1.2 on 2020-12-07 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0005_auto_20201206_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reserva',
            name='total_cobrar',
        ),
        migrations.AddField(
            model_name='reservando',
            name='total_cobrar',
            field=models.FloatField(default='0'),
        ),
    ]
