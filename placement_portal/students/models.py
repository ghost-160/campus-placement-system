from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class StudentProfile(models.Model):
    BRANCH_CHOICES = [
        ('CSE', 'Computer Science & Engineering'),
        ('ECE', 'Electronics & Communication'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
        ('EEE', 'Electrical & Electronics Engineering'),
        ('IT', 'Information Technology'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    # FIXED FIELD (IMPORTANT)
    register_no = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    branch = models.CharField(
        max_length=10,
        choices=BRANCH_CHOICES,
        blank=True,
        null=True
    )

    cgpa = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        blank=True,
        null=True
    )

    skills = models.TextField(
        blank=True,
        help_text="Comma-separated list of skills"
    )

    backlogs = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} ({self.register_no or 'No Reg No'})"

    def clean(self):
        if self.register_no and len(self.register_no) < 3:
            raise ValidationError("Register number must be at least 3 characters.")

    @property
    def is_eligible(self):
        return self.backlogs == 0 and (self.cgpa or 0) >= 6.0