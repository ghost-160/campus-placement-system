# Campus Placement Management System

A production-ready Django web application for managing campus placements with role-based authentication, job eligibility filtering, and comprehensive admin analytics.

## 🎯 Features

### For Students
- ✅ User registration with role selection
- ✅ Complete student profile (registration number, branch, CGPA, skills, resume)
- ✅ View eligible jobs based on CGPA and branch
- ✅ Apply for jobs with duplicate prevention
- ✅ Track application status (Applied → Shortlisted → Selected/Rejected)
- ✅ Dashboard with placement statistics

### For Companies
- ✅ User registration as employer
- ✅ Company profile management (logo, website, description)
- ✅ Post job openings with salary, eligibility criteria
- ✅ View applicants for posted jobs
- ✅ Update application status
- ✅ Dashboard with job and applicant statistics

### For Administrators
- ✅ Full user management
- ✅ Analytics dashboard with placement statistics
- ✅ Branch-wise placement tracking
- ✅ Highest package tracking
- ✅ Company-wise job postings overview
- ✅ Django admin panel for complete data management

## 🔒 Security Features

### Role-Based Access Control
- **Student Role**: Can only access student features, eligible jobs, and own applications
- **Company Role**: Can only access company features, post jobs, and manage own job applicants
- **Admin Role**: Full system access and analytics

### Data Protection
- **Ownership Verification**: Companies can only edit/view their own jobs and applicants
- **Duplicate Prevention**: Students cannot apply twice for the same job
- **Eligibility Validation**: Multiple layers of CGPA, branch, and deadline checks
- **CSRF Protection**: All forms include CSRF tokens
- **SQL Injection Prevention**: Django ORM protects against injection attacks

## 📊 Database Models

```
User (Django built-in)
├── StudentProfile (OneToOne)
│   ├── register_no
│   ├── branch
│   ├── cgpa
│   ├── skills
│   ├── backlogs
│   └── resume (FileField)
│
├── CompanyProfile (OneToOne)
│   ├── company_name
│   ├── description
│   ├── website
│   ├── logo
│   ├── contact_email
│   └── contact_phone
│
└── Job (ForeignKey: Company)
    ├── title
    ├── description
    ├── package
    ├── min_cgpa
    ├── branch
    ├── job_type
    ├── location
    └── deadline
        │
        └── Application (ForeignKey: Student + Job)
            ├── status (APPLIED, SHORTLISTED, SELECTED, REJECTED)
            ├── applied_date
            └── updated_date
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip
- Git

### Installation

```bash
# Clone or download the project
cd "placement_portal"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.\.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Access the application at: **http://localhost:8000**

## 🎓 Default URLs

| URL | Purpose |
|-----|---------|
| `/` | Home page |
| `/accounts/register/` | User registration |
| `/accounts/login/` | User login |
| `/accounts/logout/` | User logout |
| `/students/dashboard/` | Student dashboard |
| `/students/profile/` | Student profile management |
| `/students/jobs/` | View eligible jobs |
| `/jobs/` | Public job listing |
| `/jobs/<id>/` | Job details |
| `/applications/apply/<job_id>/` | Apply for job |
| `/applications/status/` | View application status |
| `/companies/dashboard/` | Company dashboard |
| `/companies/profile/` | Company profile management |
| `/companies/post-job/` | Post new job |
| `/companies/job/<id>/applicants/` | View applicants |
| `/accounts/admin/dashboard/` | Admin analytics dashboard |
| `/admin/` | Django admin panel |

## 📝 Testing Scenarios

### Scenario 1: Student Placement Journey
1. Register as student
2. Fill profile (CGPA: 7.5, Branch: CSE, No backlogs)
3. View eligible jobs
4. Apply for job
5. Track status as company updates it

### Scenario 2: Company Hiring Process
1. Register as company
2. Fill company profile
3. Post job (min CGPA: 7.0, Branch: CSE, Package: 12 LPA)
4. View applications
5. Update student status (Shortlisted → Selected)

### Scenario 3: Admin Analytics
1. Login as admin
2. View analytics dashboard
3. Check placement statistics
4. Analyze branch-wise placements
5. Track highest package

## 🔧 Production Deployment

### Prepare for Production

```bash
# Collect static files
python manage.py collectstatic --noinput

# Install production server
pip install gunicorn
```

### Environment Variables

Create a `.env` file:
```env
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@host/dbname
```

### Deploy with Gunicorn

```bash
gunicorn placement_portal.wsgi --bind 0.0.0.0:8000
```

### Nginx Configuration (Recommended)

Configure Nginx as reverse proxy for Gunicorn.

### Database Migration

Use PostgreSQL for production:

```bash
pip install psycopg2-binary
```

Update `settings.py` with PostgreSQL connection details.

## 📊 Technical Stack

- **Backend**: Django 6.0.2
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Frontend**: Bootstrap 5
- **Server**: Gunicorn
- **Static Files**: WhiteNoise
- **Python**: 3.14+

## 📦 Dependencies

See `requirements.txt` for complete list:
- Django
- Pillow (image handling)
- Gunicorn (production server)
- WhiteNoise (static files serving)

## 🐛 Common Issues & Solutions

### Issue: "No such table" error
```bash
python manage.py migrate
```

### Issue: Static files not loading
```bash
python manage.py collectstatic
```

### Issue: Port 8000 in use
```bash
python manage.py runserver 8001
```

### Issue: Database locked
```bash
# (Dev only) Delete and recreate database
rm db.sqlite3
python manage.py migrate
```

## 📚 Documentation

For detailed setup and deployment instructions, see: **SETUP_GUIDE.md**

## 🎓 Educational Value

This project demonstrates:
- ✅ Multi-role Django application architecture
- ✅ Profile-based authentication system
- ✅ Complex database relationships and queries
- ✅ Advanced filtering and ORM usage
- ✅ Security best practices
- ✅ Production-ready code structure
- ✅ Form validation and error handling
- ✅ Template inheritance and reusability
- ✅ Admin customization
- ✅ Deployment configuration

Perfect for **MCA projects**, **portfolio development**, or **learning Django**.

## 📄 License

This project is provided for educational purposes.

## 👨‍💻 Author

Campus Placement Management System
Built with Django
February, 2026

## 🤝 Contributing

Feel free to fork and improve this project!

## ⭐ Show Your Support

If this project helped you, please star it!

---

**Happy Coding! 🚀**
