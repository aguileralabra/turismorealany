# Generated by Django 3.1.2 on 2020-12-08 02:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0025_auto_20201207_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservando',
            name='Fecha_Reserva_Inicios',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='reservando',
            name='Fecha_Reserva_Terminos',
            field=models.DateField(blank=True),
        ),
    ]