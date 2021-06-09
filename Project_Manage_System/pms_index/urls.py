from django.urls import path
from . import views

urlpatterns = [
    path('', views.pms_index, name="Index"),
    path('login/', views.sign_in, name="Login"),
    path('logout/', views.log_out, name="Logout"),
    path('register/', views.register, name="Register"),
]
