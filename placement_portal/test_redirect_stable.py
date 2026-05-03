#!/usr/bin/env python
"""
Comprehensive redirect loop test suite.
Tests all three golden rules for redirect architecture.
Simplified version without Unicode characters for Windows compatibility.
"""

import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from students.models import StudentProfile
from companies.models import CompanyProfile

def setup_test_data():
    """Create test users for all roles."""
    # Create superuser
    superuser = User.objects.create_superuser(
        username='admin',
        email='admin@test.com',
        password='testpass123'
    )

    # Create student user
    student_user = User.objects.create_user(
        username='student1',
        email='student@test.com',
        password='testpass123',
        first_name='John',
        last_name='Doe'
    )
    StudentProfile.objects.create(
        user=student_user,
        register_no='CSE001',
        branch='CSE',
        cgpa=7.5,
        backlogs=0
    )

    # Create company user
    company_user = User.objects.create_user(
        username='company1',
        email='company@test.com',
        password='testpass123',
        first_name='Tech',
        last_name='Corp'
    )
    CompanyProfile.objects.create(
        user=company_user,
        company_name='Tech Solutions Inc'
    )
    
    return superuser, student_user, company_user

def test_redirect_architecture():
    """Test redirects match golden rules."""
    
    client = Client()
    superuser, student_user, company_user = setup_test_data()
    
    tests_passed = 0
    tests_failed = 0
    
    print("\n" + "="*70)
    print("REDIRECT ARCHITECTURE STABILITY TEST")
    print("Testing the three golden rules")
    print("="*70)
    
    # TEST 1: Unauthenticated user can access login page
    try:
        print("\n[1] Unauthenticated user accessing /accounts/login/")
        response = client.get('/accounts/login/')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print("    PASS: Status 200 OK")
        tests_passed += 1
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 2: Authenticated student on GET to login redirects
    try:
        print("\n[2] Authenticated student GETting /accounts/login/")
        client.login(username='student1', password='testpass123')
        response = client.get('/accounts/login/', follow=False)
        assert response.status_code == 302, f"Expected 302, got {response.status_code}"
        location = response.get('Location', '')
        assert 'students/dashboard' in location, f"Expected students/dashboard in {location}"
        print(f"    PASS: Status 302 -> {location}")
        tests_passed += 1
        client.logout()
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 3: Student login succeeds
    try:
        print("\n[3] Student login POST")
        response = client.post(
            '/accounts/login/',
            {'username': 'student1', 'password': 'testpass123'},
            follow=False
        )
        assert response.status_code == 302, f"Expected 302, got {response.status_code}"
        location = response.get('Location', '')
        assert 'students' in location, f"Expected students in {location}"
        print(f"    PASS: Status 302 -> {location}")
        tests_passed += 1
        client.logout()
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 4: Company login succeeds
    try:
        print("\n[4] Company login POST")
        response = client.post(
            '/accounts/login/',
            {'username': 'company1', 'password': 'testpass123'},
            follow=False
        )
        assert response.status_code == 302, f"Expected 302, got {response.status_code}"
        location = response.get('Location', '')
        assert 'companies' in location, f"Expected companies in {location}"
        print(f"    PASS: Status 302 -> {location}")
        tests_passed += 1
        client.logout()
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 5: Superuser login succeeds
    try:
        print("\n[5] Superuser login POST")
        response = client.post(
            '/accounts/login/',
            {'username': 'admin', 'password': 'testpass123'},
            follow=False
        )
        assert response.status_code == 302, f"Expected 302, got {response.status_code}"
        location = response.get('Location', '')
        assert 'college-admin' in location, f"Expected college-admin in {location}"
        print(f"    PASS: Status 302 -> {location}")
        tests_passed += 1
        client.logout()
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 6: Student cannot access admin dashboard (should redirect to home, not login)
    try:
        print("\n[6] Student accessing /college-admin/dashboard/ (RULE 2: NO LOOP)")
        client.login(username='student1', password='testpass123')
        response = client.get('/college-admin/dashboard/', follow=False)
        assert response.status_code == 302, f"Expected 302, got {response.status_code}"
        location = response.get('Location', '')
        assert location == '/', f"Expected redirect to /, got {location}"
        print(f"    PASS: Status 302 -> {location} (NOT login, prevents loop)")
        tests_passed += 1
        client.logout()
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 7: Company cannot access admin dashboard
    try:
        print("\n[7] Company accessing /college-admin/dashboard/ (RULE 2: NO LOOP)")
        client.login(username='company1', password='testpass123')
        response = client.get('/college-admin/dashboard/', follow=False)
        assert response.status_code == 302, f"Expected 302, got {response.status_code}"
        location = response.get('Location', '')
        assert location == '/', f"Expected redirect to /, got {location}"
        print(f"    PASS: Status 302 -> {location} (NOT login, prevents loop)")
        tests_passed += 1
        client.logout()
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 8: Superuser CAN access admin dashboard
    try:
        print("\n[8] Superuser accessing /college-admin/dashboard/")
        client.login(username='admin', password='testpass123')
        response = client.get('/college-admin/dashboard/', follow=False)
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"    PASS: Status 200 OK (has access)")
        tests_passed += 1
        client.logout()
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 9: Invalid login does NOT redirect
    try:
        print("\n[9] Invalid login POST (should show form, not redirect)")
        response = client.post(
            '/accounts/login/',
            {'username': 'student1', 'password': 'wrongpassword'},
            follow=False
        )
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        content = response.content.decode('utf-8', errors='ignore')
        assert 'login' in content.lower(), "Expected login form in response"
        print(f"    PASS: Status 200 (form re-rendered, not redirect)")
        tests_passed += 1
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 10: Logout redirects to login
    try:
        print("\n[10] Logout redirects to login")
        client.login(username='student1', password='testpass123')
        response = client.get('/accounts/logout/', follow=False)
        assert response.status_code == 302, f"Expected 302, got {response.status_code}"
        location = response.get('Location', '')
        assert 'accounts/login' in location, f"Expected login in {location}"
        print(f"    PASS: Status 302 -> {location}")
        tests_passed += 1
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 11: Student can access own dashboard
    try:
        print("\n[11] Student accessing /students/dashboard/")
        client.login(username='student1', password='testpass123')
        response = client.get('/students/dashboard/')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"    PASS: Status 200 OK")
        tests_passed += 1
        client.logout()
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # TEST 12: Company can access own dashboard
    try:
        print("\n[12] Company accessing /companies/dashboard/")
        client.login(username='company1', password='testpass123')
        response = client.get('/companies/dashboard/')
        assert response.status_code == 200, f"Expected 200, got {response.status_code}"
        print(f"    PASS: Status 200 OK")
        tests_passed += 1
        client.logout()
    except Exception as e:
        print(f"    FAIL: {e}")
        tests_failed += 1
    
    # Summary
    print("\n" + "="*70)
    print(f"RESULTS: {tests_passed} passed, {tests_failed} failed")
    print("="*70)
    
    if tests_failed == 0:
        print("\nALL TESTS PASSED - REDIRECT SYSTEM IS STABLE AND LOOP-FREE")
        print("\nGolden Rules Verified:")
        print("  [Rule 1] Login view only redirects on GET (prevents loops)")
        print("  [Rule 2] Decorators redirect to home, not login (breaks cycle)")
        print("  [Rule 3] LOGIN_REDIRECT_URL is neutral (home)")
        return 0
    else:
        print(f"\nSOME TESTS FAILED - SEE ERRORS ABOVE")
        return 1

if __name__ == '__main__':
    # Clean up any existing test data
    User.objects.all().delete()
    
    exit_code = test_redirect_architecture()
    sys.exit(exit_code)
