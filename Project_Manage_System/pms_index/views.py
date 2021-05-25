from django.shortcuts import render, redirect
from django.views import View
from .forms import NewProject
from .models import Projects


def index(request):

    all_projects = Projects.objects.all()

    new_project_form = NewProject()

    if request.method == "POST":
        new_project_form = NewProject(request.POST)
        if new_project_form.is_valid():
            new_project_form.save()
        return redirect("/")

    return render(request, "index.html", locals())


def login(request):
    return render(request, "login.html", locals())