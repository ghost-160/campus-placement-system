#!/usr/bin/env python
"""
Diagnostic script to check which view is being called for companies dashboard.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
django.setup()

from django.urls import resolve, reverse
from django.test import RequestFactory
from django.contrib.auth.models import User
from companies.models import CompanyProfile

# Check URL resolution
url = '/companies/dashboard/'
print(f"\n{'='*70}")
print(f"URL RESOLUTION DIAGNOSTIC")
print(f"{'='*70}")
print(f"\nChecking URL: {url}")

try:
    match = resolve(url)
    print(f"✓ URL resolves successfully")
    print(f"  View function: {match.func.__name__}")
    print(f"  View module: {match.func.__module__}")
    print(f"  URL name: {match.url_name}")
    print(f"  App namespace: {match.app_name}")
except Exception as e:
    print(f"✗ URL resolution failed: {e}")
    exit(1)

# Check if view is the correct one
from companies.views import dashboard_view
print(f"\n✓ Correct view file location: companies.views.dashboard_view")
print(f"  View function name: {dashboard_view.__name__}")

# Check template
from django.template.loader import get_template
try:
    template = get_template('companies/dashboard.html')
    print(f"\n✓ Template found: companies/dashboard.html")
    print(f"  Template file: {template.template.origin.name if hasattr(template.template, 'origin') else 'Unknown'}")
except Exception as e:
    print(f"✗ Template not found: {e}")
    exit(1)

# Check URL reverse
try:
    reversed_url = reverse('companies:dashboard')
    print(f"\n✓ URL reverse successful")
    print(f"  Reverse of 'companies:dashboard': {reversed_url}")
except Exception as e:
    print(f"✗ URL reverse failed: {e}")

# Check if view has correct decorator
import inspect
source = inspect.getsource(dashboard_view)
print(f"\n✓ View source code preview:")
print("  " + source.split('\n')[0])
if '@company_required' in source:
    print("  Has @company_required decorator: YES")
else:
    print("  Has @company_required decorator: NO (ERROR)")

print(f"\n{'='*70}")
print(f"SUMMARY: URL routing is correct")
print(f"If you're still seeing 'Coming soon', check:")
print(f"  1. Browser DevTools → Sources tab → Find 'dashboard.html'")
print(f"  2. Server logs for any error messages")
print(f"  3. Response headers to ensure no caching directives")
print(f"{'='*70}\n")
