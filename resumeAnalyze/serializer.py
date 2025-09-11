from rest_framework import serializers
from .models import Job_Description

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_Description
        fields = '__all__'
    
    def validate_resume_file(self, value):
        if not value.name.endswith('.pdf'):
            raise serializers.ValidationError("Only PDF files are allowed.")
        return value

class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job_Description
        fields = '__all__'