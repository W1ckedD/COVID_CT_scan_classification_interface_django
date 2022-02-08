import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.views import View
from samples.models import Sample
from admin_panel.models import Log
from utils.decorators import (
  login_required,
  is_authenticated,
  login_validation,
  register_validation,
  edit_account_validation,
  change_password_validation
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
      user = User.objects.filter(email=email)
      if not user.exists():
        messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
        return redirect('accounts_login')
      user = User.objects.get(email=email)
      if not user.check_password(password):
        messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
        return redirect('accounts_login')
      
      auth.login(request, user)
      messages.success(request, 'خوش آمدید.')

      # Log
      log = Log.objects.create(
        account=request.user,
        action_type='AUTH',
        msg='کاربر با ایمیل به حساب کاربری خود وارد شد.'
      )

      return redirect('accounts_dashboard')
      
    elif username:
      user = auth.authenticate(username=username, password=password)
      if user is None:
        messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
        return redirect('accounts_login')
      auth.login(request, user)
      messages.success(request, 'خوش آمدید.')
      
      # Log
      log = Log.objects.create(
        account=request.user,
        action_type='AUTH',
        msg='کاربر با نام کاربری به حساب کاربری خود وارد شد.'
      )
      
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
    
    # Log
    log = Log.objects.create(
      account=user,
      action_type='AUTH',
      msg='کاربر حساب کاربری جدید ایجاد کرد.'
    )
    return redirect('accounts_dashboard')

class LogoutView(View):
  @login_required('accounts_login')
  def post(self, request, *args, **kwargs):
    auth.logout(request)

    # Log
    log = Log.objects.create(
      account=request.user,
      action_type='AUTH',
      msg='کاربر از حساب کاربری خود خارج شد.'
    )
    return redirect('accounts_login')


class DashboardView(View):
  @login_required('accounts_login')
  def get(self, request, *args, **kwargs):
    return render(request, 'accounts/dashboard.html', context={})

class EditAccountView(View):
  @login_required('accounts_login')
  @edit_account_validation
  def post(self, request, *args, **kwargs):

    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')    

    user = User.objects.get(username=request.user.username)
    user.first_name = first_name.lower().strip()
    user.last_name = last_name.lower().strip()
    if email.lower().strip() != user.email:
      if User.objects.filter(email=email.lower().strip()).exists():
        messages.error(request, 'این ایمیل قبلا در سیستم ثبت شده است.')
        return redirect('accounts_dashboard')
      else:
        user.email = email.lower().strip()

    user.save()
    messages.success(request, 'تغییرات با موفقیت ثبت شد.')
    # Log
    log = Log.objects.create(
      account=request.user,
      action_type='UPDATE',
      msg='کاربر تنظیمات حساب خود را بروز کرد.'
    )
    
    return redirect('accounts_dashboard')

class ChangePasswordView(View):
  @login_required('accounts_login')
  @change_password_validation
  def post(self, request, *args, **kwargs):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    user = User.objects.get(username=request.user.username)
    if user.check_password(old_password):
      user.set_password(new_password)
      user.save()
      auth.login(request, user)
      messages.success(request, 'رمز عبور با موفقیت تغغیر یافت.')
      
      # Log
      log = Log.objects.create(
        account=request.user,
        action_type='UPDATE',
        msg='تغییر موفق رمز عبور.'
      )
      
      return redirect('accounts_dashboard')
    else:
      messages.error(request, 'رمز عبور فعلی اشتباه است.')
      return redirect('accounts_dashboard')

class DeleteAccountView(View):
  @login_required('accounts_login')
  def post(self, request, *args, **kwargs):
    validation = request.POST.get('validation')
    if validation != f'{request.user.username}/{request.user.email}':
      messages.error(request, 'عبارت وارد شده نادرست است.')
      return redirect('accounts_dashboard')
    else:
      samples = Sample.objects.filter(account=request.user)
      for sample in samples:
        IMG_DIR = os.path.join(os.getcwd(), 'media', str(sample.image).split('/')[2])
        fs = FileSystemStorage()
        fs.delete(IMG_DIR)
        sample.delete()
      user = User.objects.get(username=request.user.username)
      auth.logout(request)
      user.delete()
      return redirect('index')

      
