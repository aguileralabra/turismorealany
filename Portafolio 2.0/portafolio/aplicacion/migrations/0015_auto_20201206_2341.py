# Generated by Django 3.1.2 on 2020-12-07 02:41

import aplicacion.models
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0014_remove_reservando_servicioextra'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservando',
            name='Codigo_Reservas',
            field=models.CharField(default=aplicacion.models.random_string, max_length=5, unique=True),
        ),
        migrations.AddField(
            model_name='reservando',
            name='Estado_Reservas',
            field=models.BooleanField(default=False),
        ),
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
        migrations.AddField(
            model_name='reservando',
            name='servicioextras',
            field=models.ManyToManyField(blank=True, null=True, to='aplicacion.ServicioExtra'),
        ),
    ]