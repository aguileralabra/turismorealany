# Generated by Django 3.1.2 on 2020-12-08 05:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0027_auto_20201207_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservadetalle',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_sale', to='aplicacion.venta'),
        ),
    ]