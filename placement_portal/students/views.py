from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import StudentProfile
from jobs.models import Job
from applications.models import Application


def student_required(view_func):
    """
    Decorator to check if user has a student profile.
    Redirects to login if not a student.
    """
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'student_profile'):
            messages.error(request, 'This area is only for students.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return login_required(login_url='accounts:login')(wrapper)


@student_required
def profile_view(request):
    """
    Create or update student profile.
    """
    student_profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        register_no = request.POST.get('register_no', '').strip()
        branch = request.POST.get('branch', '').strip()
        cgpa = request.POST.get('cgpa', '').strip()
        skills = request.POST.get('skills', '').strip()
        backlogs = request.POST.get('backlogs', '').strip()
        resume = request.FILES.get('resume')

        # Validation
        errors = []
        
        if not register_no:
            errors.append('Registration number is required.')
        if not branch:
            errors.append('Branch is required.')
        if not cgpa:
            errors.append('CGPA is required.')
        
        try:
            cgpa_float = float(cgpa)
            if not (0 <= cgpa_float <= 10):
                errors.append('CGPA must be between 0 and 10.')
        except ValueError:
            errors.append('CGPA must be a valid number.')

        if backlogs:
            try:
                backlogs_int = int(backlogs)
                if backlogs_int < 0:
                    errors.append('Backlogs cannot be negative.')
            except ValueError:
                errors.append('Backlogs must be a valid number.')
        else:
            backlogs_int = 0

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'students/profile.html', {'profile': student_profile, 'branch_choices': StudentProfile.BRANCH_CHOICES})

        # Update profile
        student_profile.register_no = register_no
        student_profile.branch = branch
        student_profile.cgpa = cgpa_float
        student_profile.skills = skills
        student_profile.backlogs = backlogs_int
        
        if resume:
            student_profile.resume = resume

        student_profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('students:dashboard')

    context = {
        'profile': student_profile,
        'branch_choices': StudentProfile.BRANCH_CHOICES,
    }
    return render(request, 'students/profile.html', context)


@student_required
def dashboard_view(request):
    """
    Student dashboard showing profile and application statistics.
    """
    student_profile = get_object_or_404(StudentProfile, user=request.user)
    
    # Get student's applications
    applications = Application.objects.filter(student=student_profile)
    applied_count = applications.count()
    shortlisted_count = applications.filter(status='SHORTLISTED').count()
    selected_count = applications.filter(status='SELECTED').count()
    rejected_count = applications.filter(status='REJECTED').count()

    context = {
        'profile': student_profile,
        'applied_count': applied_count,
        'shortlisted_count': shortlisted_count,
        'selected_count': selected_count,
        'rejected_count': rejected_count,
        'recent_applications': applications[:5],
    }
    return render(request, 'students/dashboard.html', context)


@student_required
def eligible_jobs_view(request):
    """
    Display jobs eligible for the student based on CGPA, branch, and deadline.
    """
    student_profile = get_object_or_404(StudentProfile, user=request.user)

    # Filter eligible jobs
    eligible_jobs = Job.objects.filter(
        Q(min_cgpa__lte=student_profile.cgpa) &
        Q(branch__in=[student_profile.branch, 'ALL']) &
        Q(deadline__gte=timezone.now().date())
    ).order_by('-created_at')

    # Check which jobs student has already applied to
    applied_jobs_ids = Application.objects.filter(
        student=student_profile
    ).values_list('job_id', flat=True)

    # Add flag to indicate if student applied
    for job in eligible_jobs:
        job.already_applied = job.id in applied_jobs_ids

    # Filter by branch if requested
    selected_branch = request.GET.get('branch', '')
    if selected_branch and selected_branch != 'ALL':
        eligible_jobs = eligible_jobs.filter(branch__in=[selected_branch, 'ALL'])

    context = {
        'eligible_jobs': eligible_jobs,
        'student_profile': student_profile,
        'selected_branch': selected_branch,
        'branch_choices': [choice for choice in Job.BRANCH_CHOICES if choice[0] != 'ALL'],
    }
    return render(request, 'students/eligible_jobs.html', context)
