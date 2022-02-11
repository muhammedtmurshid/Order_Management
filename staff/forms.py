
from django import forms
from django.contrib.auth.forms import UserCreationForm

from core.models import User
from product.models import Order
from shop.models import Shop
from staff.models import Staff


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'is_distributor')

class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('place', 'mobile',)

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'is_distributor')


class StaffUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ('place', 'mobile')

class StaffOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('shop', )

    def __init__(self, staff, *args, **kwargs):
        super(StaffOrderForm, self).__init__(*args, **kwargs)
        self.fields['shop'].queryset = Shop.objects.filter(staff=staff)


class Staff_Edit_Order(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('shop',)

    def __init__(self, staff, *args, **kwargs):
        super(Staff_Edit_Order, self).__init__(*args, **kwargs)
        self.fields['shop'].queryset = Shop.objects.filter(staff=staff)
