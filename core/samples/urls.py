from django.urls import path
from . import views

urlpatterns = [
  path('', views.SamplesView.as_view(), name='samples')
]