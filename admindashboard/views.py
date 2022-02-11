import os

from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from core.models import User
from product.forms import CategoryForm, EditCategoryForm, ProductForm, EditProductForm, OrderForm, EditOrderForm, \
    OrderFormset, EditOrderProductForm
from product.models import Category, Product, Order, OrderProduct
from shop.forms import UserShopForm, ShopForm, UserShopUpdate, ShopUpdate
from shop.models import Shop
from staff.forms import UserForm, StaffForm, UserUpdateForm, StaffUpdateForm
from staff.models import Staff
from telecaller.forms import TeleForm, TeleUserForm, UpdateUserTeleForm, UpdateTeleForm
from telecaller.models import TeleCaller


def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            messages.info(request, 'Login Success Fully')
            return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('admin_login')
    return render(request, 'admin_login.html')


@login_required(login_url='admin_login')
def admin_dashboard(request):
    staff = Staff.objects.all()
    staff_count = staff.count()
    shop = Shop.objects.all()
    shop_count = shop.count()
    telecaller = TeleCaller.objects.all()
    telecaller_count = telecaller.count()
    products = Product.objects.all()
    products_count = products.count()
    total_order = Order.objects.all()
    total_order_count = total_order.count()
    pending_order = Order.objects.filter(status='Pending')
    pending_order_count = pending_order.count()
    completed_order = Order.objects.filter(status='Completed')
    completed_order_count = completed_order.count()
    context = {
        'staff_count':staff_count,
        'shop_count':shop_count,
        'telecaller_count':telecaller_count,
        'products_count' : products_count,
        'total_order_count':total_order_count,
        'pending_order_count':pending_order_count,
        'completed_order_count':completed_order_count
    }
    return render(request, 'admin_dashboard.html', context)


