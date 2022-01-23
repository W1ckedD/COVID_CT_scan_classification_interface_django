from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages, auth
from django.views import View

class LoginView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'accounts/login.html', context={})

  def post(self, request, *args, **kwargs):
    email_or_username = request.POST.get('email_or_username')
    password = request.POST.get('password')
    email = email_or_username if '@' in email_or_username else None
    username = email_or_username if '@' not in email_or_username else None

    if not email_or_username or not password: 
      messages.error(request, 'لطفا تمامی فیلد ها را پر کنید.')
      return redirect('login')

    if email:
      user = User.objects.get(email=email)
      if user is None:
        messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
        return redirect('login')
      if not user.check_password(password):
        messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
        return redirect('login')
      
      auth.login(request, user)
      messages.success(request, 'خوش آمدید.')
      return redirect('index')
      
    elif username:
      user = auth.authenticate(username=username, password=password)
      if user is None:
        messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
        return redirect('login')
      auth.login(request, user)
      messages.success(request, 'خوش آمدید.')
      return redirect('index')


class RegisterView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'accounts/register.html', context={})

  def post(self, request, *args, **kwargs):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')    
    username = request.POST.get('username')
    password = request.POST.get('password')
    password_2 = request.POST.get('password2')

    print(f'{first_name} {last_name} {email} {username} {password} {password_2}')

    if (
      not first_name 
      or not last_name 
      or not email 
      or not username 
      or not password 
      or not password_2
    ):
      messages.error(request, 'لطفا تمامی فیلد ها را پر کنید.')
      return redirect('register')
    
    if User.objects.filter(username=username).exists():
      messages.error(request, 'این نام کاربری از قبل در سیستم ثبت شده است.')
      return redirect('register')

    if User.objects.filter(email=email).exists(): 
      messages.error(request, 'این ایمیل برای کاربری دیگر در سیستم ثبت شده است.')
      return redirect('register')

    if password != password_2:
      messages.error(request, 'رمز عبور با تکرار آن همخوانی ندارد.')
      return redirect('register')

    if '@' in username:
      messages.error(request, 'نام کاربری نمی تواند شامل کاراکتر "@" باشد.')
      return redirect('register')


    user = User.objects.create_user(
      username=username,
      first_name=first_name,
      last_name=last_name,
      email=email,
      password=password
    )

    auth.login(request, user)
    user.save()
    messages.success(request, 'حساب جدید با موفقیت ایجاد شد.')
    return redirect('index')

class LogoutView(View):
  def post(self, request, *args, **kwargs):
    auth.logout(request)
    return redirect('accounts_login')