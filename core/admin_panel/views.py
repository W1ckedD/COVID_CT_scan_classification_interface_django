from datetime import datetime, timedelta
from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.db.models import Q
from .models import Log
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

class LogView(View):
  @admin_required('admin_panel_login')
  def get(self, request, *args, **kwargs):
    logs = Log.objects.all()

    log_username = request.GET.get('log_username')
    success = request.GET.get('success')
    failure = request.GET.get('failure')
    AUTH = request.GET.get('AUTH')
    READ = request.GET.get('READ')
    CREATE = request.GET.get('CREATE')
    UPDATE = request.GET.get('UPDATE')
    DELETE = request.GET.get('DELETE')
    PREDICT = request.GET.get('PREDICT')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if log_username:
      logs = logs.filter(account__username__icontains=log_username)
    
    success_query = Q(success=True) if success else Q()
    failure_query = Q(success=False) if failure else Q()
    AUTH_query = Q(action_type='AUTH') if AUTH else Q()
    READ_query = Q(action_type='READ') if READ else Q()
    CREATE_query = Q(action_type='CREATE') if CREATE else Q()
    UPDATE_query = Q(action_type='UPDATE') if UPDATE else Q()
    DELETE_query = Q(action_type='DELETE') if DELETE else Q()
    PREDICT_query = Q(action_type='PREDICT') if PREDICT else Q()

    logs = logs.filter(
      success_query |
      failure_query |
      AUTH_query |
      READ_query |
      CREATE_query |
      UPDATE_query |
      DELETE_query |
      PREDICT_query 
    )
    if start_date and end_date:
      logs = logs.filter(created_at__range=[start_date, end_date])
    elif start_date:
      logs = logs.filter(created_at__range=[start_date, (datetime.today() + timedelta(1)).strftime('%Y-%m-%d')])
    
    logs = logs.order_by('-created_at')

    return render(request, 'admin_panel/logs.html', context={'logs': logs})
