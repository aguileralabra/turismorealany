# Generated by Django 3.1.2 on 2020-12-07 04:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0021_remove_reservando_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservando',
            name='Fecha_Reserva_Inicios',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='reservando',
            name='Fecha_Reserva_Terminos',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
    ]