from django.db import models
from companies.models import CompanyProfile
from django.core.validators import MinValueValidator
from django.utils import timezone


class Job(models.Model):
    """
    Job posting model for companies.
    """
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('ECE', 'Electronics & Communication'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('EEE', 'Electrical & Electronics Engineering'),
        ('IT', 'Information Technology'),
        ('ALL', 'All Branches'),
    ]

    JOB_TYPE_CHOICES = [
        ('FT', 'Full-Time'),
        ('IT', 'Internship'),
        ('PT', 'Part-Time'),
    ]

    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=255)
    description = models.TextField()
    package = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)])
    min_cgpa = models.FloatField(validators=[MinValueValidator(0.0)])
    branch = models.CharField(max_length=10, choices=BRANCH_CHOICES)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES, default='FT')
    location = models.CharField(max_length=255, blank=True)
    deadline = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Job"
        verbose_name_plural = "Jobs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.company.company_name}"

    @property
    def is_active(self):
        """Check if job posting is still active (deadline not passed)"""
        return self.deadline >= timezone.now().date()

    @property
    def days_remaining(self):
        """Get days remaining until deadline"""
        delta = self.deadline - timezone.now().date()
        return max(0, delta.days)
