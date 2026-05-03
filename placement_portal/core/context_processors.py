def role_flags(request):
    """Provide simple role flags for templates to avoid attribute errors."""
    user = getattr(request, 'user', None)
    is_student = False
    is_company = False
    try:
        if user and user.is_authenticated:
            is_student = hasattr(user, 'student_profile')
            is_company = hasattr(user, 'company_profile')
    except Exception:
        is_student = False
        is_company = False

    return {
        'is_student': is_student,
        'is_company': is_company,
    }
