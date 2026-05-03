#!/usr/bin/env python
"""
Comprehensive redirect loop test suite.
Tests all three golden rules for redirect architecture.
"""

import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_portal.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.test import Client, TestCase
from django.contrib.auth.models import User
from students.models import StudentProfile
from companies.models import CompanyProfile


class RedirectLoopTests(TestCase):
    """Test that redirect architecture prevents loops."""

    def setUp(self):
        """Create test users for all roles."""
        self.client = Client()

        # Create superuser
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='testpass123'
        )

        # Create student user
        self.student_user = User.objects.create_user(
            username='student1',
            email='student@test.com',
            password='testpass123',
            first_name='John',
            last_name='Doe'
        )
        StudentProfile.objects.create(
            user=self.student_user,
            register_no='CSE001',
            branch='CSE',
            cgpa=7.5,
            backlogs=0
        )

        # Create company user
        self.company_user = User.objects.create_user(
            username='company1',
            email='company@test.com',
            password='testpass123',
            first_name='Tech',
            last_name='Corp'
        )
        CompanyProfile.objects.create(
            user=self.company_user,
            company_name='Tech Solutions Inc'
        )

    def test_1_unauthenticated_login_page(self):
        """RULE 1: Unauthenticated user can access login page."""
        print("\n✓ TEST 1: Unauthenticated user accessing /accounts/login/")
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        print(f"  Status: {response.status_code} (OK)")

    def test_2_authenticated_user_get_login_redirects(self):
        """RULE 1: Authenticated user on GET to login redirects based on role."""
        print("\n✓ TEST 2: Authenticated user (student) GETting /accounts/login/")
        self.client.login(username='student1', password='testpass123')
        response = self.client.get('/accounts/login/', follow=False)
        print(f"  Status: {response.status_code}")
        print(f"  Redirects to: {response.get('Location', 'None')}")
        # Should redirect to student dashboard
        self.assertEqual(response.status_code, 302)
        self.assertIn('students/dashboard', response.get('Location', ''))

    def test_3_student_login_success(self):
        """Test student login redirects to student dashboard."""
        print("\n✓ TEST 3: Student login POST and redirect")
        response = self.client.post(
            '/accounts/login/',
            {'username': 'student1', 'password': 'testpass123'},
            follow=False
        )
        print(f"  Status: {response.status_code}")
        print(f"  Redirects to: {response.get('Location', 'None')}")
        self.assertEqual(response.status_code, 302)
        self.assertIn('students/dashboard', response.get('Location', ''))

    def test_4_company_login_success(self):
        """Test company login redirects to company dashboard."""
        print("\n✓ TEST 4: Company login POST and redirect")
        response = self.client.post(
            '/accounts/login/',
            {'username': 'company1', 'password': 'testpass123'},
            follow=False
        )
        print(f"  Status: {response.status_code}")
        print(f"  Redirects to: {response.get('Location', 'None')}")
        self.assertEqual(response.status_code, 302)
        self.assertIn('companies/dashboard', response.get('Location', ''))

    def test_5_superuser_login_success(self):
        """Test superuser login redirects to admin dashboard."""
        print("\n✓ TEST 5: Superuser login POST and redirect")
        response = self.client.post(
            '/accounts/login/',
            {'username': 'admin', 'password': 'testpass123'},
            follow=False
        )
        print(f"  Status: {response.status_code}")
        print(f"  Redirects to: {response.get('Location', 'None')}")
        self.assertEqual(response.status_code, 302)
        self.assertIn('college-admin', response.get('Location', ''))

    def test_6_student_cannot_access_admin_dashboard(self):
        """RULE 2: Student accessing admin dashboard gets 302 to home (not loop)."""
        print("\n✓ TEST 6: Student accessing /college-admin/dashboard/ (should redirect to home)")
        self.client.login(username='student1', password='testpass123')
        response = self.client.get('/college-admin/dashboard/', follow=False)
        print(f"  Status: {response.status_code}")
        print(f"  Redirects to: {response.get('Location', 'None')}")
        # Should redirect to home, not login (prevents loop)
        self.assertEqual(response.status_code, 302)
        self.assertIn('home', response.get('Location', '') or response.get('Location', ''))

    def test_7_company_cannot_access_admin_dashboard(self):
        """RULE 2: Company accessing admin dashboard gets 302 to home (not loop)."""
        print("\n✓ TEST 7: Company accessing /college-admin/dashboard/ (should redirect to home)")
        self.client.login(username='company1', password='testpass123')
        response = self.client.get('/college-admin/dashboard/', follow=False)
        print(f"  Status: {response.status_code}")
        print(f"  Redirects to: {response.get('Location', 'None')}")
        self.assertEqual(response.status_code, 302)
        self.assertIn('home', response.get('Location', '') or response.get('Location', ''))

    def test_8_superuser_can_access_admin_dashboard(self):
        """RULE 2: Superuser accessing admin dashboard succeeds."""
        print("\n✓ TEST 8: Superuser accessing /college-admin/dashboard/")
        self.client.login(username='admin', password='testpass123')
        response = self.client.get('/college-admin/dashboard/', follow=False)
        print(f"  Status: {response.status_code}")
        # Should return 200 (success)
        self.assertEqual(response.status_code, 200)

    def test_9_student_can_access_own_dashboard(self):
        """Test student can access their own dashboard."""
        print("\n✓ TEST 9: Student accessing /students/dashboard/")
        self.client.login(username='student1', password='testpass123')
        response = self.client.get('/students/dashboard/')
        print(f"  Status: {response.status_code}")
        self.assertEqual(response.status_code, 200)

    def test_10_company_can_access_own_dashboard(self):
        """Test company can access their own dashboard."""
        print("\n✓ TEST 10: Company accessing /companies/dashboard/")
        self.client.login(username='company1', password='testpass123')
        response = self.client.get('/companies/dashboard/')
        print(f"  Status: {response.status_code}")
        self.assertEqual(response.status_code, 200)

    def test_11_logout_redirects_to_login(self):
        """Test logout redirects to login page."""
        print("\n✓ TEST 11: Logout and redirect")
        self.client.login(username='student1', password='testpass123')
        response = self.client.get('/accounts/logout/', follow=False)
        print(f"  Status: {response.status_code}")
        print(f"  Redirects to: {response.get('Location', 'None')}")
        self.assertEqual(response.status_code, 302)
        self.assertIn('accounts/login', response.get('Location', ''))

    def test_12_invalid_login_shows_form_not_redirect(self):
        """Test invalid login shows login form, doesn't redirect."""
        print("\n✓ TEST 12: Invalid credentials on login (should show form, not redirect)")
        response = self.client.post(
            '/accounts/login/',
            {'username': 'student1', 'password': 'wrongpassword'},
            follow=False
        )
        print(f"  Status: {response.status_code}")
        # Should return 200 (form re-rendered) not redirect
        self.assertEqual(response.status_code, 200)
        self.assertIn('login', response.content.decode().lower())


if __name__ == '__main__':
    from django.test.utils import get_runner
    from django.conf import settings

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=True)
    
    print("\n" + "="*70)
    print("REDIRECT LOOP TEST SUITE")
    print("Testing all three golden rules of redirect architecture")
    print("="*70)
    
    failures = test_runner.run_tests(['__main__'])
    
    if failures == 0:
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED - REDIRECT SYSTEM IS STABLE")
        print("="*70)
        sys.exit(0)
    else:
        print("\n" + "="*70)
        print("❌ SOME TESTS FAILED - SEE ABOVE")
        print("="*70)
        sys.exit(1)
