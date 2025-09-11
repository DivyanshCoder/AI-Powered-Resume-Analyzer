from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_resume, name='upload_resume'),
    path('analyzing/<int:resume_id>/', views.analyzed_data, name='analyzed_data'),
    path('result/<int:resume_id>/', views.result_data, name='result_data'),
    path("analyzer/<int:resume_id>/", views.analyze_resume_with_hf, name="analyzer"),
]