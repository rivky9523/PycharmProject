from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .models import Task
from .forms import  SetProfileForm
from .models import UserStaff
from django.contrib.auth.decorators import login_required
from .forms import ManagerTaskForm, TaskForm
from django.contrib.auth import logout

def home(request):
    context = {
        'logged_in': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else ''
    }
    return render(request, 'home.html', context)
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserStaff.objects.create(user=user)
            login(request, user)
            return redirect("profile")
        else:
            print(form.errors)
    else:
        form = UserCreationForm()
    return render(request,"register.html",{'form':form})



def login2(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("allTasks")
    else:
        form = AuthenticationForm()
    return render(request,"login.html",{'form':form})
@login_required
def logout2(request):
    logout(request)
    return redirect('home')

def setProfile(request):
    if request.method == 'POST':
        form = SetProfileForm(request.POST)
        if form.is_valid():
            profile = UserStaff.objects.get(user=request.user)
            profile.role = form.cleaned_data['role']
            profile.team = form.cleaned_data['team']
            profile.save()
            return redirect("allTasks")
    else:
        form = SetProfileForm()
    return render(request, "profile.html", {'form': form})
@login_required
def allTasks(request):
    user_staff = request.user.userstaff
    print(user_staff.role)
    tasks = Task.objects.filter(team=user_staff.team)
    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)
    my_tasks = request.GET.get('my')
    if my_tasks == "1":
        tasks = tasks.filter(user=user_staff)
    context = {
        'tasks': tasks,
        'staff': user_staff,
    }
    return render(request, 'allTasks.html', context)
@login_required
def take_task(request, task_id):
    user_staff = request.user.userstaff
    task = Task.objects.filter(id=task_id, team=user_staff.team).first()
    if task and task.status == 1:
        task.user = user_staff
        task.status = 2
        task.save()
    return redirect('allTasks')

@login_required
def complete_task(request, task_id):
    task = Task.objects.filter(id=task_id, team=request.user.userstaff.team).first()
    if not task:
        return redirect('allTasks')
    if task.user == request.user.userstaff:
        task.status = 3
        task.save()
    return redirect('allTasks')

@login_required
def task_add(request):
    user_staff = request.user.userstaff
    if user_staff.role != 1:
        return redirect('allTasks')
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit = False)
            new_task.team = user_staff.team
            new_task.save()
            return  redirect('allTasks')
    else:
        form = TaskForm()

    return render(request, 'taskForm.html', {"form" : form})

@login_required
def task_edit(request, task_id):
    user_staff = request.user.userstaff
    if user_staff.role != 1:
        return redirect('allTasks')
    task = Task.objects.filter(id=task_id, team=request.user.userstaff.team).first()
    if not task:
        return redirect('allTasks')
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('allTasks')
    else:
        form = TaskForm(instance=task)
    return  render(request, 'taskForm.html', {"form": form})

@login_required
def task_delete(request, task_id):
    user_staff = request.user.userstaff
    if user_staff.role != 1:
        return redirect('allTasks')
    try:
        task = Task.objects.get(id = task_id, team = user_staff.team)
        task.delete()
    except Task.DoesNotExist:
        pass
    return redirect('allTasks')


