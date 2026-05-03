from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def superuser_required(view_func):
    """
    Decorator to restrict view access to superusers only.
    Redirects to home page if user is not a superuser (not back to login to avoid loops).
    """
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        # Not a superuser - redirect to home (not login to avoid redirect loop)
        return redirect('core:home')
    return wrapper
