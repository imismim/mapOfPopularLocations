from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from .form import CustomUserCreationForm


@method_decorator(never_cache, name='dispatch')
class LoginView(View):
    template_name = 'user/login-register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account')
        return render(request, self.template_name, {"page": "login"})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "Username does not exist")
            return render(request, self.template_name, {"page": "login"})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'Username OR Password is not correct')
            return render(request, self.template_name, {"page": "login"})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')


@method_decorator(never_cache, name='dispatch')
class RegisterView(View):
    template_name = 'user/login-register.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('account')

        form = CustomUserCreationForm()
        return render(request, self.template_name, {"form": form, "page": "register"})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            login(request, user)
            messages.success(request, "User successfully created")
            return redirect('account')
        else:
            messages.error(request, "An error has occurred during registration")
            return render(request, self.template_name, {"page": "register", "form": form})

class AccountView(LoginRequiredMixin, View):
    login_url='login'
    template_name='user/account.html'
    
    def get(self, request):
        return render(request, self.template_name)