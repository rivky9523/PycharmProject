from  django import  forms
from django.contrib.auth.models import User
from .models import Task, UserStaff, Team

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','dateEnd']
        labels = {
            'title':'Task Title',
            'description':'Task Description',
            'dateEnd':'Deadline',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'dateEnd': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class SetProfileForm(forms.ModelForm):
    class Meta:
        model = UserStaff
        fields = ['role', 'team']
        labels = {
            'role':'Choose your Role',
            'team':'Choose your Team'
        }
        widgets = {
            'role': forms.Select(attrs={'class':'form-control'}),
            'team': forms.Select(attrs={'class':'form-control'}),
        }

class ManagerTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"
        labels = {
            'title':'Task Title',
            'description':'Task Description',
            'dateEnd':'Deadline',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.Textarea(attrs={'class':'form-control'}),
            'dateEnd': forms.DateInput(attrs={'class':'form-control'}),
        }