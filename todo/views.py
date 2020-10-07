from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login,logout,authenticate
from .forms import TodoForm
from .models import Todoapp
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signup.html', {'form':UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username = request.POST['username'], password = request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodo')
            except IntegrityError:
                 return render(request, 'todo/signup.html', {'form':UserCreationForm(), 'error':"The username is already taken please choose another username"})

        else:
            return render(request, 'todo/signup.html', {'form':UserCreationForm(), 'error':"The password didnt match"})


def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':"The username and password didn't match"})
        else:
            login(request, user)
            return redirect('currenttodo')


@login_required
def createtodo(request):
    if request.method == "GET":
        return render(request, 'todo/createtodo.html',{'form':TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodo')
        except ValueError:
           return render(request, 'todo/createtodo.html',{'form':TodoForm(), 'error': 'Bad value is passed. please try again'}) 

@login_required
def currenttodo(request):
    todos = Todoapp.objects.filter(user= request.user, date_completed__isnull = True)
    return render(request,'todo/currenttodo.html', {'todos':todos})

@login_required
def todoview(request, todo_pk):
    context = get_object_or_404(Todoapp, pk = todo_pk, user = request.user)
    if request.method == 'GET':
        form = TodoForm(instance=context)
        return render(request,'todo/todoview.html',{'context':context, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance = context)
            form.save()
            return redirect('currenttodo')
        except ValueError:
            return render(request,'todo/todoview.html',{'context':context,'form':form, 'error':"The value you have entered is incorrect"})

@login_required
def completetodo(request, todo_pk):
    context = get_object_or_404(Todoapp, pk = todo_pk, user = request.user)
    if request.method == "POST":
        context.date_completed = timezone.now()
        context.save()
        return redirect('currenttodo')

@login_required
def deletetodo(request, todo_pk):
    context = get_object_or_404(Todoapp, pk = todo_pk, user = request.user)
    if request.method == 'POST':
        context.delete()
        return redirect('currenttodo')

@login_required
def completedtodo(request):
    context = Todoapp.objects.filter( user = request.user, date_completed__isnull = False).order_by('-date_completed')
    return render(request, 'todo/completedtodo.html',{'context':context})