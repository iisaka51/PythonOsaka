from django.views.generic import CreateView, UpdateView, ListView
from .models import User
from .forms import UserForm

class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'crispy_user_form.html'

class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'crispy_user_update.html'
