from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm
from django.contrib import messages

from .forms import MyAuthenticationForm, MyUserCreationForm


def _login_view(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        passwd = data.get('passwd')
        user = authenticate(username=username, password=passwd)
        if user:
            login(request, user)
            messages.success(request, 'Account successfully authenticated')
            return redirect('articles:list')
        messages.error(request, "Account not found")
        return redirect('.')
    ctx = {

    }
    return render(request, 'accounts/login.html', ctx)


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'Firstly you should logout')
        return redirect('articles:list')
    form = MyAuthenticationForm(request)
    if request.method == 'POST':
        form = MyAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Account successfully authenticated')
            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            return redirect('articles:list')
    ctx = {
        'form': form
    }
    return render(request, 'accounts/login_form.html', ctx)


def logout_view(request):
    if not request.user.is_authenticated:
        messages.info(request, 'Firstly you should login')
        return redirect('accounts:login')
    if request.method == "POST":
        logout(request)
        messages.error(request, 'Account logout')
        return redirect('articles:list')
    return render(request, 'accounts/logout.html')


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'Firstly you should logout')
        return redirect('articles:list')
    form = MyUserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Account successfully registered')
        return redirect('accounts:login')
    ctx = {
        'form': form
    }
    return render(request, 'accounts/register.html', ctx)
