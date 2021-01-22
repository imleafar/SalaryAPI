from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import UserForm, CreateAccountForm
from .models import User

# Create your views here.


@login_required(login_url='login')
def user_list(request):
    context = {'user_list': User.objects.all()}
    return render(request, "user_register/user_list.html", context)


@login_required(login_url='login')
def user_form(request, id=0):
    if request.method == "GET":
        if id == 0:
            form = UserForm()
        else:
            user = User.objects.get(pk=id)
            form = UserForm(instance=user)
        return render(request, "user_register/user_form.html", {'form': form})
    else:
        if id == 0:
            form = UserForm(request.POST)
        else:
            user = User.objects.get(pk=id)
            form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
        else:
            return HttpResponse("<script>alert('Please do not try to insert fake data. Date must be in mm/dd/yyyy format.')</script>")
        return redirect('/users')


@login_required(login_url='login')
def user_delete(request, id):
    user = User.objects.get(pk=id)
    user.delete()
    return redirect('/users')


def register_page(request):
    if request.user.is_authenticated:
        return redirect('')
    else:
        form = CreateAccountForm()
        if request.method == 'POST':
            form = CreateAccountForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'accounts/register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('user_list')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/users')
            else:
                messages.info(request, 'Username or password is incorrect')

        context = {}
        return render(request, 'accounts/login.html', context)


def logout_user(request):
    logout(request)
    return\
        redirect('login')
