from django import forms
from .models import Projects, ProjectMembers
from django.contrib.auth.models import User


class NewProject(forms.ModelForm):

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


class NewProjectMembers(forms.ModelForm):

    member_id: forms.ModelMultipleChoiceField(queryset=User.objects.none())

    class Meta:

        model = ProjectMembers
        fields = ('member_id',)
        widgets = {
            'member_id': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        labels = {
            'member_id': '專案使用者',
        }