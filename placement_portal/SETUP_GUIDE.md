"""
Campus Placement Management System - Setup and Quick Reference Guide
=====================================================================

This document provides setup, testing, and deployment instructions for the 
Campus Placement Management System built with Django.

## QUICK START

### 1. Environment Setup

```bash
# Activate virtual environment
# Windows:
.\.venv\Scripts\activate

# macOS/Linux:
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py migrate
```

### 4. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

then use these credentials to access:
- Admin Panel: http://localhost:8000/admin/
- Analytics Dashboard: http://localhost:8000/accounts/admin/dashboard/

### 5. Run Development Server

```bash
python manage.py runserver
```

Access at: http://localhost:8000/

---

## TESTING CHECKLIST

### Student User Flow:
1. ✅ Register as Student
2. ✅ Login
3. ✅ Complete Student Profile (Register No, CGPA, Skills, Resume)
4. ✅ View Eligible Jobs
5. ✅ Apply for Job
6. ✅ View Application Status

### Company User Flow:
1. ✅ Register as Company
2. ✅ Login
3. ✅ Complete Company Profile
4. ✅ Post a Job
5. ✅ View Job Applicants
6. ✅ Update Application Status

### Admin User Flow:
1. ✅ Login (with superuser credentials)
2. ✅ Access Admin Panel (/admin/)
3. ✅ Access Analytics Dashboard (/accounts/admin/dashboard/)
4. ✅ View Statistics
5. ✅ Manage Users, Students, Companies, Jobs, Applications

### Security Testing:
1. ✅ Student trying to access /companies/* → Blocked
2. ✅ Company trying to access /students/* → Blocked
3. ✅ Student applying twice for same job → Blocked
4. ✅ Company updating another company's job → Blocked
5. ✅ Unauthenticated users accessing protected pages → Redirected to login
6. ✅ Expired job filtering → Correctly filtered

---

## PROJECT STRUCTURE

### Core Apps:

**accounts/**
- User authentication (register, login, logout)
- Admin analytics dashboard
- Role detection (student, company, admin)

**students/**
- StudentProfile model
- Profile management
- View eligible jobs
- Dashboard with application stats

**companies/**
- CompanyProfile model
- Profile management
- Post jobs
- View applicants for own jobs

**jobs/**
- Job model with filtering
- Job listing (role-based)
- Job detail with eligibility checks

**applications/**
- Application model
- Apply for job (with duplicate prevention)
- View application status
- Update application status (company only)

### Key Features:

1. **Role-Based Access Control**
   - Student, Company, Admin roles
   - Profile-based (no custom User model)

2. **Job Eligibility System**
   - CGPA filtering
   - Branch filtering
   - Deadline validation
   - Backlog prevention

3. **Application System**
   - Duplicate application prevention
   - Status workflow (Applied → Shortlisted → Selected/Rejected)
   - Company-only status updates
   - Ownership verification

4. **Security Features**
   - Defense-in-depth validation
   - Ownership verification on all operations
   - IntegrityError handling for race conditions
   - CSRF protection
   - SQL injection prevention (Django ORM)

5. **Admin Analytics**
   - Total students, companies, jobs, applications
   - Placement statistics
   - Branch-wise placement count
   - Highest package tracking
   - Company-wise job postings

---

## DEPLOYMENT

### Prepare for Production:

```bash
# Collect static files
python manage.py collectstatic --noinput

# Install production server
pip install gunicorn whitenoise
```

### Environment Variables (Production):

```bash
export DEBUG=False
export ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
export SECRET_KEY=your-very-secret-key-change-this
export DATABASE_URL=postgresql://user:password@host/dbname
```

### Run with Gunicorn:

```bash
gunicorn placement_portal.wsgi --bind 0.0.0.0:8000
```

### Database (Production):

For PostgreSQL instead of SQLite:

```bash
pip install psycopg2-binary
```

Update settings.py:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'placement_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## ADMIN PANEL USAGE

### Access Django Admin:
Navigate to: `/admin/`

### Available Models:
1. **Users** - Manage all user accounts
2. **Student Profiles** - Edit student profiles directly
3. **Company Profiles** - Edit company profiles directly
4. **Jobs** - Create/edit/delete job postings
5. **Applications** - View and manage applications
6. **Groups & Permissions** - Advanced access control

---

## IMPORTANT SECURITY REMINDERS

1. **Change SECRET_KEY before deploying to production**
   - Generate a new one using: `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`

2. **Use environment variables for sensitive data**
   - Never commit .env files to version control
   - Use .env.example for documentation

3. **Set DEBUG=False in production**
   - Never leave DEBUG=True in production

4. **Use HTTPS in production**
   - Configure SECURE_SSL_REDIRECT = True

5. **Configure ALLOWED_HOSTS properly**
   - Don't use wildcard (*) in production

6. **Use strong database passwords**

---

## TROUBLESHOOTING

### 1. "No such table" error after migration
```bash
python manage.py migrate
```

### 2. Static files not loading
```bash
python manage.py collectstatic
```

### 3. Permission denied accessing media files
Ensure `media/` folder has proper permissions:
```bash
chmod -R 755 media/
```

### 4. Port 8000 already in use
```bash
python manage.py runserver 8001
```

### 5. Database locked (SQLite)
Delete db.sqlite3 and run migrations fresh (dev only):
```bash
rm db.sqlite3
python manage.py migrate
```

---

## NEXT STEPS

### For Production Deployment:
- [ ] Change SECRET_KEY
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use PostgreSQL
- [ ] Deploy using Gunicorn + Nginx
- [ ] Install SSL certificate
- [ ] Configure backups

### For Enhanced Features:
- [ ] Email notifications
- [ ] SMS notifications
- [ ] REST API (Django REST Framework)
- [ ] Advanced analytics with Chart.js
- [ ] Performance metrics dashboard
- [ ] Automated test suite

---

## PROJECT STATISTICS

**Models Created:** 5
- User (Django built-in)
- StudentProfile
- CompanyProfile
- Job
- Application

**Views Created:** 15+
- Authentication (3)
- Student (3)
- Company (4)
- Jobs (2)
- Applications (3)
- Admin Dashboard (1)

**Templates Created:** 12+
- Login, Register, Home
- Student Dashboard, Profile, Jobs
- Company Dashboard, Profile, Post Job, View Applicants
- Job List, Job Detail
- Application Status, Update Status
- Admin Dashboard

**Security Features:** 8+
- Role-based access control
- Ownership verification
- Duplicate application prevention
- Eligibility filtering
- IntegrityError handling
- CSRF protection
- SQL injection prevention
- Defense-in-depth validation

---

## SUPPORT & DOCUMENTATION

For Django documentation: https://docs.djangoproject.com/en/6.0/

For this project, refer to:
- `/accounts/` - Authentication logic
- `/students/` - Student features
- `/companies/` - Company features
- `/jobs/` - Job filtering logic
- `/applications/` - Application workflow

---

## FILE LOCATION GUIDE

```
placement_portal/
├── manage.py                 # Django management script
├── db.sqlite3                # Development database
├── requirements.txt          # Python dependencies
├── placement_portal/         # Main project folder
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL configuration
│   ├── wsgi.py              # WSGI for deployment
│   └── asgi.py              # ASGI for async
├── accounts/                # Authentication app
├── students/                # Student features app
├── companies/               # Company features app
├── jobs/                    # Job listing app
├── applications/            # Application management app
├── templates/               # Root templates
├── static/                  # CSS, JS, images
├── media/                   # User uploads (resumes, logos)
└── staticfiles/             # Collected static files (production)
```

---

Generated: February 13, 2026
Django Version: 6.0.2
Python Version: 3.14+

"""