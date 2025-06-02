# chatapp/urls.py
from django.urls import path
from . import views

app_name = 'chatapp'  
urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('chat/clear/', views.clear_chat, name='clear_chat'),
]