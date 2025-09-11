from django.db import models

# Create your models here.
class Job_Description(models.Model):
    job_description = models.TextField(blank=True, null=True)    
    resume_file = models.FileField(upload_to='resumes/')    
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    