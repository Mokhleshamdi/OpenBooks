from django.forms import ModelForm,fields
from .models import Book, Profile, Comment
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from simple_search import search_form_factory
from django.views.generic.edit import UpdateView
from django.contrib.auth.admin import admin

class AddBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title','author','summary','isbn','genre','language','image','file','copies']
class LoginForm(forms.Form):
    username = forms.CharField(label='User_name', max_length=64)
    password = forms.CharField(widget=forms.PasswordInput())

SearchForm = search_form_factory(Book.objects.all(),
                                 ['^title', 'description'])
class AddUserForm(UserCreationForm):

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email','password1', 'password2')

class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name', 'last_name','email')
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


