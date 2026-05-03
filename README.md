# Campus Placement Management System 🎓💼

A full-stack web application built with **Django** for managing campus placements.  
This system connects **Students**, **Companies**, and **Admins** in a structured placement workflow.

---

## 🚀 Features

### 👨‍🎓 Student Module
- Student registration & login
- Profile management
- Resume upload
- View eligible jobs based on CGPA and branch
- Apply for jobs
- Track application status
- View selected applications
- Chat with company after selection

---

### 🏢 Company Module
- Company registration & login
- Company profile management
- Post new jobs
- View posted jobs
- View applicants
- Shortlist / Select / Reject students
- Chat with selected students

---

### 👨‍💼 Admin Module
- Monitor all students
- Monitor all companies
- Track placements
- Manage system data

---

### 💬 Messaging System
- Private student-company messaging
- Messaging allowed only after selection
- Thread isolation (per job + user pair)
- Inbox system
- Unread message badge

---

### 📄 Job Management
- Create jobs
- Edit jobs
- Delete jobs
- Eligibility-based job filtering
- Deadline-based active jobs

---

## 🛠 Tech Stack

### Backend
- Python
- Django

### Database
- SQLite (Development)

### Frontend
- HTML
- CSS
- Bootstrap 5
- JavaScript

### File Handling
- Resume upload (PDF)
- Company logo upload

---

## 📂 Project Structure

```bash
placement_portal/
│── accounts/
│── students/
│── companies/
│── jobs/
│── applications/
│── messaging/
│── core/
│── templates/
│── media/
│── static/
│── placement_portal/
│── manage.py
│── db.sqlite3
```

---

## ⚙ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/ghost-160/campus-placement-management-system.git
cd campus-placement-management-system
```

---

### 2️⃣ Create Virtual Environment

```bash
python -m venv .venv
```

Activate virtual environment:

Windows:

```bash
.venv\Scripts\activate
```

Mac/Linux:

```bash
source .venv/bin/activate
```

---

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install django pillow whitenoise
```

---

### 4️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

---

## 🔐 Test Credentials

### Student Login

Username:

```text
student1
```

Password:

```text
test12345
```

---

### Company Login

Username:

```text
company1
```

Password:

```text
test12345
```

---

## 🔄 System Workflow

### Student Flow

Register → Login → Complete Profile → View Jobs → Apply → Track Status → Selected → Chat

---

### Company Flow

Register → Login → Complete Profile → Post Job → View Applicants → Select Student → Chat

---

## 📌 Key Features Implemented

- Role-based authentication
- Profile auto-creation using signals
- Resume upload system
- Eligibility matching
- Application tracking
- Selection-based messaging
- Inbox system
- Unread badge notifications

---

## 🔒 Security Features

- Role-based access protection
- Unique application constraints
- Secure file upload validation
- CSRF protection
- Messaging access control

---

## 📸 Screenshots

Add screenshots after deployment.

Suggested screenshots:
- Home Page
- Student Dashboard
- Company Dashboard
- Job Posting Page
- Job Applications Page
- Messaging Inbox

---

## 🔮 Future Improvements

- Placement analytics dashboard
- Interview scheduling system
- Email notifications
- Resume preview for companies
- Real-time chat using WebSockets
- Cloud deployment

---

## 👨‍💻 Author

Developed by **Ghost**  
GitHub: https://github.com/ghost-160

---

## 📜 License

This project is developed for educational purposes.
