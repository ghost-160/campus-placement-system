from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from students.models import StudentProfile
from companies.models import CompanyProfile
from jobs.models import Job
from applications.models import Application


def home(request):
    """Public home page with role-based redirection and statistics."""
    user = request.user
    if user.is_authenticated:
        if user.is_superuser:
            return redirect('college_admin:dashboard')
        if hasattr(user, 'student_profile'):
            return redirect('students:dashboard')
        if hasattr(user, 'company_profile'):
            return redirect('companies:dashboard')

    stats = {
        'total_students': StudentProfile.objects.count(),
        'total_companies': CompanyProfile.objects.count(),
        'total_jobs': Job.objects.count(),
        'total_placements': Application.objects.filter(status='SELECTED').count(),
    }

    return render(request, 'core/home.html', {'stats': stats})
