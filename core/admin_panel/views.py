from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import auth, messages
from utils.decorators import (
  admin_required
)

class AdminLoginView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'admin_panel/login.html', context={})

  def post(self, request, *args, **kwargs):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_staff:
      auth.login(request, user)
      messages.success(request, f'{user} خوش آمدید.')

    return redirect('admin_panel_dashboard')

class AdminDashboardView(View):
  @admin_required('admin_panel_login')
  def get(self, request, *args, **kwargs):
    return render(request, 'admin_panel/dashboard.html', context={})