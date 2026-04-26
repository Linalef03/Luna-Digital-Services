from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm, RegisterForm
from logs.utils import create_log


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            create_log(user, f"Se connecter")

            if user.is_superuser:
                return redirect('dashboard:admin_dashboard')
            elif hasattr(user, 'employee'):
                return redirect('dashboard:employee_dashboard')
            else:
                return redirect('orders:my_orders')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
            return redirect('accounts:login')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            create_log(user, "Il a créé un nouveau compte")

            return redirect('accounts:login')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def logout_view(request):
    
    create_log(request.user, "Se déconnecter")

    logout(request)
    return redirect('home')