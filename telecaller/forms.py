from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import User
from telecaller.models import TeleCaller


class TeleUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_telecaller')

class TeleForm(forms.ModelForm):
    class Meta:
        model = TeleCaller
        fields = ('mobile', 'place')

class UpdateUserTeleForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_telecaller')

class UpdateTeleForm(forms.ModelForm):
    class Meta:
        model = TeleCaller
        fields = ('mobile', 'place')