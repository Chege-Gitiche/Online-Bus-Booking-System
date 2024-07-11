from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns= [
    path('',views.home,name='home'),
    path('home',views.index,name='index'),
    path('admin_template/', views.admin, name='admin_template'),
    path('user_stats/', views.user_stats, name='user_stats'),
    path('settings', views.settings, name='settings'),

    path('users', views.users, name='users'),
    path('add_user/', views.add_user, name='add_user'),
    path('edit_user/<int:pk>/', views.edit_user, name='edit_user'),
    path('delete_user/<int:pk>/', views.delete_user, name='delete_user'),

    
    path('buses', views.buses, name='buses'),
    path('add_bus/', views.add_bus, name='add_bus'),
    path('edit_bus/<int:pk>/', views.edit_bus, name='edit_bus'),
    path('delete_bus/<int:pk>/', views.delete_bus, name='delete_bus'),

    path('schedule/', views.schedules, name='schedule'),
    path('add_schedule/', views.add_schedule, name='add_schedule'),
    path('edit_schedule/<int:schedule_id>/', views.edit_schedule, name='edit_schedule'),
    path('delete_schedule/<int:schedule_id>/', views.delete_schedule, name='delete_schedule'),

    path('routes_admin', views.routes_admin, name='routes_admin'),
    path('routes_admin/add/', views.add_route, name='add_route'),
    path('routes_admin/edit/<str:route_id>/', views.edit_route, name='edit_route'),
    path('routes_admin/delete/<str:route_id>/', views.delete_route, name='delete_route'),


    path('gender/', views.gender, name='gender'),
    path('search/', views.search_results, name='search_results'),
    

    path('sign_up',views.signUp,name='sign_up'),
    path("verify-email/<slug:username>", views.verifyEmail, name="verify-email"),
    path("resend-otp", views.resendOtp, name="resend-otp"),
    path('login_user', views.login_user, name="login"),

    path('routes/', views.routes_view, name='routes'),
    path('search_view/', views.search_view, name='search_view'),

    path('seat-selection/<int:bus_id>/', views.seat_selection_view, name='seat_selection'),
    path('booking_details/<str:selected_seats>/', views.booking_details, name='booking_details'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('logout_user', views.logout_user, name='logout'),
    path('lockscreen', views.lockscreen, name='lockscreen'),

    path('booking', views.booking, name='booking'),


    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
]