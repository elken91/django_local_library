from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
from django.contrib.auth.models import Permission

from catalog.models import Author, BookInstance, Book, Genre, Language
from django.urls import reverse

class AuthorlistViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user=User.objects.create_user(username='testuser1', password='12345')
        test_user.save()

        number_of_authors=13
        for author_num in range(number_of_authors):
            Author.objects.create(first_name='Chirstian %s' % author_num, last_name='Surname %s' % author_num)
    
    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser1', password='12345')
        resp=self.client.get('/catalog/author/')
        self.assertEqual(resp.status_code, 200)
    
    def test_view_url_accessible_by_name(self):
        self.client.login(username='testuser1', password='12345') 
        resp= self.client.get(reverse('author'))
        self.assertEqual(resp.status_code, 200)
    
    def test_view_uses_correct_template(self):
        self.client.login(username='testuser1', password='12345')
        resp=self.client.get(reverse('author'))
        self.assertEqual(resp.status_code, 200)
        
        self.assertTemplateUsed(resp, 'catalog/author_list.html')

    def test_pagination_is_ten(self):
        self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('author'))
        self.assertEqual(resp.status_code,200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated']==True)
        self.assertTrue( len(resp.context['author_list'])==10)

    def test_lists_all_authors(self):
        self.client.login(username='testuser1', password='12345')
        resp=self.client.get(reverse('author')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated']==True)
        self.assertTrue( len(resp.context['author_list'])==3)
    
class LoanedBookInstancesByUserListViewTest(TestCase):
    def setUp(self):

        #creacion de usuarios para test
        test_user1=User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2=User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()

        #crear un libro para el test

        test_author=Author.objects.create(first_name='Jhon', last_name='Smith')
        test_genre=Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book Title',
            summary='My Book summary',
            isbn='ABCDEFG',
            author=test_author)
        
        # crear genero como un paso posterior (pendiente)
        genre_objects_for_book=Genre.objects.all()
        test_book.language.set([test_language])
        test_book.genre.set(genre_objects_for_book)#no se permite la adignación directa de tipos de muchos a muchos
        test_book.save()

        #creacion de 30 objetos BookInstance
        number_of_book_copies=30
        for book_copy in range (number_of_book_copies):
            return_date=timezone.now() + datetime.timedelta(days=book_copy %5)
            if book_copy % 2:
                the_borrower=test_user1
            else:
                the_borrower=test_user2
            status='m'
            BookInstance.objects.create(
                book=test_book, 
                imprint='Unlikely Imprint, 2016', 
                due_back=return_date, 
                borrower=the_borrower, 
                status=status
                )


    def test_redirect_if_not_logged_in(self):
        resp=self.client.get(reverse('my-borrowed'))
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/mybooks/')
    
    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username='testuser1', password='12345')
        resp= self.client.get(reverse('my-borrowed'))

        #comprobar que nuestro usuario tiene la sessión iniciada
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #comprueba que obtuvimos uan respuesta "exitosa"
        self.assertEqual(resp.status_code, 200)

        #compruebe que usamos la plantilla correcta
        self.assertTemplateUsed(resp, 'catalog/bookinstance_list_borrowed_user.html')
    
    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-borrowed'))

        #comprobar que el usuario tiene la sesión abierta
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #comprobacion que se obtuvo coneccion exitosa
        self.assertEqual(resp.status_code, 200)

        #comprueba que inicialmente no tenemos ningun libro en la lista ( ninguno en prestamo)
        self.assertTrue('bookinstance_list' in resp.context)
        self.assertEqual(len(resp.context['bookinstance_list']), 0)

        #ahora cambia todos los libros para que esten en prestamo
        get_ten_books=BookInstance.objects.all()[:10]

        for copy in get_ten_books:
            copy.status='o'
            copy.save()
        
        #comprueba que ahora tenemos libros prestados en la lista
        resp = self.client.get(reverse('my-borrowed'))
        #comprobar que nuestro usuario tiene sesion iniciada
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #comprueba que obtuvimos respuesta con exito
        self.assertEqual(resp.status_code, 200)

        self.assertTrue('bookinstance_list' in resp.context)

        #confirma que todos los libros pertenecen a testuser1 y estan en prestamo
        for bookitem in resp.context['bookinstance_list']:
            self.assertEqual(resp.context['user'], bookitem.borrower)
            self.assertEqual('o', bookitem.status)
    
    def test_pages_ordered_by_due_date(self):
        #cambiar todos los libros para que esten en préstamo
        for copy in BookInstance.objects.all():
            copy.status='o'
            copy.save()
        
        login =self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-borrowed'))

        #comprbar que nuestro usuario tiene sesión abierta
        self.assertEqual(str(resp.context['user']), 'testuser1')
        #comprobacion que tuvimos conexción exitosa
        self.assertEqual(resp.status_code, 200)

        #confirmacion de artuculos, solo se muestran 10 por la paginación.
        self.assertEqual(len(resp.context['bookinstance_list']),10)

        last_date=0
        for copy in resp.context['bookinstance_list']:
            if last_date==0:
                last_date=copy.due_back
            else:
                self.assertTrue(last_date <= copy.due_back)



