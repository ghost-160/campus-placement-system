from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('jobs/', views.eligible_jobs_view, name='eligible_jobs'),
]