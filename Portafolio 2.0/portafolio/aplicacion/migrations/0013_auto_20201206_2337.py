# Generated by Django 3.1.2 on 2020-12-07 02:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0012_reservando_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservando',
            name='Estado_Reservas',
        ),
        migrations.RemoveField(
            model_name='reservando',
            name='Fecha_Reservas_Inicio',
        ),
        migrations.RemoveField(
            model_name='reservando',
            name='Fecha_Reservas_Termino',
        ),
        migrations.RemoveField(
            model_name='reservando',
            name='checks',
        ),
        migrations.RemoveField(
            model_name='reservando',
            name='user',
        ),
    ]
