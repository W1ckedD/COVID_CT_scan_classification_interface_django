from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.LoginView.as_view(), name='accounts_login'),
  path('register/', views.RegisterView.as_view(), name='accounts_register'),
  path('logout/', views.LogoutView.as_view(), name='accounts_logout'),
  path('dashboard/', views.DashboardView.as_view(), name='accounts_dashboard'),
  path('edit-account/', views.EditAccountView.as_view(), name='accounts_edit-account'),
  path('change-password/', views.ChangePasswordView.as_view(), name='accounts_change-password'),
  path('delete-account/', views.DeleteAccountView.as_view(), name='accounts_delete-account'),
]