# Generated by Django 3.1.2 on 2020-12-07 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0013_auto_20201206_2337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservando',
            name='servicioextra',
        ),
    ]
