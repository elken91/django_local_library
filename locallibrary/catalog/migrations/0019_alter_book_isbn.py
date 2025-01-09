# Generated by Django 5.1.2 on 2024-12-23 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0018_alter_author_date_of_death'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>', max_length=14, verbose_name='ISBN'),
        ),
    ]
