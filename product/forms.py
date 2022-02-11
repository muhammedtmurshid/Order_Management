from django import forms
from django.forms import modelformset_factory

from product.models import Category, Product, Order, OrderProduct


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')

class EditCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('__all__')

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')

class EditProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('__all__')

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('shop', 'staff', 'status')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

OrderFormset = modelformset_factory(
    OrderProduct,
    OrderForm,
    fields=('product', 'quantity'),
    extra=1,
    widgets={'product': forms.Select(attrs={'class': 'form-control',}),}
)

class EditOrderProductForm(forms.ModelForm):
    class Meta:
        model = OrderProduct
        fields = ('product', 'quantity')


class EditOrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('__all__')

