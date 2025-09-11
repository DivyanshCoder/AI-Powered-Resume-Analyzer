from django.shortcuts import render, redirect, get_object_or_404
from .forms import JobDescriptionForm
from .serializer import JobDescriptionSerializer, Job_Description, ResumeSerializer
from .utils.text_extractor import extract_text_from_pdf, extract_text_from_docx
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.test import RequestFactory    
from .utils.llm_analyzer import HuggingFaceAnalyzer   
from .utils.prompt_generator import create_hf_resume_analysis_prompt 
from django.views.decorators.csrf import csrf_exempt
import re



# Create your views here.
def upload_resume(request):
    if request.method == 'POST':
        form = JobDescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return redirect('analyzed_data', resume_id = obj.id)    
    else:
        form = JobDescriptionForm()     
    return render(request, 'upload.html', {'form': form})   

# class JobDescriptionAPI(APIView):
#     def get(self, request):
#         queryset = Job_Description.objects.all()
#         serializer = JobDescriptionSerializer(queryset, many=True)
#         return Response(serializer.data)

# class AnalyzeResumeAPI(APIView):
#     def post(self, request):
#         response_data = get_anaylze_result(request.data)
#         return Response(response_data)
    
def analyzed_data(request, resume_id):
    return render(request, 'analyzing_data.html', {'resume_id': resume_id})

def result_data(request):
    return render(request, 'result.html')  

def parse_analysis_response(analysis_text):
    """Parse the AI response into structured data"""
    parsed_data = {
        'overall_score': None,
        'score_percentage': 0,
        'skills': [],
        'experience_level': None,
        'experience_class': 'junior',
        'strengths': [],
        'improvements': []
    }
    
    try:
        # Extract Overall Quality Score
        score_pattern = r'(?:overall\s+)?score[:\s]*(\d+(?:\.\d+)?)\s*(?:/\s*(\d+(?:\.\d+)?)|%)?'
        score_match = re.search(score_pattern, analysis_text, re.IGNORECASE)

        if score_match:
            score = float(score_match.group(1))
            max_score = float(score_match.group(2)) if score_match.group(2) else 10
            
            # Convert to percentage if not already
            if max_score == 100:
                parsed_data['overall_score'] = f"{score}/100"
                parsed_data['score_percentage'] = score
            else:
                # Assume it's out of 10, convert to percentage
                percentage = (score / max_score) * 100
                parsed_data['overall_score'] = f"{score}/{max_score}"
                parsed_data['score_percentage'] = percentage
        
        # Extract Key Skills
        skills_pattern = r'(?:skills?|technologies?)[:\s]*([^\n\r]+)'
        skills_match = re.search(skills_pattern, analysis_text, re.IGNORECASE)
        if skills_match:
            skills_text = skills_match.group(1)
            parsed_data['skills'] = [skill.strip() for skill in re.split(r',|;|\|', skills_text) if skill.strip()]
        
        # Extract Experience Level
        if 'senior' in analysis_text.lower():
            parsed_data['experience_level'] = 'Senior Level'
            parsed_data['experience_class'] = 'senior'
        elif 'mid' in analysis_text.lower() or 'intermediate' in analysis_text.lower():
            parsed_data['experience_level'] = 'Mid Level'
            parsed_data['experience_class'] = 'mid'
        else:
            parsed_data['experience_level'] = 'Junior Level'
            parsed_data['experience_class'] = 'junior'
        
        # Extract Strengths
        strengths_section = re.search(r'(?:strengths?|positive\s+aspects?)[:\s]*\n((?:[-*•]\s*.+\n?)+)', analysis_text, re.IGNORECASE | re.MULTILINE)
        if strengths_section:
            strengths_text = strengths_section.group(1)
            parsed_data['strengths'] = [re.sub(r'^[-*•]\s*', '', line.strip()) for line in strengths_text.split('\n') if line.strip()]
        
        # Extract Improvement Areas
        improvements_section = re.search(r'(?:improvements?|suggestions?|recommendations?)[:\s]*\n((?:[-*•]\s*.+\n?)+)', analysis_text, re.IGNORECASE | re.MULTILINE)
        if improvements_section:
            improvements_text = improvements_section.group(1)
            parsed_data['improvements'] = [re.sub(r'^[-*•]\s*', '', line.strip()) for line in improvements_text.split('\n') if line.strip()]
    
    except Exception as e:
        print(f"Error parsing analysis: {str(e)}")
    
    return parsed_data

@csrf_exempt
def analyze_resume_with_hf(request, resume_id):
        try:
            obj = get_object_or_404(Job_Description, id=resume_id)

            file_path = obj.resume_file.path    
            file_extension = file_path.split('.')[-1]

            # analysis_type = request.POST.get('analysis_type', 'general')

            # Extract text from resume
            resume_text = extract_text_from_pdf(file_path)

            # Job description (if stored in DB)
            job_description = obj.job_description if obj.job_description else ""

            # Generate Hugging Face prompt
            prompt = create_hf_resume_analysis_prompt(resume_text, job_description)

            # Analyze with Hugging Face
            analyzer = HuggingFaceAnalyzer()
            analysis_result = analyzer.analyze_resume(prompt)

            # Parse the analysis into structured data
            parsed_data = parse_analysis_response(analysis_result)

            return render(request, 'result.html', {
                'analysis': analysis_result,    
                'parsed_data': parsed_data,
                'model_used': 'Google Gemini 1.5-Flash',
                'model_used': 'analyzer.model_name',
                'resume_preview': resume_text[:300] + "...",
                'success': True
            })  
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })