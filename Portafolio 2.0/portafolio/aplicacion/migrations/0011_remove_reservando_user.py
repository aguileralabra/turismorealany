# Generated by Django 3.1.2 on 2020-12-07 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0010_auto_20201206_2335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservando',
            name='user',
        ),
    ]
