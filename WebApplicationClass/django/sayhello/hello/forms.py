from django import forms

class UserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=32)
    password = forms.CharField(label='Password',
                               min_length=8, max_length=32,
                               widget=forms.PasswordInput)
