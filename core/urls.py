from django.urls import path
from django.contrib.auth import views as auth_views

from core import views

urlpatterns = [
    path('', views.index, name='index'),

    path('password_reset/',
         auth_views.PasswordResetView.as_view(template_name="password/password_reset.html"), name='password_reset'),
    path('password_reset_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password/password_reset_sent.html"),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password/password_reset_confirm.html"),
         name='password_reset_confirm'),

    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password/password_reset_complete.html"),
         name='password_reset_complete'),
]