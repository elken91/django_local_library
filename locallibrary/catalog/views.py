from django.urls import reverse
from django.views import generic
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# Create your views here.
from .models import Book, Author, BookInstance, Genre, Language


def index(request):  
    """Función vista para la página inicio del sitio. """ 
    # Contadores de registros  
    num_books = Book.objects.all().count() 
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_genre = Genre.objects.all().count() 
    
    num_visits= request.session.get('num_visits', 0)
    num_visits+=1
    request.session['num_visits']=num_visits


    # Renderiza la plantilla con los datos  
    return render( 
        request,  
        'index.html',  
        context={'num_books':num_books,
                 'num_instances':num_instances,
                 'num_instances_available':num_instances_available,
                 'num_authors':num_authors,
                 'num_genre': num_genre,
                 'num_visits': num_visits,
                 }
    )




class BookListView(LoginRequiredMixin, generic.ListView):
    model= Book
    template_name='catalog/book_list.html'
    paginate_by = 10
    
    
    def get_queryset(self):
        return Book.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'Estos son solo algunos datos'
        return context
    

class BookDetailView(generic.DetailView):
    model = Book
    def get_queryset(self):
        return Book.objects.all()
    

class AuthorListView(LoginRequiredMixin, generic.ListView):
    model= Author
    paginate_by = 10
    template_name='catalog/author_list.html'

    def get_queryset(self):
        return Author.objects.all()

    def get_context_data(self, **kwargs):
        context = super(AuthorListView, self).get_context_data(**kwargs)
        context['some_data'] = 'Estos son solo algunos datos'
        return context


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):  
    model= Author
    template_name='catalog/author_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.filter(author=self.object)
        return context


class GenreListView(LoginRequiredMixin, generic.ListView):
    model = Genre
    template_name='catalog/genre_list.html'



class GenreDetailView(generic.DetailView):
    model = Genre
    template_name='catalog/genre_detail.html'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.filter(genre=self.object)
        return context
    

class LanguageListView(LoginRequiredMixin, generic.ListView):
    model = Language
    template_name='catalog/language_list.html'

class LanguageDetailView(generic.DetailView):
    model = Language
    template_name='catalog/language_detail.html'
    
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['book_list'] = Book.objects.filter(language=self.object)
        return context


class LoaneBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """vista generica basada en clases que enumera los libros prestados al usuario actual."""
    model=BookInstance
    template_name='catalog/bookinstance_list_borrowed_user.html'
    paginate_by=10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
    
class BooksCheckedOutByAllUsers(LoginRequiredMixin,generic.ListView):
    model = BookInstance
    template_name = 'catalog/list_of_books_checked_out_by_all_users.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').select_related('borrower').order_by('due_back')


from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import datetime

from .forms import RenewBookForm, AuthorSelectForm, BookSelectForm

@permission_required('catalog.set_book_as_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific BookInstance by librarian
    """
    book_inst=get_object_or_404(BookInstance, pk = pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})




class AuthorCreate(LoginRequiredMixin, CreateView):
    model= Author
    fields= '__all__'
    initial={'date_of_death': '05/05/2018',}



def select_author(request):
    selected_author=None
    if request.method == 'POST':
        form = AuthorSelectForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario
            selected_author = form.cleaned_data['author']
            # Hacer algo con el autor seleccionado
            return redirect(reverse('author-update', kwargs={'pk': selected_author.pk}))
    else:
        form = AuthorSelectForm()

    return render(request, 'catalog/author_select_form.html', {'form': form, 'selected_author':select_author})


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model= Author
    fields= ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

    template_name = 'catalog/author_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author_form'] = AuthorSelectForm()
        return context

class AuthorDelete(LoginRequiredMixin, DeleteView):
    model=Author
    template_name= 'catalog/author_confirm_delete.html'
    success_url=reverse_lazy('author')

class BookCreate(LoginRequiredMixin, CreateView):
    model= Book
    fields = ['title', 'author', 'summary', 'isbn', 'language', 'genre']
    template_name='catalog/book_form.html'


def select_book(request):
    if request.method == 'POST':
        form = BookSelectForm(request.POST)
        if form.is_valid():
            # Procesar los datos del formulario
            selected_book = form.cleaned_data['book']
            # Hacer algo con el autor seleccionado
            return redirect(reverse('book-update', kwargs={'pk': selected_book.pk}))
    else:
        form = BookSelectForm()

    return render(request, 'catalog/book_select_form.html', {'form': form})

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model=Book
    fields= ['title', 'author', 'summary', 'isbn', 'language', 'genre']
    template_name='catalog/book_update_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_form'] = BookSelectForm()
        return context

class BookDelete(LoginRequiredMixin, DeleteView):
    model=Book
    template_name= 'catalog/book_confirm_delete.html'
    success_url=reverse_lazy('books')