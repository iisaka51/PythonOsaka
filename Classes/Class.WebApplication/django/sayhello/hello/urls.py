from django.urls import path
from . import views

app_name = 'hello'
urlpatterns = [
    path('index/', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('artist_list/', views.artist_list, name='artist_list'),
]
