from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from .models import Job
from students.models import StudentProfile
from companies.models import CompanyProfile
from applications.models import Application


@login_required(login_url='accounts:login')
def job_list_view(request):
    """
    Display jobs based on user role.
    - Students: See eligible jobs only
    - Companies: See only their own jobs
    - Admin: See all jobs
    """
    user = request.user

    # Determine role and filter jobs accordingly
    if user.is_superuser:
        # Admin sees all jobs
        jobs = Job.objects.all().order_by('-created_at')
        context = {
            'jobs': jobs,
            'is_admin': True,
        }
        return render(request, 'jobs/job_list.html', context)

    elif hasattr(user, 'company_profile'):
        # Company sees only their own jobs
        company = user.company_profile
        jobs = Job.objects.filter(company=company).order_by('-created_at')
        context = {
            'jobs': jobs,
            'is_company': True,
        }
        return render(request, 'jobs/job_list.html', context)

    elif hasattr(user, 'student_profile'):
        # Student sees only eligible jobs
        student = user.student_profile

        # Filter for eligible jobs
        eligible_jobs = Job.objects.filter(
            Q(min_cgpa__lte=student.cgpa) &
            Q(branch__in=[student.branch, 'ALL']) &
            Q(deadline__gte=timezone.now().date())
        ).order_by('-created_at')

        # Check which jobs student has already applied to
        applied_jobs_ids = Application.objects.filter(
            student=student
        ).values_list('job_id', flat=True)

        # Add flag to indicate if student applied
        for job in eligible_jobs:
            job.already_applied = job.id in applied_jobs_ids

        context = {
            'jobs': eligible_jobs,
            'student_profile': student,
            'is_student': True,
        }
        return render(request, 'jobs/job_list.html', context)

    else:
        messages.error(request, 'Invalid user role.')
        return redirect('home')


@login_required(login_url='accounts:login')
def job_detail_view(request, job_id):
    """
    Display job details with role-based information.
    - Students: See eligibility status and apply button
    - Companies: See applicant count
    - Admin: See all information
    """
    job = get_object_or_404(Job, id=job_id)
    user = request.user

    context = {
        'job': job,
        'applicant_count': job.applications.count(),
    }

    # Student-specific context
    if hasattr(user, 'student_profile'):
        student = user.student_profile

        # Check eligibility again (defense in depth)
        is_eligible = (
            student.cgpa >= job.min_cgpa and
            (job.branch == student.branch or job.branch == 'ALL') and
            job.deadline >= timezone.now().date() and
            student.is_eligible
        )

        # Check if already applied
        already_applied = Application.objects.filter(
            student=student,
            job=job
        ).exists()

        context.update({
            'is_student': True,
            'is_eligible': is_eligible,
            'already_applied': already_applied,
            'student': student,
            'eligibility_reasons': {
                'cgpa': student.cgpa >= job.min_cgpa,
                'branch': job.branch == 'ALL' or job.branch == student.branch,
                'deadline': job.deadline >= timezone.now().date(),
                'no_backlogs': student.backlogs == 0,
            }
        })

    # Company-specific context
    elif hasattr(user, 'company_profile'):
        company = user.company_profile
        is_owner = job.company == company

        context.update({
            'is_company': True,
            'is_owner': is_owner,
        })

    # Admin context
    elif user.is_superuser:
        context.update({
            'is_admin': True,
        })

    return render(request, 'jobs/job_detail.html', context)
