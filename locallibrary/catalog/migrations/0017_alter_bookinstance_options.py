# Generated by Django 5.1.2 on 2024-12-15 19:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_alter_bookinstance_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back']},
        ),
    ]
