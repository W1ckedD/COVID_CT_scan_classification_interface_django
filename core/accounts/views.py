from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.views import View
from utils.decorators import (
  login_required,
  is_authenticated,
  login_validation,
  register_validation
)

class LoginView(View):
  @is_authenticated
  def get(self, request, *args, **kwargs):
    return render(request, 'accounts/login.html', context={})

  @login_validation
  def post(self, request, *args, **kwargs):
    email_or_username = request.POST.get('email_or_username')
    password = request.POST.get('password')
    
    email = email_or_username.lower().strip() if '@' in email_or_username else None
    username = email_or_username.lower().strip() if '@' not in email_or_username else None

    if email:
      user = User.objects.get(email=email)
      if user is None:
        messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
        return redirect('accounts_login')
      if not user.check_password(password):
        messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
        return redirect('accounts_login')
      
      auth.login(request, user)
      messages.success(request, 'خوش آمدید.')
      return redirect('accounts_dashboard')
      
    elif username:
      user = auth.authenticate(username=username, password=password)
      if user is None:
        messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
        return redirect('login')
      auth.login(request, user)
      messages.success(request, 'خوش آمدید.')
      return redirect('accounts_dashboard')


class RegisterView(View):
  @is_authenticated
  def get(self, request, *args, **kwargs):
    return render(request, 'accounts/register.html', context={})

  @register_validation
  def post(self, request, *args, **kwargs):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = User.objects.create_user(
      username=username.lower().strip(),
      first_name=first_name.lower().strip(),
      last_name=last_name.lower().strip(),
      email=email.lower().strip(),
      password=password
    )

    auth.login(request, user)
    user.save()
    messages.success(request, 'حساب جدید با موفقیت ایجاد شد.')
    return redirect('accounts_dashboard')

class LogoutView(View):
  @login_required('accounts_login')
  def post(self, request, *args, **kwargs):
    auth.logout(request)
    return redirect('accounts_login')


class DashboardView(View):

  @login_required('accounts_login')
  def get(self, request, *args, **kwargs):
    return render(request, 'accounts/dashboard.html', context={})
   