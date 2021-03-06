from django.urls import path
from . import views

urlpatterns = [
  path('', views.SamplesView.as_view(), name='samples'),
  path('my-samples/', views.MySamplesView.as_view(), name='samples_my-samples'),
  path('my-samples/<int:id>', views.SampleDetailsView.as_view(), name='samples_my-sample-details'),
  path('add-sample/', views.AddSampleView.as_view(), name='samples_add-sample'),
  path('edit-sample/', views.EditSampleNameView.as_view(), name='samples_edit-sample'),
  path('delete-sample/', views.DeleteSampleView.as_view(), name='samples_delete-sample'),
  path('predict/', views.PredictSampleView.as_view(), name='samples_predict-sample'),
]