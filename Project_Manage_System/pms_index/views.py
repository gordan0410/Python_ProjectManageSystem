from django.shortcuts import render, redirect
from django.views import View
from .forms import ProjectForm, RegisterForm, LoginForm
from .models import Projects, ProjectMembers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url="Login")
def pms_index(request):
    all_users = User.objects.exclude(username=request.user)
    my_projects = Projects.objects.filter(visibility_id=1)
    public_projects = Projects.objects.filter(visibility_id=2)
    group_projects = Projects.objects.filter(visibility_id=3)

    new_project_form = ProjectForm()

    if request.method == "POST":
        new_project_form = ProjectForm(request.POST)
        current_user = request.user
        data = dict(request.POST)
        select_user = list(data['select_user'])
        select_user = [int(x) for x in select_user]
        select_user.append(current_user.id)
        if new_project_form.is_valid():
            npfform = new_project_form.save(commit=False)
            npfform.status = "active"
            npfform.save()
            for member_id in select_user:
                member_model = ProjectMembers()
                member_model.project_id = npfform
                if member_id == current_user.id:
                    member_model.member_status = "Owner"
                else:
                    member_model.member_status = "Developer"
                member = User.objects.filter(id=member_id).first()
                member_model.member_id = member
                member_model.save()
            return redirect("/")

    return render(request, "index.html", locals())


def sign_in(request):

    login_form = LoginForm()

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")

    return render(request, "login.html", locals())


def log_out(request):

    logout(request)

    return redirect('/login')


def register(request):
    register_form = RegisterForm()
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(request, "註冊成功，請重新登入")
            return redirect("/login")
        else:
            errs = dict(register_form.errors)
            errfields = []
            for errfield in errs.keys():
                errfields.append(errfield)
            messages.error(request, "註冊失敗，請重新輸入")

    return render(request, "register.html", locals())


def workspace(request, pk):

    return render(request, "workspace.html", locals())