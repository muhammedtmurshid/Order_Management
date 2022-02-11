from django.urls import path

from staff import views

urlpatterns = [
    path('', views.staff_login, name='staff_login'),
    path('staff_dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff_products/', views.staff_products, name='staff_products'),
    path('staff_category/', views.staff_category, name='staff_category'),
    path('staff_shop/', views.staff_shop, name='staff_shop'),
    path('staff_add_order/', views.staff_add_order, name='staff_add_order'),
    path('staff_view_order/', views.staff_view_order, name='staff_view_order'),
    path('staff_pending_order/', views.staff_pending_order, name='staff_pending_order'),
    path('staff_completed_order', views.staff_completed_order, name='staff_completed_order'),
    path('staff_logout/', views.staff_logout, name='staff_logout'),
    path('staff_edit_order/<int:id>/', views.staff_edit_order, name='staff_edit_order'),
    path('staff_delete_order/<int:id>/', views.staff_delete_order, name='staff_delete_order'),
    path('st_edit_staff/', views.st_edit_staff, name='st_edit_staff'),
    path('st_view_order_list/<int:id>/', views.st_view_order_list, name='st_view_order_list'),
    path('staff_order_list_edit/<int:id>/', views.staff_order_list_edit, name='staff_order_list_edit'),
    path('staff_order_list_delete/<int:id>/', views.staff_order_list_delete, name='staff_order_list_delete'),
]