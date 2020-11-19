from django.urls import path, include
from . import views

app_name = 'crispy'
urlpatterns = [
    path('add/', views.UserCreateView.as_view(), name='user_create'),
]
