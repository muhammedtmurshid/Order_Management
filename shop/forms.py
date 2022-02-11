from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import User
from shop.models import Shop


class UserShopForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_shop')

class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'place', 'staff', 'mobile')

class UserShopUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_shop')

class ShopUpdate(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'place', 'staff', 'mobile')
