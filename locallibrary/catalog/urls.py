from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>', views.BookDetailView.as_view(), name='book-detail'),
    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book-select/', views.select_book, name='book-select'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    path('author/', views.AuthorListView.as_view(), name='author'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    path('author-select/', views.select_author, name='author-select'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author-update'), 
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
    path('genre/', views.GenreListView.as_view(), name='genre'),
    path('genres/<int:pk>', views.GenreDetailView.as_view(), name='genre-detail'),
    path('language/', views.LanguageListView.as_view(), name='language'),
    path('language/<int:pk>/', views.LanguageDetailView.as_view(), name='language-detail'),
    path('mybooks/', views.LoaneBooksByUserListView.as_view(), name='my-borrowed'),
    path('allbooks/', views.BooksCheckedOutByAllUsers.as_view(), name='all-borrowed'),
]