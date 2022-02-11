from django.urls import path

from telecaller import views

urlpatterns = [
    path('', views.telecaller_login, name='telecaller_login'),
    path('tele_dashboard/', views.tele_dashboard, name='tele_dashboard'),
    path('tele_pending_order/', views.tele_pending_order, name='tele_pending_order'),
    path('tele_logout/', views.tele_logout, name='tele_logout'),
    path('tele_edit_ad/', views.tele_edit_ad, name='tele_edit_ad'),
    path('tele_order_list/<int:id>/', views.tele_order_list, name='tele_order_list')
]