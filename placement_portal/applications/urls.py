from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_for_job_view, name='apply'),
    path('status/', views.application_status_view, name='application_status'),
    path('update/<int:application_id>/', views.update_application_status_view, name='update_status'),
]
