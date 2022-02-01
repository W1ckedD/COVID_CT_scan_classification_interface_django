from django.urls import path
from . import views

urlpatterns = [
  path('', views.SamplesView.as_view(), name='samples'),
  path('my-samples/', views.MySamplesView.as_view(), name='samples_my-samples'),
  path('add-sample/', views.AddSampleView.as_view(), name='samples_add-sample')
]