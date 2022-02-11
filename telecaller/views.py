from django.contrib import auth, messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


# Create your views here.
from product.models import Order, OrderProduct
from telecaller.forms import UpdateUserTeleForm, UpdateTeleForm


def telecaller_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_telecaller:
            login(request, user)
            messages.info(request, 'Login Success Fully')
            return redirect('tele_dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('telecaller_login')
    return render(request, 'tele_login.html')


@login_required(login_url='tele_login')
def tele_dashboard(request):
    pending_orders = Order.objects.all()
    tele_pending_orders = pending_orders.count()
    return render(request, 'tele_dashboard.html', {'tele_pending_orders':tele_pending_orders})

@login_required(login_url='tele_login')
def tele_pending_order(request):
    order = Order.objects.filter(status='Pending')

    context ={
        'order' : order,
    }
    return render(request, 'tele_pending_order.html', context)

@login_required(login_url='tele_login')
def tele_logout(request):
    auth.logout(request)
    messages.info(request, 'Logout Success Fully')
    return redirect('telecaller_login')

@login_required(login_url='tele_login')
def tele_edit_ad(request):
    if request.method == 'POST':
        tele_edit_ad = UpdateUserTeleForm(request.POST, instance=request.user)
        tele_edit_up = UpdateTeleForm(request.POST, instance=request.user.telecaller)
        if tele_edit_ad.is_valid() and tele_edit_up.is_valid():
            tele_edit_ad.save()
            tele_edit_up.save()
            messages.info(request, 'Edit Success Fully')
        else:
            messages.error(request, 'Error Please Try Again')
            return redirect('tele_edit_ad')
    else:
        tele_edit_ad = UpdateUserTeleForm(instance=request.user)
        tele_edit_up = UpdateTeleForm(instance=request.user.telecaller)

    context = {
        'tele_edit_ad':tele_edit_ad,
        'tele_edit_up':tele_edit_up,
    }
    return render(request, 'tele_edit_ad.html', context)

def tele_order_list(request, id):
    order = Order.objects.get(id=id)
    orderproduct = OrderProduct.objects.filter(order_id=order)
    return render(request, 'tele_order_list.html', {'orderproduct':orderproduct})