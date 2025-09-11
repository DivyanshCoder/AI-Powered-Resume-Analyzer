from huggingface_hub import InferenceClient
import requests
import json
from django.conf import settings
import traceback
import time
import google.generativeai as genai

class HuggingFaceAnalyzer:
    def __init__(self):
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def analyze_resume(self, prompt):
        try:
            response = self.model.generate_content(prompt)
            # response = self.model.generate_content("hello")
            print(response.text) 
            return response.text
        except Exception as e:
            return f"Analysis error: {str(e)}"
