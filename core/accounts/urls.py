from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.LoginView.as_view(), name='accounts_login'),
  path('register/', views.RegisterView.as_view(), name='accounts_register'),
  path('logout/', views.LogoutView.as_view(), name='accounts_logout')
]