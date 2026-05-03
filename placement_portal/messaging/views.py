from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .models import Conversation, Message
from students.models import StudentProfile
from companies.models import CompanyProfile
from applications.models import Application


@login_required
def start_conversation_view(request, company_id):
    # Only students may start a conversation (Option A)
    if not hasattr(request.user, 'student_profile'):
        raise Http404

    student = request.user.student_profile

    # Check if student applied to any job from this company
    has_applied = Application.objects.filter(
        student=student,
        job__company_id=company_id
    ).exists()

    if not has_applied:
        raise Http404

    company = get_object_or_404(CompanyProfile, id=company_id)

    conversation, created = Conversation.objects.get_or_create(
        student=student,
        company=company
    )

    return redirect('messaging:detail', conversation_id=conversation.id)


@login_required
def conversation_list_view(request):
    # Student conversations
    if hasattr(request.user, 'student_profile'):
        conversations = Conversation.objects.filter(student=request.user.student_profile)

    # Company conversations
    elif hasattr(request.user, 'company_profile'):
        conversations = Conversation.objects.filter(company=request.user.company_profile)

    else:
        raise Http404

    return render(request, 'messaging/conversation_list.html', {
        'conversations': conversations
    })


@login_required
def conversation_detail_view(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Ownership check
    if hasattr(request.user, 'student_profile'):
        if conversation.student != request.user.student_profile:
            raise Http404

    elif hasattr(request.user, 'company_profile'):
        if conversation.company != request.user.company_profile:
            raise Http404
    else:
        raise Http404

    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

    # Mark unread messages as read (except those sent by current user)
    Message.objects.filter(
        conversation=conversation,
        is_read=False
    ).exclude(sender=request.user).update(is_read=True)

    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages
    })


@login_required
def send_message_view(request, conversation_id):
    if request.method != 'POST':
        raise Http404

    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Ownership validation
    if hasattr(request.user, 'student_profile'):
        if conversation.student != request.user.student_profile:
            raise Http404

    elif hasattr(request.user, 'company_profile'):
        if conversation.company != request.user.company_profile:
            raise Http404
    else:
        raise Http404

    content = request.POST.get('content')

    if content:
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )

    return redirect('messaging:detail', conversation_id=conversation.id)
