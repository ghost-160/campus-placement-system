from django.db import models
from django.contrib.auth.models import User


class CompanyProfile(models.Model):
    """
    Company profile model for campus placement system.
    OneToOne relationship with Django User model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profiles"
        ordering = ['-created_at']

    def __str__(self):
        return self.company_name
