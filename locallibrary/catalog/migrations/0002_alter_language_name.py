# Generated by Django 5.1.2 on 2024-11-09 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='language',
            name='name',
            field=models.CharField(help_text='Ingrese el nombre del idioma', max_length=200, verbose_name='Language'),
        ),
    ]
