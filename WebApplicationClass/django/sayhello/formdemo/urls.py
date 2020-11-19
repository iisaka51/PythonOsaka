from django.urls import path, include, re_path
from . import views

app_name = 'formdemo'
urlpatterns = [
    path('', views.UserListView.as_view(), name='user_list'),
    path('list/', views.UserListView.as_view(), name='user_list'),
    path('add/', views.UserCreateView.as_view(), name='user_create'),
    path('edit/<int:pk>/',
           views.UserUpdateView.as_view(), name='user_update'),
    path('show/<int:pk>/',
           views.UserDetailView.as_view(), name='user_detail'),
    path('delete/<int:pk>/',
           views.UserDeleteView.as_view(), name='user_delete'),
]
