from django.urls import path
from shop import views

urlpatterns = [
    path('', views.shop_login, name='shop_login'),
    path('shop_dashboard/', views.shop_dashboard, name='shop_dashboard'),
    path('shop_view_order/', views.shop_view_order, name='shop_view_order'),
    path('shop_pending_order/', views.shop_pending_order, name='shop_pending_order'),
    path('shop_completed_order/', views.shop_completed_order, name='shop_completed_order'),
    path('shop_products/', views.shop_products, name='shop_products'),
    path('ct_shop_edit/', views.ct_shop_edit, name='ct_shop_edit'),
    path('shop_logout', views.shop_logout, name='shop_logout'),
    path('shop_order_list/<int:id>/', views.shop_order_list, name='shop_order_list'),
]