from django.shortcuts import render
from django.db.models import Count, Max
from students.models import StudentProfile
from companies.models import CompanyProfile
from jobs.models import Job
from applications.models import Application
from .decorators import superuser_required


@superuser_required
def admin_dashboard(request):
    total_students = StudentProfile.objects.count()
    total_companies = CompanyProfile.objects.count()
    total_jobs = Job.objects.count()
    total_applications = Application.objects.count()

    total_placements = Application.objects.filter(status='SELECTED').count()

    placement_rate = 0
    if total_students > 0:
        placement_rate = round((total_placements / total_students) * 100, 2)

    highest_package = Job.objects.aggregate(Max('package'))['package__max'] or 0

    branch_placements = (
        Application.objects
        .filter(status='SELECTED')
        .values('student__branch')
        .annotate(count=Count('id'))
        .order_by('-count')
    )

    status_breakdown = (
        Application.objects
        .values('status')
        .annotate(count=Count('id'))
    )

    company_job_count = (
        Job.objects
        .values('company__company_name')
        .annotate(total_jobs=Count('id'))
        .order_by('-total_jobs')[:10]
    )

    context = {
        'total_students': total_students,
        'total_companies': total_companies,
        'total_jobs': total_jobs,
        'total_applications': total_applications,
        'total_placements': total_placements,
        'placement_rate': placement_rate,
        'highest_package': highest_package,
        'branch_placements': branch_placements,
        'status_breakdown': status_breakdown,
        'company_job_count': company_job_count,
    }

    return render(request, 'college_admin/dashboard.html', context)
