from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from .models import Sample

class SamplesView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      samples = Sample.objects.filter(visible_to_users=True).order_by('-issued_at')
      return render(request, 'samples/samples.html', context={'samples': samples})
    else:
      samples = Sample.objects.filter(visible_to_public=True).order_by('-issued_at')
      return render(request, 'samples/samples.html', context={'samples': samples})

class MySamplesView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      samples = Sample.objects.filter(account=request.user).order_by('-issued_at')
      return render(request, 'samples/samples.html', context={'samples': samples})
    else:
      messages.error(request, 'برای استفاده از این بخش ابتدا به حساب کاربری خود وارد شوید.')
      return redirect('accounts_login')


class AddSampleView(View):
  def get(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      messages.error(request, 'برای استفاده از این بخش ابتدا به حساب کاربری خود وارد شوید.')
      return redirect('accounts_login')

    return render(request, 'samples/add-sample.html', context={})

  def post(self, request, *args, **kwargs):
    name = request.POST.get('name')
    image = request.FILES.get('image')
    visible_to_users = request.POST.get('visible_to_users')
    visible_to_public = request.POST.get('visible_to_public')
    fs = FileSystemStorage()
    file = fs.save(image.name, image)
    img_url = fs.url(file)

    sample = Sample(account=request.user, name=name, image=img_url)
    if visible_to_users is None:
      sample.visible_to_users = False
      sample.visible_to_public = False
    elif visible_to_public is None:
      sample.visible_to_users = True
      sample.visible_to_public = False
    else:
      sample.visible_to_public = True
      sample.visible_to_public = True
    sample.save()
    return redirect('samples_my-samples')
