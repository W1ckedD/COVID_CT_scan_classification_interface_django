from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages

from .models import Sample

class SamplesView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      samples = Sample.objects.filter(visible_to_users=True)
      return render(request, 'samples/samples.html', context={'samples': samples})
    else:
      samples = Sample.objects.filter(visible_to_public=True)
      return render(request, 'samples/samples.html', context={'samples': samples})


class AddSampleView(View):
  def get(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      messages.error(request, 'برای استفاده از این بخش ابتدا به حساب کاربری خود وارد شوید.')
      return redirect('accounts_login')

    return render(request, 'samples/add-sample.html', context={})

