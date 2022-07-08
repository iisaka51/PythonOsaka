from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Fieldset
from crispy_forms.bootstrap import Field
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'nickname', 'about_you')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-userform'
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.add_input(Submit('save', 'Save User',
                              css_class='btn-success'))
        self.helper.layout = Layout(
           Fieldset('User Name',
                    Field('name', placeholder='user name for login',
                          css_class="some-class"),
                    Field('email', placeholder="Your Email address"),),
           Fieldset('Profile',
                    Field('nickname', placeholder="Your nickname",
                          css_class="some-class"),
                    Field('about_you', placeholder="Your Profile"),))
