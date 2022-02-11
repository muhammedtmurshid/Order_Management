from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
from product.models import Order, Product, OrderProduct
from shop.forms import UserShopUpdate, ShopUpdate


def shop_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_shop:
            login(request, user)
            messages.info(request, 'Login Success Fully')
            return redirect('shop_dashboard')
        else:
            messages.error(request, 'Error')
            return redirect('shop_login')
    return render(request, 'shop_login.html')


@login_required(login_url='shop_login')
def shop_dashboard(request):
    product = Product.objects.all()
    product_count = product.count()
    total_order = Order.objects.filter(shop=request.user.shop)
    shop_order_count = total_order.count()
    shop_pending_orders = Order.objects.filter(shop=request.user.shop, status='Pending')
    shop_pending_orders_count = shop_pending_orders.count()
    shop_completed_orders = Order.objects.filter(shop=request.user.shop, status='Completed')
    shop_completed_orders_count = shop_completed_orders.count()
    context = {
        'product_count':product_count,
        'shop_order_count':shop_order_count,
        'shop_pending_orders_count':shop_pending_orders_count,
        'shop_completed_orders_count':shop_completed_orders_count
    }
    return render(request, 'shop_dashboard.html', context)


@login_required(login_url='shop_login')
def shop_view_order(request):
    order = Order.objects.filter(shop=request.user.shop)
    return render(request, 'shop_view_order.html', {'order':order})


@login_required(login_url='shop_login')
def shop_pending_order(request):
    shop_order = Order.objects.filter(shop=request.user.shop)
    order = Order.objects.filter(status='Pending')
    return render(request, 'shop_pending_order.html', {'shop_order':shop_order, 'order':order})

@login_required(login_url='shop_login')
def shop_completed_order(request):
    shop_order = Order.objects.filter(shop=request.user.shop)
    order = Order.objects.filter(status='Completed')
    return render(request, 'shop_completed_order.html', {'shop_order':shop_order, 'order':order})

@login_required(login_url='shop_login')
def shop_products(request):
    products = Product.objects.all()
    return render(request, 'shop_products.html', {'products':products})

@login_required(login_url='ct_shop_edit')
def ct_shop_edit(request):
    if request.method == 'POST':
        ct_shop_edit = UserShopUpdate(request.POST, instance=request.user)
        ct_shop_update = ShopUpdate(request.POST, instance=request.user.shop)
        if ct_shop_edit.is_valid() and ct_shop_update.is_valid():
            ct_shop_edit.save()
            ct_shop_update.save()
            messages.info(request, 'Edit Success Fully')
            return redirect('ct_shop_edit')
        else:
            messages.error(request, 'Error Please Try Again')
            return redirect('ct_shop_edit')
    else:
        ct_shop_edit = UserShopUpdate(instance=request.user)
        ct_shop_update = ShopUpdate(instance=request.user.shop)

    context = {
        'ct_shop_edit':ct_shop_edit,
        'ct_shop_update':ct_shop_update,
    }
    return render(request, 'ct_shop_edit.html', context)

def shop_logout(request):
    auth.logout(request)
    messages.info(request, 'Logout Success Full')
    return redirect('shop_login')

def shop_order_list(request, id):
    order = Order.objects.get(id=id)
    orderproduct = OrderProduct.objects.filter(order_id=order)
    return render(request, 'shop_order_list.html', {'orderproduct':orderproduct})
