from django.shortcuts import render
from django.views import View

from .models import Sample

class SamplesView(View):
  def get(self, request, *args, **kwargs):
    if request.user.is_authenticated:
      samples = Sample.objects.filter(visible_to_users=True)
      return render(request, 'samples/samples.html', context={'samples': samples})
    else:
      samples = Sample.objects.filter(visible_to_public=True)
      return render(request, 'samples/samples.html', context={'samples': samples})
      

