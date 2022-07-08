from django.views.generic import (
        CreateView, UpdateView, ListView, DetailView, DeleteView
    )
from django.urls import reverse_lazy
from .models import User
from .forms import UserForm

class UserListView(ListView):
    model = User
    fields = ('name', 'email')
    template_name = 'user_list.html'

class UserCreateView(CreateView):
    model = User
    fields = ('name', 'email', 'nickname', 'about_you')
    template_name = 'user_form.html'
    success_url = reverse_lazy('formdemo:user_list')

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'user_update.html'
    success_url = reverse_lazy('formdemo:user_list')

class UserDetailView(DetailView):
    model = User
    form_class = UserForm
    template_name = 'user_detail.html'
    success_url = reverse_lazy('formdemo:user_list')

class UserDeleteView(DeleteView):
    model = User
    form_class = UserForm
    template_name = 'user_delete.html'
    success_url = reverse_lazy('formdemo:user_list')
