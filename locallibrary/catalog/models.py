from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Requerida para las instancias de libros únicos
from datetime import date
from django.contrib.auth.models import User


# Create your models here.
class Genre(models.Model):
    """Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.)."""
    name = models.CharField(max_length=200, help_text="Ingrese el nombre del género (p. ej. Ciencia Ficción, Poesía Francesa etc.)")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)"""
        return self.name
    
    def get_absolute_url(self):
        return reverse('genre-detail', args=[str(self.id)])
    

    


class Language(models.Model):
    """Modelo que representa un género literario (p. ej. ciencia ficción, poesía, etc.)."""
    name = models.CharField('Language', max_length=200, help_text="Ingrese el nombre del idioma")

    def __str__(self):
        """Cadena que representa a la instancia particular del modelo (p. ej. en el sitio de Administración)"""
        return self.name
    
    def get_absolute_url(self):
        return reverse('language-detail', args=[str(self.id)])
    
    def display_Language(self):
        if self.name:
            return','.join([name.name for name in self.name.all()[:3]])
        return 'No hay Idiomas'
    display_Language.short_description='Language'



class Book(models.Model):
    """Modelo que representa un libro (pero no un Ejemplar específico)."""
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True, related_name='books')
    # ForeignKey, ya que un libro tiene un solo autor, pero el mismo autor puede haber escrito muchos libros.
    # 'Author' es un string, en vez de un objeto, porque la clase Author aún no ha sido declarada.
    summary = models.TextField(max_length=1000, help_text="Ingrese una breve descripción del libro")
    isbn = models.CharField('ISBN',max_length=14, help_text='13 Caracteres <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Seleccione el genero para este libro" )
    # ManyToManyField, porque un género puede contener muchos libros y un libro puede cubrir varios géneros.
    # La clase Genre ya ha sido definida, entonces podemos especificar el objeto arriba.py
    language = models.ManyToManyField(Language, help_text="Seleccione un idioma para este libro")

    class Meta:
        ordering = ["title"]
    

    def __str__(self):
        """String que representa al objeto Book"""
        return self.title


    def get_absolute_url(self):
        """Devuelve el URL a una instancia particular de Book"""
        return reverse('book-detail', args=[str(self.id)])
    
    
    def display_genre(self):
        if self.genre:
            return','.join([genre.name for genre in self.genre.all()[:3]])
        return 'No Genre'
    display_genre.short_description ='Genre'

    def display_language(self): 
        if self.language:
            return ', '.join(language.name for language in self.language.all()[:3])
        return 'No language'
    display_genre.short_description = 'Language'



class BookInstance(models.Model):
    """Modelo que representa una copia específica de un libro (i.e. que puede ser prestado por la biblioteca)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="ID único para este libro particular en toda la biblioteca")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField('Observación',max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, 
                             choices=LOAN_STATUS,
                             blank=True, default='m',
                             help_text='Disponibilidad del libro')

    class Meta:
        ordering = ["due_back"]


    def __str__(self):
        """String para representar el Objeto del Modelo"""
        return '%s (%s)' % (self.id,self.book.title)
    
    @property
    def is_overdue(self): 
        if self.due_back and date.today() > self.due_back:
             return True 
        return False


class Author(models.Model):
    """Modelo que representa un autor"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died',null=True, blank=True)

    
    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):
        """Retorna la url para acceder a una instancia particular de un autor."""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        """String para representar el Objeto Modelo"""
        return '%s, %s' % (self.last_name, self.first_name)