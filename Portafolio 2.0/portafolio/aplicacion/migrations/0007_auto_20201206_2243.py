# Generated by Django 3.1.2 on 2020-12-07 01:43

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0006_auto_20201206_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='departamento',
            name='Codigo',
            field=models.CharField(default='', max_length=3, unique=True),
        ),
        migrations.AddField(
            model_name='departamento',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created'),
        ),
        migrations.AddField(
            model_name='departamento',
            name='modified',
            field=model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified'),
        ),
        migrations.AlterField(
            model_name='reservando',
            name='Codigo',
            field=models.CharField(max_length=3, unique=True),
        ),
    ]
