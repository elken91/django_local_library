# Generated by Django 5.1.2 on 2024-12-15 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0015_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'set book as returned'),)},
        ),
    ]
