from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.AdminLoginView.as_view(), name='admin_panel_login'),
  path('dashboard/', views.AdminDashboardView.as_view(), name='admin_panel_dashboard'),
  path('logs/', views.LogView.as_view(), name='admin_panel_logs'),
]