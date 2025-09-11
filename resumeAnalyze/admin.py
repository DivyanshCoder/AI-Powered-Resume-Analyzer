from django.contrib import admin
from .models import Job_Description

# Register your models here.

@admin.register(Job_Description)
class JobDescriptionAdmin(admin.ModelAdmin):
    list_display = ['job_description']  
    exclude = ['name', 'resume_file']
