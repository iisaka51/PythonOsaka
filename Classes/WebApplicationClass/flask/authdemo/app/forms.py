from flask_wtf import FlaskForm
from wtforms_alchemy import ModelForm
from app.models import User

class LoginForm(ModelForm, FlaskForm):
    class Meta:
        model = User
