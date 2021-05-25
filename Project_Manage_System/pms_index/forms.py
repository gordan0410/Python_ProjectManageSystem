from django import forms
from .models import Projects


class NewProject(forms.ModelForm):

    class Meta:
        model = Projects
        fields = ('name', 'deadline', 'descriptions', 'owner')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'deadline': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descriptions': forms.Textarea(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control'}),
            }
        labels = {
            'name': '專案名稱',
            'deadline': '專案截止日',
            'descriptions': '專案內容',
            'owner': '專案擁有者'
        }