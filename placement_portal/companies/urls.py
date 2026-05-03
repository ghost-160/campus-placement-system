from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('post-job/', views.post_job_view, name='post_job'),
    path('job/<int:job_id>/applicants/', views.view_applicants_view, name='job_applicants'),
]