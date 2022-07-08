from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'nickname', 'about_you')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save User'))
