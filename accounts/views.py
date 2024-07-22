from django.views.generic import (
    TemplateView
)
from django.urls import reverse_lazy
from django.contrib.auth.views import LogoutView,LoginView
from .forms import *
from django.contrib import messages
from django.views.generic import CreateView
class LoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    
    
class SignupView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = SignupForm
    success_url = reverse_lazy('accounts:login')


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home:home')