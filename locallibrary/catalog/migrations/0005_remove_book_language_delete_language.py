# Generated by Django 5.1.2 on 2024-11-09 23:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_bookinstance_language_book_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='language',
        ),
        migrations.DeleteModel(
            name='Language',
        ),
    ]
