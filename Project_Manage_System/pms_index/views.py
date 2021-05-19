from django.shortcuts import render

from django.views import View


def index(request):
    return render(request, "index.html", locals())


def login(request):
    return render(request, "login.html", locals())