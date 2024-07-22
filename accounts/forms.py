from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth.models import User
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-10 pr-4 py-2  border border-gray-300 focus:border-yellow-500 focus:outline-none transition duration-500',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-10 pr-4 py-2  border border-gray-300 focus:border-yellow-500 focus:outline-none transition duration-500',
            'placeholder': 'Password'
        })
    )



class SignupForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'w-full pl-10 pr-4 py-2 border border-gray-300 focus:border-yellow-500 focus:outline-none transition duration-500',
            'placeholder': 'Username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full pl-10 pr-4 py-2 border border-gray-300 focus:border-yellow-500 focus:outline-none transition duration-500',
            'placeholder': 'Email'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-10 pr-4 py-2 border border-gray-300 focus:border-yellow-500 focus:outline-none transition duration-500',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full pl-10 pr-4 py-2 border border-gray-300 focus:border-yellow-500 focus:outline-none transition duration-500',
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')