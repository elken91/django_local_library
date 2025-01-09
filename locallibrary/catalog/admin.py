from django.contrib import admin
from .models import Author, Genre, Book, BookInstance ,Language

# Register your models here.


class BookInline(admin.TabularInline):
    model = Book
    fields=['title', 'genre']
    extra = 0

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0

#admin.site.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]
admin.site.register(Book, BookAdmin)

#admin.site.register(Author)

    
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name','date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines=[BookInline]
    
    def book_titles(self, obj):
        return ", ".join([book.title for book in obj.book_set.all()]) 
    book_titles.short_description = 'Books'
    pass

admin.site.register(Author,AuthorAdmin)


admin.site.register(Genre)

#admin.site.register(BookInstance)


class BookInstanceAdmin(admin.ModelAdmin):
    
    list_display= ('book', 'status','borrower', 'due_back','id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back','borrower')
        }),
    )

    pass
admin.site.register(BookInstance, BookInstanceAdmin)


admin.site.register(Language)