@login_required(login_url='admin_login')
def add_staff(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        staff_form = StaffForm(request.POST)
        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save()
            user.save()
            staff = staff_form.save(commit=False)
            staff.user=user
            staff.save()
            messages.info(request, 'Adding SuccessFull')
            return redirect('add_staff')
        else:
            messages.error(request, 'Error Retry')
            return redirect('add_staff')
    else:
        user_form = UserForm()
        staff_form = StaffForm()
    context = {
        'user_form' : user_form,
        'staff_form' : staff_form
    }
    return render(request, 'add_staff.html', context)


@login_required(login_url='admin_login')
def view_staff(request):
    staffs = Staff.objects.all()
    context = {
        'staffs':staffs
    }
    return render(request, 'view_staff.html', context)



@login_required(login_url='admin_login')
def edit_staff(request, id):
    staff = Staff.objects.get(id=id)
    if request.method == 'POST':
        user_update = UserUpdateForm(request.POST, instance=staff.user)
        staff_update = StaffUpdateForm(request.POST, instance=staff)
        if user_update.is_valid() and staff_update.is_valid():
            user_update.save()
            staff_update.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('view_staff')
        else:
            messages.error(request, 'Error Retry')
            return redirect(reverse('edit_staff', kwargs={'id' : id}))
    else:
        user_update = UserUpdateForm(instance=staff.user)
        staff_update = StaffUpdateForm(instance=staff)

    context = {
        'user_update':user_update,
        'staff_update':staff_update
    }
    return render(request, 'edit_staff.html', context)


@login_required(login_url='admin_login')
def delete_staff(request, id):
    staff = Staff.objects.get(id=id)
    b = User.objects.filter(username=staff)
    staff.delete()
    b.delete()
    messages.info(request, 'Deleted Sucess Fully')
    return redirect('view_staff')



@login_required(login_url='admin_login')
def add_shop(request):
    if request.method == 'POST':
        user_form = UserShopForm(request.POST)
        shop_form = ShopForm(request.POST)
        if user_form.is_valid() and shop_form.is_valid():
            user = user_form.save()
            user.save()
            shop = shop_form.save(commit=False)
            shop.user=user
            shop.save()
            messages.info(request, 'Adding SuccessFull')
            return redirect('view_shop')
        else:
            messages.error(request, 'Error Retry')
            return redirect('add_shop')

    else:
        user_form = UserShopForm()
        shop_form = ShopForm()

    context = {
        'user_form': user_form,
        'shop_form' : shop_form
    }
    return render(request, 'add_shop.html', context)


@login_required(login_url='admin_login')
def view_shop(request):
    shops = Shop.objects.all()
    return render(request, 'view_shop.html', {'shops':shops})



@login_required(login_url='admin_login')
def edit_shop(request, id):
    shop = Shop.objects.get(id=id)
    if request.method == 'POST':
        user_shopupdate = UserShopUpdate(request.POST, instance=shop.user)
        shop_update = ShopUpdate(request.POST, instance=shop)
        if user_shopupdate.is_valid() and shop_update.is_valid():
            user_shopupdate.save()
            shop_update.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('view_shop')
        else:
            messages.info(request, 'Error Retry')
            return redirect(reverse('edit_shop', kwargs={'id' : id}))
    else:
        user_shopupdate = UserShopUpdate(instance=shop.user)
        shop_update = ShopUpdate(instance=shop)

    context = {
        'user_shopupdate' : user_shopupdate,
        'shop_update' : shop_update
    }
    return render(request, 'edit_shop.html', context)



@login_required(login_url='admin_login')
def delete_shop(request, id):
    shop = Shop.objects.get(id=id)
    b = User.objects.filter(username=shop)
    shop.delete()
    b.delete()
    messages.info(request, 'Deleted SuccessFull')
    return redirect('view_shop')


@login_required(login_url='admin_login')
def add_telecaller(request):
    if request.method == 'POST':
        tele_userform = TeleUserForm(request.POST)
        tele_form = TeleForm(request.POST)
        if tele_userform.is_valid() and tele_form.is_valid():
            user = tele_userform.save()
            user.save()
            tele = tele_form.save(commit=False)
            tele.user=user
            tele.save()
            messages.info(request, 'Adding SuccessFull')
            return redirect('add_telecaller')
        else:
            messages.error(request, 'Error Retry')
            return redirect('add_telecaller')
    else:
        tele_userform = TeleUserForm()
        tele_form = TeleForm()

    context = {
        'tele_userform' : tele_userform,
        'tele_form' : tele_form
    }
    return render(request, 'add_telecaller.html', context)


@login_required(login_url='admin_login')
def view_telecaller(request):
    telecaller = TeleCaller.objects.all()
    return render(request, 'view_telecaller.html', {'telecaller':telecaller})


@login_required(login_url='admin_login')
def edit_telecaller(request, id):
    telecallers = TeleCaller.objects.get(id=id)
    if request.method == 'POST':
        tele_edit_form = UpdateUserTeleForm(request.POST, instance=telecallers.user)
        tele_update = UpdateTeleForm(request.POST, instance=telecallers)
        if tele_edit_form.is_valid() and tele_update.is_valid():
            tele_edit_form.save()
            tele_update.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('view_telecaller')
        else:
            messages.error(request, 'Error Retry')
            return redirect(reverse('edit_telecaller', kwargs={'id' : id}))
    else:
        tele_edit_form = UpdateUserTeleForm(instance=telecallers.user)
        tele_update = UpdateTeleForm(instance=telecallers)

    context = {
        'tele_edit_form' : tele_edit_form,
        'tele_update' : tele_update
    }
    return render(request, 'edit_telecaller.html', context)



@login_required(login_url='admin_login')
def delete_telecaller(request, id):
    telecaller = TeleCaller.objects.get(id=id)
    b = User.objects.filter(username=telecaller)
    telecaller.delete()
    b.delete()
    messages.info(request, 'Deleted SuccessFull')
    return redirect('view_telecaller')


@login_required(login_url='admin_login')
def add_category(request):
    if request.method == 'POST':
        category_form = CategoryForm(request.POST, request.FILES)
        if category_form.is_valid():
            category_form.save()
            messages.info(request, 'Adding SuccessFull')
            return redirect('add_category')
        else:
            messages.error(request, 'Error Retry')
            return redirect('add_category')
    else:
        category_form = CategoryForm()

    context = {
        'category_form' : category_form,
    }
    return render(request, 'category.html', context)


@login_required(login_url='admin_login')
def view_category(request):
    category = Category.objects.all()
    return render(request, 'view_category.html', {'category':category})


@login_required(login_url='admin_login')
def edit_category(request, id):
    category = Category.objects.get(id=id)
    if request.method == 'POST':
        edit_category = EditCategoryForm(request.POST, request.FILES, instance=category)
        if edit_category.is_valid():
            edit_category.save()
            messages.info(request, 'Adding SuccessFull')
            return redirect('view_category')
        else:
            messages.info(request, 'Error Retry')
            return redirect(reverse('edit_category', kwargs={'id':id}))
    else:
        edit_category = EditCategoryForm(instance=category)

    context = {
        'edit_category' : edit_category
    }
    return render(request, 'edit_category.html', context)


@login_required(login_url='admin_login')
def delete_category(request, id):
    category = Category.objects.get(id=id)
    if len(category.image) > 0:
        os.remove(category.image.path)
    category.delete()
    messages.info(request, 'Deleting SuccessFull')
    return redirect('view_category')


@login_required(login_url='admin_login')
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        if product_form.is_valid():
            product_form.save()
            messages.info(request, 'Adding SuccessFull')
            return redirect('add_product')
        else:
            messages.error(request, 'Error Retry')
            return redirect('add_product')
    else:
        product_form = ProductForm()

    context = {
        'product_form':product_form
    }
    return render(request, 'add_product.html', context)


@login_required(login_url='admin_login')
def view_product(request):
    products = Product.objects.all()
    return render(request, 'view_product.html', {'products':products})


@login_required(login_url='admin_login')
def edit_product(request, id):
    products = Product.objects.get(id=id)
    if request.method == 'POST':
        edit_product = EditProductForm(request.POST, request.FILES, instance=products)
        if edit_product.is_valid():
            edit_product.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('view_product')
        else:
            messages.error(request, 'Error Retry')
            return redirect(reverse('edit_product', kwargs={'id': id}))
    else:
        edit_product = EditProductForm(instance=products)

    context = {
        'edit_product' : edit_product
    }
    return render(request, 'edit_product.html', context)

@login_required(login_url='admin_login')
def delete_product(request, id):
    product = Product.objects.get(id=id)
    if len(product.image) > 0:
        os.remove(product.image.path)
        product.delete()
        messages.info(request, 'Deleting SuccessFull')
    return redirect('view_product')



@login_required(login_url='admin_login')
def add_order(request):
    if request.method == 'GET':
        order_form = OrderForm(request.GET or None)
        formset = OrderFormset(queryset=OrderProduct.objects.none())
    elif request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderFormset(request.POST)
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save()
            for form in formset:
                # so that `book` instance can be attached.
                orderproduct = form.save(commit=False)
                orderproduct.order = order
                orderproduct.save()
            messages.info(request, 'Adding SuccessFull')
            return redirect('add_order')
        else:
            messages.error(request, 'Error Retry')
            return redirect('add_order')
    context = {
        'order_form' : order_form,
        'formset':formset
    }
    return render(request, 'add_order.html', context)



@login_required(login_url='admin_login')
def view_order(request):
    orders = OrderProduct.objects.all().count()
    order = Order.objects.all()
    return render(request, 'view_order.html', {'orders':orders, 'order':order})



@login_required(login_url='admin_login')
def edit_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        edit_order = EditOrderForm(request.POST, instance=order)
        if edit_order.is_valid():
            edit_order.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('view_order')
        else:
            messages.info(request, 'Error Retry')
            return redirect(reverse('edit_order', kwargs={'id':id}))
    else:
        edit_order = EditOrderForm(instance=order)

    context = {
        'edit_order' : edit_order
    }
    return render(request, 'edit_order.html', context)


@login_required(login_url='admin_login')
def delete_order(request, id):
    order = Order.objects.get(id=id)
    b = OrderProduct.objects.filter(order=order)
    order.delete()
    b.delete()
    messages.info(request, 'Deleted SuccessFull')
    return redirect('view_order')


@login_required(login_url='admin_login')
def pending_order(request):
    order = Order.objects.filter(status='Pending')
    return render(request, 'pending_order.html', {'order':order})


@login_required(login_url='admin_login')
def completed_order(request):
    order = Order.objects.filter(status='Completed')
    return render(request, 'completed_order.html', {'order':order})


@login_required(login_url='admin_login')
def admin_logout(request):
    auth.logout(request)
    messages.info(request, 'Logout SuccessFull')
    return redirect('admin_login')


@login_required(login_url='admin_login')
def staff_wise_shop(request, id):
    staff = Staff.objects.get(id=id)
    shops = Shop.objects.filter(staff_id=id)
    context = {
        'staff' : staff,
        'shops' : shops,
    }
    return render(request, 'staff_wise_shop.html', context)

@login_required(login_url='admin_login')
def staff_wise_order(request, id):
    staff = Staff.objects.get(id=id)
    order = Order.objects.filter(staff_id=id)

    context = {
        'staff':staff,
        'order':order,
    }
    return render(request, 'staff_wise_order.html', context)

@login_required(login_url='admin_login')
def multiple_order(request):
    return render(request, 'multiple_order.html')

@login_required(login_url='admin_login')
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            return redirect('edit_profile')
        else:
            return redirect(reverse('edit_profile', kwargs={'id':id}))
    else:
        user_form = UserForm(instance=request.user)
    return render(request, 'edit_profile.html', {'user_form':user_form})

def order_list(request, id):
    order = Order.objects.get(id=id)
    orderproduct = OrderProduct.objects.filter(order_id=order)
    return render(request, 'order_list.html', {'order':order, 'orderproduct':orderproduct})

def order_list_edit(request, id):
    order_product = OrderProduct.objects.get(id=id)
    if request.method == 'POST':
        edit_productorder = EditOrderProductForm(request.POST, instance=order_product)
        if edit_productorder.is_valid():
            edit_productorder.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('view_order')
        else:
            messages.info(request, 'Error Retry')
            return redirect(reverse('order_list_edit', kwargs={'id':id}))
    else:
        edit_productorder = EditOrderProductForm(instance=order_product)

    context = {
        'edit_productorder' : edit_productorder
    }
    return render(request, 'order_list_edit.html', context)

def order_list_delete(request, id):
    order_product = OrderProduct.objects.get(id=id)
    order_product.delete()
    messages.info(request, 'Deleted SuccessFull')
    return redirect('view_order')

def pending_order_list(request, id):
    order = Order.objects.get(id=id)
    orderproduct = OrderProduct.objects.filter(order_id=order)
    return render(request, 'pending_order_list.html', {'orderproduct':orderproduct, 'order':order})

def pending_order_edit(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        edit_order = EditOrderForm(request.POST, instance=order)
        if edit_order.is_valid():
            edit_order.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('pending_order')
        else:
            messages.info(request, 'Error Retry')
            return redirect(reverse('pending_order_edit', kwargs={'id': id}))
    else:
        edit_order = EditOrderForm(instance=order)

    context = {
        'edit_order': edit_order
    }
    return render(request, 'pending_order_edit.html', context)

def pending_order_delete(request, id):
    order = Order.objects.get(id=id)
    b = OrderProduct.objects.filter(order=order)
    order.delete()
    b.delete()
    messages.info(request, 'Deleted SuccessFull')
    return redirect('pending_order')

def pending_order_list_edit(request, id):
    order = OrderProduct.objects.get(id=id)
    if request.method == 'POST':
        edit_productorder = EditOrderProductForm(request.POST, instance=order)
        if edit_productorder.is_valid():
            edit_productorder.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('pending_order')
        else:
            messages.info(request, 'Error Retry')
            return redirect(reverse('pending_order_list_edit', kwargs={'id': id}))
    else:
        edit_productorder = EditOrderProductForm(instance=order)

    context = {
        'edit_productorder': edit_productorder
    }
    return render(request, 'pending_order_list_edit.html', context)

def pending_order_list_delete(request, id):
    order_product = OrderProduct.objects.get(id=id)
    order_product.delete()
    messages.info(request, 'Deleted SuccessFull')
    return redirect('pending_order')


def completed_order_list(request, id):
    order = Order.objects.get(id=id)
    orderproduct = OrderProduct.objects.filter(order_id=order)
    return render(request, 'completed_order_list.html', {'orderproduct':orderproduct, 'order':order})

def completed_order_edit(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        edit_order = EditOrderForm(request.POST, instance=order)
        if edit_order.is_valid():
            edit_order.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('completed_order')
        else:
            messages.info(request, 'Error Retry')
            return redirect(reverse('completed_order_edit', kwargs={'id': id}))
    else:
        edit_order = EditOrderForm(instance=order)

    context = {
        'edit_order': edit_order
    }
    return render(request, 'completed_order_edit.html', context)

def completed_order_delete(request, id):
    order = Order.objects.get(id=id)
    b = OrderProduct.objects.filter(order=order)
    order.delete()
    b.delete()
    messages.info(request, 'Deleted SuccessFull')
    return redirect('completed_order')

def completed_order_list_edit(request, id):
    order = OrderProduct.objects.get(id=id)
    if request.method == 'POST':
        edit_productorder = EditOrderProductForm(request.POST, instance=order)
        if edit_productorder.is_valid():
            edit_productorder.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('completed_order')
        else:
            messages.info(request, 'Error Retry')
            return redirect(reverse('completed_order_list_edit', kwargs={'id': id}))
    else:
        edit_productorder = EditOrderProductForm(instance=order)

    context = {
        'edit_productorder': edit_productorder
    }
    return render(request, 'completed_order_list_edit.html', context)

def completed_order_list_delete(request, id):
    order_product = OrderProduct.objects.get(id=id)
    order_product.delete()
    messages.info(request, 'Deleted SuccessFull')
    return redirect('completed_order')