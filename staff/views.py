from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse

from product.forms import OrderFormset, EditOrderProductForm
from product.models import Product, Category, Order, OrderProduct
from shop.models import Shop
from staff.forms import StaffOrderForm, Staff_Edit_Order, UserUpdateForm, StaffUpdateForm


def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_distributor:
            login(request, user)
            messages.info(request, 'Login Success Fully')
            return redirect('staff_dashboard')
        else:
            messages.error(request, 'Error Retry')
            return redirect('staff_login')
    return render(request, 'staff_login.html')


@login_required(login_url='staff_login')
def staff_dashboard(request):
    shops = Shop.objects.filter(staff=request.user.staff)
    shops_count = shops.count()
    orders = Order.objects.filter(staff=request.user.staff)
    order_count = orders.count()
    pending_orders = Order.objects.filter(staff=request.user.staff, status='Pending')
    pending_orders_count = pending_orders.count()
    completed_orders = Order.objects.filter(staff=request.user.staff, status='Completed')
    completed_orders_count = completed_orders.count()
    products = Product.objects.all()
    products_count = products.count()

    context = {
        'shops_count':shops_count,
        'order_count':order_count,
        'pending_orders_count':pending_orders_count,
        'completed_orders_count':completed_orders_count,
        'products_count':products_count,
    }
    return render(request, 'staff_dashboard.html', context)


@login_required(login_url='staff_login')
def staff_products(request):
    products = Product.objects.filter(status='Approved')
    return render(request, 'staff_products.html', {'products':products})


@login_required(login_url='staff_login')
def staff_category(request):
    category = Category.objects.all()
    return render(request, 'staff_category.html', {'category':category})

@login_required(login_url='staff_login')
def staff_shop(request):
    shops = Shop.objects.filter(staff=request.user.staff)
    return render(request, 'staff_shop.html', {'shops':shops})

@login_required(login_url='staff_login')
def staff_add_order(request):
    if request.method == 'GET':
        staff_order_form = StaffOrderForm(request.GET or None)
        formset = OrderFormset(queryset=OrderProduct.objects.none())
    if request.method == 'POST':
        staff_order_form = StaffOrderForm(request.user.staff, request.POST)
        formset = OrderFormset(request.POST)
        if staff_order_form.is_valid() and formset.is_valid():
            order = staff_order_form.save()
            staff_order_form = staff_order_form.save(commit=False)
            staff_order_form.staff = request.user.staff
            staff_order_form.save()
            for form in formset:
                # so that `book` instance can be attached.
                orderproduct = form.save(commit=False)
                orderproduct.order = order
                orderproduct.save()
            messages.info(request, 'Adding Success Fully')
            return redirect('staff_add_order')
        else:
            messages.error(request, 'Error Retry')
            return redirect('staff_add_order')
    else:
        staff_order_form = StaffOrderForm(request.user.staff)

    context = {
        'staff_order_form' : staff_order_form,
        'formset': formset,

    }
    return render(request, 'staff_add_order.html', context)

@login_required(login_url='staff_login')
def staff_view_order(request):
    order = Order.objects.filter(staff=request.user.staff)
    return render(request, 'staff_view_order.html', {'order':order})


@login_required(login_url='staff_login')
def staff_pending_order(request):
    staff_order = Order.objects.filter(staff=request.user.staff)
    pending = Order.objects.filter(status='Pending')
    return render(request, 'staff_pending_order.html', {'staff_order':staff_order, 'pending':pending})

@login_required(login_url='staff_login')
def staff_completed_order(request):
    staff_order = Order.objects.filter(staff=request.user.staff)
    order = Order.objects.filter(status='Completed')
    return render(request, 'staff_completed_order.html', {'staff_order':staff_order, 'order':order})

@login_required(login_url='staff_login')
def staff_edit_order(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        update_order = Staff_Edit_Order(request.user.staff, request.POST, instance=order)
        if update_order.is_valid():
            update_order.save()
            messages.info(request, 'Editing Success Fully')
            return redirect('staff_view_order')
        else:
            messages.error(request, 'Error Retry')
            return redirect(reverse('staff_edit_order', kwargs={'id':id}))
    else:
        update_order = Staff_Edit_Order(request.user.staff, instance=order)

    context = {
        'update_order':update_order,
    }
    return render(request, 'staff_edit_order.html', context)


@login_required(login_url='staff_login')
def staff_delete_order(request, id):
    order = Order.objects.get(id=id)
    order.delete()
    messages.info(request, 'Deleted Success Fully')
    return redirect('staff_view_order')

@login_required(login_url='staff_login')
def staff_logout(request):
    auth.logout(request)
    messages.info(request, 'Logout Success Full')
    return redirect('staff_login')

@login_required(login_url='staff_login')
def st_edit_staff(request):
    if request.method == 'POST':
        st_staff_edit = UserUpdateForm(request.POST, instance=request.user)
        st_staff = StaffUpdateForm(request.POST, instance=request.user)
        if st_staff_edit.is_valid() and st_staff.is_valid():
            st_staff_edit.save()
            st_staff.save()
            messages.info(request, 'Edit Success Fully')
            return redirect('st_edit_staff')
        else:
            messages.error(request, 'Error Please Try Again')
    else:
        st_staff_edit = UserUpdateForm(instance=request.user)
        st_staff = StaffUpdateForm(instance=request.user.staff)

    context = {
        'st_staff_edit':st_staff_edit,
        'st_staff':st_staff,
    }
    return render(request, 'st_edit_staff.html', context)


def st_view_order_list(request, id):
    order = Order.objects.get(id=id)
    orderproduct = OrderProduct.objects.filter(order_id=order)
    return render(request, 'st_view_order_list.html', {'orderproduct':orderproduct})


def staff_order_list_edit(request, id):
    order_product = OrderProduct.objects.get(id=id)
    if request.method == 'POST':
        edit_productorder = EditOrderProductForm(request.POST, instance=order_product)
        if edit_productorder.is_valid():
            edit_productorder.save()
            messages.info(request, 'Editing SuccessFull')
            return redirect('staff_view_order')
        else:
            messages.info(request, 'Error Retry')
            return redirect(reverse('staff_order_list_edit', kwargs={'id':id}))
    else:
        edit_productorder = EditOrderProductForm(instance=order_product)

    context = {
        'edit_productorder' : edit_productorder
    }
    return render(request, 'staff_order_list_edit.html', context)

def staff_order_list_delete(request, id):
    order_product = OrderProduct.objects.get(id=id)
    order_product.delete()
    messages.info(request, 'Deleted SuccessFull')
    return redirect('staff_view_order')