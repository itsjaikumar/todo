from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user


@login_required(login_url='login')
def index(request):
    tasks = request.user.task_set.order_by('-created').all()
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
        return redirect('/')

    context = {
        'tasks':tasks,
        'form':form,
    }
    return render(request, 'tasks/list.html', context)

def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm2(instance=task)

    if request.method == 'POST':
        form = TaskForm2(request.POST, instance=task)
        if form.is_valid():
            form.save()
        return redirect('/')
    
    context = {
        'form':form,
    }
    return render(request, 'tasks/update_task.html', context)


def deleteTask(request, pk):
    item = Task.objects.get(id=pk)

    if request.method == 'POST':
        item.delete()
        return redirect('/')
    context = {
        'item':item,
    }
    return render(request, 'tasks/delete.html', context)

@unauthenticated_user
def loginPage(request):
    
        if request.method =='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username or Password is incorrect')
        context = {}
        return render(request, 'tasks/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@unauthenticated_user
def registerPage(request):
    
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                username = form.cleaned_data.get('username')
                
                messages.success(request, 'Account has been created for ' + username)
                return redirect('login')
        
        context ={'form':form}
        return render(request, 'tasks/register.html', context)

    


