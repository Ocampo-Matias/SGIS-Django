from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import incidents, comment, CustomUser
from django.contrib.auth import get_user_model

class IncidentsForm(forms.ModelForm):
    class Meta:
        model = incidents
        fields = ['incident_type', 'description', 'history_incident', 'assigned_to', 'priority', 'state']
        widgets = {
            'incident_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            'history_incident': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a history incident'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'state': forms.Select(attrs={'class': 'form-control'}),
        }

class CommentsFrom(forms.ModelForm):
    class Meta:
        model = comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Write a comment...'}),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', 'role']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2', 'role']:
            self.fields[fieldname].required = True
            
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('username'):
            self.add_error('username', 'This field is required.')
        return cleaned_data

User = get_user_model()

class UserRoleUpdateFrom(forms.ModelForm):
    class Meta:
        model = User
        fields = ['role']
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
