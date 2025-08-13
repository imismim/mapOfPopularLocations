from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("account/", views.AccountView.as_view(), name="account"),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(),
         name='reset_password'),
    
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    
    path('password_reset_complete', auth_views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]