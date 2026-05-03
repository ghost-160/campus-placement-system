from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import IntegrityError
from django.http import Http404
from students.models import StudentProfile
from companies.models import CompanyProfile
from jobs.models import Job
from .models import Application


def student_required(view_func):
    """
    Decorator to check if user has a student profile.
    """
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'student_profile'):
            messages.error(request, 'This action is only for students.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return login_required(login_url='accounts:login')(wrapper)


def company_required(view_func):
    """
    Decorator to check if user has a company profile.
    """
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'company_profile'):
            messages.error(request, 'This action is only for companies.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return login_required(login_url='accounts:login')(wrapper)


@student_required
def apply_for_job_view(request, job_id):
    """
    Student applies for a job.
    
    Security checks:
    1. Verify student eligibility
    2. Prevent duplicate applications
    3. Verify job exists and is still open
    """
    student = get_object_or_404(StudentProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id)

    # 1. Check eligibility one final time (defense in depth)
    eligibility_checks = {
        'cgpa': student.cgpa >= job.min_cgpa,
        'branch': job.branch == 'ALL' or job.branch == student.branch,
        'deadline': job.deadline >= timezone.now().date(),
        'no_backlogs': student.backlogs == 0,
        'general_eligibility': student.is_eligible,
    }

    if not all(eligibility_checks.values()):
        reasons = [k.replace('_', ' ').title() for k, v in eligibility_checks.items() if not v]
        messages.error(request, f'You are not eligible for this job. Reason: {", ".join(reasons)}')
        return redirect('jobs:job_detail', job_id=job_id)

    # 2. Check for duplicate applications (defense against double-click)
    try:
        application, created = Application.objects.get_or_create(
            student=student,
            job=job,
            defaults={'status': 'APPLIED'}
        )

        if created:
            messages.success(request, f'Successfully applied for {job.title}!')
            return redirect('applications:application_status')
        else:
            messages.warning(request, 'You have already applied for this job.')
            return redirect('applications:application_status')

    except IntegrityError:
        # Double-click protection
        messages.warning(request, 'Application already exists for this job.')
        return redirect('applications:application_status')
    except Exception as e:
        messages.error(request, f'Error applying for job: {str(e)}')
        return redirect('jobs:job_detail', job_id=job_id)


@student_required
def application_status_view(request):
    """
    Student views all their applications and statuses.
    """
    student = get_object_or_404(StudentProfile, user=request.user)
    applications = Application.objects.filter(student=student).order_by('-applied_date')

    # Group by status
    applied = applications.filter(status='APPLIED')
    shortlisted = applications.filter(status='SHORTLISTED')
    selected = applications.filter(status='SELECTED')
    rejected = applications.filter(status='REJECTED')

    context = {
        'applications': applications,
        'applied': applied,
        'shortlisted': shortlisted,
        'selected': selected,
        'rejected': rejected,
        'total_applications': applications.count(),
    }
    return render(request, 'applications/application_status.html', context)


@company_required
def update_application_status_view(request, application_id):
    """
    Company updates the status of an application.
    
    Critical security checks:
    1. Verify the company owns the job
    2. Verify status is valid
    """
    application = get_object_or_404(Application, id=application_id)
    company = get_object_or_404(CompanyProfile, user=request.user)

    # CRITICAL SECURITY CHECK: Verify company owns this job
    if application.job.company != company:
        messages.error(request, 'You do not have permission to update this application.')
        raise Http404('Application not found.')

    if request.method == 'POST':
        new_status = request.POST.get('status', '').strip()

        # Validate status
        valid_statuses = [choice[0] for choice in Application.STATUS_CHOICES]
        if new_status not in valid_statuses:
            messages.error(request, 'Invalid status selected.')
            return redirect('companies:job_applicants', job_id=application.job.id)

        # Update status
        old_status = application.status
        application.status = new_status
        application.save()

        messages.success(request, f'Application status updated from {old_status} to {new_status}.')
        return redirect('companies:job_applicants', job_id=application.job.id)

    context = {
        'application': application,
        'status_choices': Application.STATUS_CHOICES,
    }
    return render(request, 'applications/update_status.html', context)
