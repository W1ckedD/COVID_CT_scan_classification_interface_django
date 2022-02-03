from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages

def login_required(login_path_name):
  def decorator(view_function):
    def wrapper(_, request, *args, **kwargs):
      if not request.user.is_authenticated:
        messages.error(request, 'برای مشاهده این قسمت، ابتدا به حساب کاربری خود وارد شوید.')
        return redirect(login_path_name)
      else:
        return view_function(_, request, *args, **kwargs)
    return wrapper
  return decorator

def is_authenticated(view_function):
  def wrapper(_, request, *args, **kwargs):
    if request.user.is_authenticated:
      return redirect('accounts_dashboard')
    else:
      return view_function(_, request, *args, **kwargs)
  return wrapper

def login_validation(view_function):
  def wrapper(_, request, *args, **kwargs):
    email_or_username = request.POST.get('email_or_username')
    password = request.POST.get('password')
    if not email_or_username or not password: 
      messages.error(request, 'لطفا تمامی فیلد ها را پر کنید.')
      return redirect('accounts_login')

    return view_function(_, request, *args, *kwargs)
  return wrapper

def register_validation(view_function):
  def wrapper(_, request, *args, **kwargs):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')    
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_2 = request.POST.get('password2')

    if (
      not first_name 
      or not last_name 
      or not email 
      or not username 
      or not password 
      or not password_2
    ):
      messages.error(request, 'لطفا تمامی فیلد ها را پر کنید.')
      return redirect('accounts_register')
    
    if User.objects.filter(username=username.lower().strip()).exists():
      messages.error(request, 'این نام کاربری از قبل در سیستم ثبت شده است.')
      return redirect('accounts_register')

    if User.objects.filter(email=email.lower().strip()).exists(): 
      messages.error(request, 'این ایمیل برای کاربری دیگر در سیستم ثبت شده است.')
      return redirect('accounts_register')

    if password != password_2:
      messages.error(request, 'رمز عبور با تکرار آن همخوانی ندارد.')
      return redirect('accounts_register')

    if '@' in username:
      messages.error(request, 'نام کاربری نمی تواند شامل کاراکتر "@" باشد.')
      return redirect('accounts_register')
    return view_function(_, request, *args, **kwargs)
  return wrapper