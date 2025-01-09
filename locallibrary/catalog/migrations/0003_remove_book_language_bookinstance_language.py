# Generated by Django 5.1.3 on 2024-11-09 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_alter_language_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='language',
        ),
        migrations.AddField(
            model_name='bookinstance',
            name='language',
            field=models.ManyToManyField(help_text='Seleccione un idioma para este libro', to='catalog.language'),
        ),
    ]
