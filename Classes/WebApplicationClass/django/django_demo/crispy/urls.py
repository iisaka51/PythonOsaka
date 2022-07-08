from django.urls import path, include
from . import views

app_name = 'crispy'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('list/', views.ProductListView.as_view(), name='product_list'),
    path('add/', views.ProductCreateView.as_view(), name='product_create'),
    path('edit/<int:pk>/',
           views.ProductUpdateView.as_view(), name='product_update')
]

