from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

class LoginView(LoginView):
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('home')

class LogoutView(LogoutView):
    success_url = reverse_lazy('login')

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'