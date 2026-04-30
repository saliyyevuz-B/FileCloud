from django.urls import path
from django.contrib.auth import views as auth_views
from storage_app import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'), #login
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),# logout
    path('register/', views.RegisterView.as_view(), name='register'), # registeratsiya  otish uchun
]