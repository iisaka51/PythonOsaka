from django.urls import path, include
from . import views

app_name = 'authdemo'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
]
