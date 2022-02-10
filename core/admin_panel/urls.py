from django.urls import path
from . import views

urlpatterns = [
  path('login/', views.AdminLoginView.as_view(), name='admin_panel_login'),
  path('dashboard/', views.AdminDashboardView.as_view(), name='admin_panel_dashboard'),
  path('block-user/', views.AdminBlockUserView.as_view(), name='admin_panel_block-user'),
  path('unblock-user/', views.AdminUnBlockUserView.as_view(), name='admin_panel_unblock-user'),
  path('delete-user/', views.AdminDeleteUser.as_view(), name='admin_panel_delete-user'),
  path('users/', views.AdminManageUsersView.as_view(), name='admin_panel_users'),
  path('logs/', views.LogView.as_view(), name='admin_panel_logs'),
]