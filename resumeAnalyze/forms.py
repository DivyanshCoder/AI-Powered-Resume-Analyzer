from django import forms
from .models import Job_Description

class JobDescriptionForm(forms.ModelForm):
    class Meta:
        model = Job_Description
        fields = ['job_description', 'resume_file']

        widgets = {
            'job_description': forms.Textarea(attrs={'class': 'form-control'}),
            'resume_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
   