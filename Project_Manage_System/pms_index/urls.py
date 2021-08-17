from django.urls import path
from . import views

urlpatterns = [
    path('', views.pms_index, name="Index"),
    path('login/', views.sign_in, name="Login"),
    path('logout/', views.log_out, name="Logout"),
    path('register/', views.register, name="Register"),
    path('workspace/<int:pk>', views.workspace, name="Workspace"),
    path('workspace/create', views.create_workspace, name="CreateNewWorkspace"),
    path('workspace_delete/', views.workspace_delete, name="WorkspaceDelete"),
    path('workspace_list_add/', views.workspace_list_add, name="ListAdd"),
    path('workspace_card_add/', views.workspace_card_add, name="CardAdd"),
    path('workspace_list_switch/', views.workspace_list_switch, name="ListSwitch"),
    path('workspace_card_switch/', views.workspace_card_switch, name="CardSwitch"),
    path('workspace_list_delete/', views.workspace_list_delete, name="ListDelete"),
    path('workspace_card_delete/', views.workspace_card_delete, name="CardDelete"),
    path('workspace_card_edit/', views.workspace_card_edit, name="CardEdit"),
]
