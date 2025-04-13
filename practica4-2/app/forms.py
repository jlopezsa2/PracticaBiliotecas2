# app_primera_bd/forms.py
from django import forms
from .models import Library, Loan, Book, User

class LibraryForm(forms.ModelForm):
    class Meta:
        model = Library
        fields = '__all__'

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'

class LoanForm(forms.ModelForm):
    class Meta:
        model = Loan
        exclude = ['devuelto']
        
        
class EditarLibroForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['titulo', 'autor', 'editorial', 'biblioteca']        