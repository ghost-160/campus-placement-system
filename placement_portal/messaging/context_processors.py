from .models import Message


def unread_messages(request):
    if request.user.is_authenticated:
        count = Message.objects.filter(is_read=False).exclude(sender=request.user).count()
        return {'unread_count': count}
    return {}
