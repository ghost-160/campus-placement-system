from django.db import models
from students.models import StudentProfile
from jobs.models import Job


class Application(models.Model):
    """
    Job application model linking students to job postings.
    Ensures one application per student per job.
    """
    STATUS_CHOICES = [
        ('APPLIED', 'Applied'),
        ('SHORTLISTED', 'Shortlisted'),
        ('SELECTED', 'Selected'),
        ('REJECTED', 'Rejected'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='APPLIED')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Application"
        verbose_name_plural = "Applications"
        unique_together = ('student', 'job')  # Prevent duplicate applications
        ordering = ['-applied_date']

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.job.title}"
