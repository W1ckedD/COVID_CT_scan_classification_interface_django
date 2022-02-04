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

def add_sample_validation(view_function):
  def wrapper(_, request, *args, **kwargs):
    name = request.POST.get('name')
    image = request.FILES.get('image')

    if not name or name is None:
      messages.error(request, 'لطفا عنوان نمونه را وارد کنید.')
      return redirect('samples_add-sample')

    if image is None:
      messages.error(request, 'لطفا تصویر نمونه را جهت بارگذاری انتخاب کنید.')
      return redirect('samples_add-sample')

    return view_function(_, request, *args, **kwargs)
  return wrapper

def edit_account_validation(view_function):
  def wrapper(_, request, *args, **kwargs):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')

    if (
      not first_name 
      or not last_name
      or not email
    ):
      messages.error(request, 'لطفا تمامی فیلد ها را پر کنید.')
      return redirect('accounts_register')

    return view_function(_, request, *args, **kwargs)
  return wrapper

def change_password_validation(view_function):
  def wrapper(_, request, *args, **kwargs):
    old_password = request.POST.get('old_password')
    new_password = request.POST.get('new_password')
    new_password_2 = request.POST.get('new_password_2')

    if (
      not old_password
      or not new_password
      or not new_password_2
    ):
      messages.error(request, 'لطفا تمامی فیلد ها را پر کنید.')
      return redirect('accounts_register')
    
    if new_password != new_password_2:
      messages.error(request, 'رمز عبور با تکرار آن همخوانی ندارد.')
      return redirect('accounts_register')
    
    if new_password == old_password:
      messages.error(request, 'رمز عبور فعلی و رمز عبور جدید نمی توانند یکسان باشند.')
      return redirect('accounts_register')


    return view_function(_, request, *args, **kwargs)
  return wrapper

def admin_required(login_path_name):
  def decorator(view_function):
    def wrapper(_, request, *args, **kwargs):
      if request.user.is_authenticated and request.user.is_staff:
        return view_function(_, request, *args, **kwargs)
      else:
        messages.error(request, 'تنها مدیران به این قسمت دسترسی دارند.')
        return redirect(login_path_name)
    return wrapper
  return decorator