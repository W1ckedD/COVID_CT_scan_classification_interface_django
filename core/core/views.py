from django.shortcuts import render, redirect
from django.views import View

class IndexView(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'index.html', context={})
