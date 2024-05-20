from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns= [
    path('',views.index,name='index'),
    path('home',views.index,name='index'),
    path('sign_up',views.sign_up,name='sign_up'),
    path("verify-email/<slug:username>", views.verify_email, name="verify-email"),
    path("resend-otp", views.resend_otp, name="resend-otp"),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]