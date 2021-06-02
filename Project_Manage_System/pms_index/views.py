from django.shortcuts import render, redirect
from django.views import View
from .forms import ProjectForm, ProjectMembersForm
from .models import Projects, ProjectMembers
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q


def pms_index(request):
    all_users = User.objects.exclude(username=request.user)
    all_projects = Projects.objects.all()

    new_project_form = ProjectForm()
    new_project_member_form = ProjectMembersForm()

    if request.method == "POST":
        new_project_form = ProjectForm(request.POST)
        current_user = User.objects.filter(username=request.user).first()
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


def login(request):
    return render(request, "login.html", locals())