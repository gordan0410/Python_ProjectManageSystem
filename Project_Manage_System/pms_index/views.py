from django.shortcuts import render, redirect
from django.views import View
from .forms import NewProject, NewProjectMembers
from .models import Projects, ProjectMembers


def index(request):

    all_projects = Projects.objects.all()

    new_project_form = NewProject()
    new_project_member_form = NewProjectMembers()

    if request.method == "POST":
        new_project_form = NewProject(request.POST)
        new_project_member_form = NewProjectMembers(request.POST)
        if new_project_member_form.is_valid() and new_project_form.is_valid():
            npfform = new_project_form.save(commit=False)
            npfform.owner = request.user
            new_project_form.save()
            npmform = new_project_member_form.save(commit=False)
            npmform.project_id = npfform
            npmform.member_status = "Developer"
            npmform.save()
            new_project_member_form.save_m2m()
            return redirect("/")

    return render(request, "index.html", locals())


def login(request):
    return render(request, "login.html", locals())