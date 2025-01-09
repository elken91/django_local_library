from django.db import migrations, models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

def create_permission(apps, schema_editor):
    BookInstance = apps.get_model('catalog', 'BookInstance')
    content_type = ContentType.objects.get_for_model(BookInstance)
    Permission.objects.create(
        codename='set_book_as_returned',
        name='Set book as returned',
        content_type=content_type,
    )

class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0019_alter_book_isbn'),  # Reemplaza '0019_alter_book_isbn' con el nombre del archivo de migración anterior
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, null=True, verbose_name='Died'),
        ),
        migrations.RunPython(create_permission),
    ]
