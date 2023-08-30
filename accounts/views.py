from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('posts:index')

    else:
        form = CustomUserCreationForm()

    context = {
        'form': form
    }

    return render(request, 'accounts/form.html', context)

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request,request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request,user)

            return redirect('posts:index')

    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form
    }

    return render(request, 'form.html', context)