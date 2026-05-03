from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import Http404
from django.views.decorators.http import require_http_methods
from .models import CompanyProfile
from jobs.models import Job
from applications.models import Application


def company_required(view_func):
    """
    Decorator to check if user has a company profile.
    Redirects to login if not a company.
    """
    def wrapper(request, *args, **kwargs):
        if not hasattr(request.user, 'company_profile'):
            messages.error(request, 'This area is only for companies.')
            return redirect('accounts:login')
        return view_func(request, *args, **kwargs)
    return login_required(login_url='accounts:login')(wrapper)


@company_required
def profile_view(request):
    """
    Create or update company profile.
    """
    company_profile, created = CompanyProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        company_name = request.POST.get('company_name', '').strip()
        description = request.POST.get('description', '').strip()
        website = request.POST.get('website', '').strip()
        contact_email = request.POST.get('contact_email', '').strip()
        contact_phone = request.POST.get('contact_phone', '').strip()
        logo = request.FILES.get('logo')

        # Validation
        if not company_name:
            messages.error(request, 'Company name is required.')
            return render(request, 'companies/profile.html', {'profile': company_profile})

        if not contact_email:
            messages.error(request, 'Contact email is required.')
            return render(request, 'companies/profile.html', {'profile': company_profile})

        # Update profile
        company_profile.company_name = company_name
        company_profile.description = description
        company_profile.website = website
        company_profile.contact_email = contact_email
        company_profile.contact_phone = contact_phone

        if logo:
            company_profile.logo = logo

        company_profile.save()
        messages.success(request, 'Company profile updated successfully!')
        return redirect('companies:dashboard')

    context = {
        'profile': company_profile,
    }
    return render(request, 'companies/profile.html', context)


@company_required
def dashboard_view(request):
    """
    Company dashboard showing job postings and applicant statistics.
    """
    company_profile = get_object_or_404(CompanyProfile, user=request.user)

    # Get company's jobs
    jobs = Job.objects.filter(company=company_profile).order_by('-created_at')
    total_jobs = jobs.count()

    # Count total applicants for all company jobs
    total_applicants = Application.objects.filter(
        job__company=company_profile
    ).count()

    # Get recent jobs
    recent_jobs = jobs[:5]

    context = {
        'profile': company_profile,
        'total_jobs': total_jobs,
        'total_applicants': total_applicants,
        'recent_jobs': recent_jobs,
    }
    return render(request, 'companies/dashboard.html', context)


@company_required
@require_http_methods(["GET", "POST"])
def post_job_view(request):
    """
    Create a new job posting.
    """
    company_profile = get_object_or_404(CompanyProfile, user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        package = request.POST.get('package', '').strip()
        min_cgpa = request.POST.get('min_cgpa', '').strip()
        branch = request.POST.get('branch', '').strip()
        job_type = request.POST.get('job_type', '').strip()
        location = request.POST.get('location', '').strip()
        deadline = request.POST.get('deadline', '').strip()

        # Validation
        errors = []

        if not title:
            errors.append('Job title is required.')
        if not description:
            errors.append('Job description is required.')
        if not package:
            errors.append('Package is required.')
        if not min_cgpa:
            errors.append('Minimum CGPA is required.')
        if not branch:
            errors.append('Branch is required.')
        if not deadline:
            errors.append('Deadline is required.')

        # Validate numeric fields
        if package:
            try:
                package_float = float(package)
                if package_float < 0:
                    errors.append('Package cannot be negative.')
            except ValueError:
                errors.append('Package must be a valid number.')

        if min_cgpa:
            try:
                cgpa_float = float(min_cgpa)
                if not (0 <= cgpa_float <= 10):
                    errors.append('Minimum CGPA must be between 0 and 10.')
            except ValueError:
                errors.append('Minimum CGPA must be a valid number.')

        # Validate deadline
        if deadline:
            try:
                deadline_date = timezone.datetime.strptime(deadline, '%Y-%m-%d').date()
                if deadline_date < timezone.now().date():
                    errors.append('Deadline cannot be in the past.')
            except ValueError:
                errors.append('Invalid date format. Use YYYY-MM-DD.')

        if branch not in [choice[0] for choice in Job.BRANCH_CHOICES]:
            errors.append('Invalid branch selected.')

        if job_type not in [choice[0] for choice in Job.JOB_TYPE_CHOICES]:
            errors.append('Invalid job type selected.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'companies/post_job.html', {
                'branch_choices': Job.BRANCH_CHOICES,
                'job_type_choices': Job.JOB_TYPE_CHOICES,
            })

        # Create job
        try:
            job = Job.objects.create(
                company=company_profile,
                title=title,
                description=description,
                package=package_float,
                min_cgpa=cgpa_float,
                branch=branch,
                job_type=job_type,
                location=location,
                deadline=deadline_date
            )
            messages.success(request, f'Job "{title}" posted successfully!')
            return redirect('companies:dashboard')
        except Exception as e:
            messages.error(request, f'Error posting job: {str(e)}')
            return render(request, 'companies/post_job.html', {
                'branch_choices': Job.BRANCH_CHOICES,
                'job_type_choices': Job.JOB_TYPE_CHOICES,
            })

    context = {
        'branch_choices': Job.BRANCH_CHOICES,
        'job_type_choices': Job.JOB_TYPE_CHOICES,
    }
    return render(request, 'companies/post_job.html', context)


@company_required
def view_applicants_view(request, job_id):
    """
    View applicants for a specific job.
    Only show if job belongs to the company.
    """
    company_profile = get_object_or_404(CompanyProfile, user=request.user)
    job = get_object_or_404(Job, id=job_id)

    # Security check: verify job belongs to this company
    if job.company != company_profile:
        messages.error(request, 'You do not have permission to view this.')
        raise Http404('Job not found.')

    # Get all applicants for this job
    applications = Application.objects.filter(job=job).order_by('-applied_date')

    # Group by status
    applied = applications.filter(status='APPLIED')
    shortlisted = applications.filter(status='SHORTLISTED')
    selected = applications.filter(status='SELECTED')
    rejected = applications.filter(status='REJECTED')

    context = {
        'job': job,
        'applicants': applications,
        'applied': applied,
        'shortlisted': shortlisted,
        'selected': selected,
        'rejected': rejected,
        'total_applicants': applications.count(),
    }
    return render(request, 'companies/job_applicants.html', context)
