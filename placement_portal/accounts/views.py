from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods


def get_redirect_url(user):
    """
    FINAL STABLE VERSION (no reverse issues)
    """
    if hasattr(user, 'student_profile'):
        return '/students/dashboard/'
    elif hasattr(user, 'company_profile'):
        return '/companies/dashboard/'
    elif user.is_superuser:
        return '/admin/'
    return '/'


@require_http_methods(["GET", "POST"])
def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        role = request.POST.get('role', '').strip()

        # Validation
        if not all([first_name, email, username, password, role]):
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/register.html', {'roles': ['student', 'company']})

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html', {'roles': ['student', 'company']})

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return render(request, 'accounts/register.html', {'roles': ['student', 'company']})

        if role not in ['student', 'company']:
            messages.error(request, 'Invalid role selected.')
            return render(request, 'accounts/register.html', {'roles': ['student', 'company']})

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'accounts/register.html', {'roles': ['student', 'company']})

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html', {'roles': ['student', 'company']})

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            messages.success(request, 'Account created successfully! Please login.')
            return redirect('/accounts/login/')

        except Exception as e:
            messages.error(request, f'Error creating account: {str(e)}')
            return render(request, 'accounts/register.html', {'roles': ['student', 'company']})

    return render(request, 'accounts/register.html', {'roles': ['student', 'company']})


@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated and request.method == 'GET':
        return redirect(get_redirect_url(request.user))

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'accounts/login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {user.username}!')
            return redirect(get_redirect_url(user))
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


@login_required(login_url='/accounts/login/')
def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('/accounts/login/')