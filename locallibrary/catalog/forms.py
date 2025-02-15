from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime #for checking renewal date range.
from .models import BookInstance, Author, Book

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))

        #Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return data
    
    class Meta:
        model= BookInstance
        fields = ['due_back',]
        labels = {'due_back': ('Enter a date between now and 4 weeks (default 3).'),}

class AuthorSelectForm(forms.Form):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), label='Seleccionar Autor')

class BookSelectForm(forms.Form):
    book = forms.ModelChoiceField(queryset=Book.objects.all(), label='Seleccionar Book')