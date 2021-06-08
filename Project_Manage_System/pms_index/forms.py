from django import forms
from .models import Projects, ProjectMembers
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Projects
        fields = ('name', 'deadline', 'descriptions')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descriptions': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': '專案名稱',
            'deadline': '專案截止日',
            'descriptions': '專案內容',
        }


# class ProjectMembersForm(forms.ModelForm):
#
#     member_id: forms.ModelMultipleChoiceField(queryset=User.objects.none())
#
#     class Meta:
#
#         # model = ProjectMembers
#         fields = ('member_id',)
#         widgets = {
#             'member_id': forms.SelectMultiple(attrs={'class': 'form-control'}),
#         }
#         labels = {
#             'member_id': '專案使用者',
#         }


class RegisterForm(UserCreationForm):

    last_name = forms.CharField(
        label="姓",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    first_name = forms.CharField(
        label="名字",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
    )

    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password2 = forms.CharField(
        label="確認密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:

        model = User
        fields = {'last_name', 'first_name', 'email', 'username', 'password1', 'password2'}


class LoginForm(forms.Form):

    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

