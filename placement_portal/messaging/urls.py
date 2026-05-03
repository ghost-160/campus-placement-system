from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list_view, name='list'),
    path('start/<int:company_id>/', views.start_conversation_view, name='start'),
    path('<int:conversation_id>/', views.conversation_detail_view, name='detail'),
    path('<int:conversation_id>/send/', views.send_message_view, name='send'),
]