from django.contrib.auth.models import Permission # Requerido para otorgar el permiso necesario para establecer un libro como devuelto.

class RenewBookInstancesViewTest(TestCase):

    def setUp(self):
        #Crear un usuario
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()

        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()
        
        permission = Permission.objects.get(codename='set_book_as_returned')
        test_user2.user_permissions.add(permission) 
        test_user2.save()

        #Crear un libro
        test_author = Author.objects.create(first_name='John', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(
            title='Book Title', 
            summary = 'My book summary', 
            isbn='ABCDEFG', 
            author=test_author, 
            )
        
        # Crear género como un paso posterior
        test_book.language.set([test_language])
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # No se permite la asignación directa de tipos de muchos a muchos.
        test_book.save()

        #Cree un objeto BookInstance para test_user1
        return_date= datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance1=BookInstance.objects.create(book=test_book,imprint='Unlikely Imprint, 2016', due_back=return_date, borrower=test_user1, status='o')

        #Cree un objeto BookInstance para test_user2
        return_date= datetime.date.today() + datetime.timedelta(days=5)
        self.test_bookinstance2=BookInstance.objects.create(book=test_book,imprint='Unlikely Imprint, 2016', due_back=return_date, borrower=test_user2, status='o')

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}) )
        #Revisar manualmente la redirección (no se puede usar assertRedirect, porque la URL de redirección es impredecible)
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/accounts/login/') )

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}) )

        #Revisar manualmente la redirección (no se puede usar assertRedirect, porque la URL de redirección es impredecible)
        self.assertEqual( resp.status_code,302)
        self.assertTrue( resp.url.startswith('/accounts/login/') )

    def test_logged_in_with_permission_borrowed_book(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance2.pk,}) )

        #Comprobar que nos permita iniciar sesión: este es nuestro libro y tenemos los permisos correctos.
        self.assertEqual( resp.status_code,200)

    def test_logged_in_with_permission_another_users_borrowed_book(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}) )

        #Comprobar que nos deja iniciar sesión. Somos bibliotecarios, por lo que podemos ver cualquier libro de usuarios.
        self.assertEqual( resp.status_code,200)

    def test_HTTP404_for_invalid_book_if_logged_in(self):
        import uuid
        test_uid = uuid.uuid4() #¡Es improbable que el UID coincida con nuestra instancia de libro!
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk':test_uid,}) )
        self.assertEqual( resp.status_code, 404)

    def test_uses_correct_template(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}) )
        self.assertEqual( resp.status_code,200)

        #Compruebe que usamos la plantilla correcta
        self.assertTemplateUsed(resp, 'catalog/book_renew_librarian.html')

    def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
        login = self.client.login(username='testuser2', password='12345')
        resp = self.client.get(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}) )
        self.assertEqual( resp.status_code,200)

        date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
        self.assertEqual(resp.context['form'].initial['renewal_date'], date_3_weeks_in_future )
    

    def test_form_invalid_renewal_date_past(self):
        login = self.client.login(username='testuser2', password='12345')
        date_in_past = datetime.date.today() - datetime.timedelta(weeks=1)
        resp = self.client.post(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':date_in_past} )
        self.assertEqual( resp.status_code,200)
        self.assertFormError(resp.context['form'], 'renewal_date', 'Invalid date - renewal in past')

    def test_form_invalid_renewal_date_future(self):
        login = self.client.login(username='testuser2', password='12345')
        invalid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=5)
        resp = self.client.post(reverse('renew-book-librarian', kwargs={'pk':self.test_bookinstance1.pk,}), {'renewal_date':invalid_date_in_future} )
        form = resp.context['form']
        self.assertEqual( resp.status_code,200)
        self.assertFormError(resp.context['form'], 'renewal_date', 'Invalid date - renewal more than 4 weeks ahead')