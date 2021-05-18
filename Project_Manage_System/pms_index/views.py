from django.shortcuts import render
from django.views import View


class Index(View):
    index = "index.html"

    def get(self, request):
        return render(request, self.index, locals())


class Login(View):
    login = "login.html"

    def get(self, request):
        return render(request, self.login, locals())