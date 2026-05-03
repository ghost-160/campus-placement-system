from django.db import models
from django.conf import settings


class Conversation(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE, related_name='conversations')
    company = models.ForeignKey('companies.CompanyProfile', on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (('student', 'company'),)

    def __str__(self):
        return f"Conversation: {self.student} <-> {self.company}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp:%Y-%m-%d %H:%M:%S}"
