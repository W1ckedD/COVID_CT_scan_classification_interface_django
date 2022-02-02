import os
from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

from .models import Sample

from tensorflow.keras.models import load_model
from utils.preprocess import preprocess_img


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
    if not request.user.is_authenticated:
      messages.error(request, 'برای استفاده از این بخش ابتدا به حساب کاربری خود وارد شوید.')
      return redirect('accounts_login')
    name = request.POST.get('name')
    image = request.FILES.get('image')
    visible_to_users = request.POST.get('visible_to_users')
    visible_to_public = request.POST.get('visible_to_public')
    fs = FileSystemStorage()
    file = fs.save(image.name, image)
    img_url = fs.url(file)

    sample = Sample(account=request.user, name=name, image=img_url)
    if visible_to_public is not None:
      sample.visible_to_users = True
      sample.visible_to_public = True
    elif visible_to_users is not None:
      sample.visible_to_users = True
      sample.visible_to_public = False
    else:
      sample.visible_to_users = False
      sample.visible_to_public = False
    sample.save()
    return redirect('samples_my-samples')

class SampleDetailsView(View):
  def get(self, request, *args, **kwargs):
    sample = get_object_or_404(Sample, id=kwargs.get('id'))
    return render(request, 'samples/my-sample-details.html', context={'sample': sample})

  def post(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      messages.error(request, 'برای استفاده از این بخش ابتدا به حساب کاربری خود وارد شوید.')
      return redirect('accounts_login')
    visible_to_users = request.POST.get('visible_to_users')
    visible_to_public = request.POST.get('visible_to_public')
    sample_id = kwargs.get('id')
    sample = get_object_or_404(Sample, id=sample_id)
    if request.user != sample.account:
      messages.error(request, 'شما دسترسی لازم جهت انجام این عمل را ندارید.')
      return redirect('samples_my-sample-details', sample_id)


    if visible_to_public is not None:
      sample.visible_to_users = True
      sample.visible_to_public = True
    elif visible_to_users is not None:
      sample.visible_to_users = True
      sample.visible_to_public = False
    else:
      sample.visible_to_users = False
      sample.visible_to_public = False
    sample.save()
    messages.success(request, 'تغییرات با موفقیت ثبت شد.')
    return redirect('samples_my-sample-details', sample_id)

class PredictSampleView(View):
  def post(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      messages.error(request, 'برای استفاده از این بخش ابتدا به حساب کاربری خود وارد شوید.')
      return redirect('accounts_login')
    MODEL_DIR = os.path.join(os.getcwd(), 'models', '002.h5')
    cnn_model = load_model(MODEL_DIR)
    sample_id = request.POST.get('sample_id')
    sample = get_object_or_404(Sample, id=sample_id)
    if request.user != sample.account:
      messages.error(request, 'شما دسترسی لازم جهت انجام این عمل را ندارید.')
      return redirect('samples_my-sample-details', sample_id)
    IMG_DIR = os.path.join(os.getcwd(), 'media', str(sample.image).split('/')[2])
    img = preprocess_img(IMG_DIR)
    predicted = cnn_model.predict(img)[0]

    if predicted[0] > predicted[1]:
      probability = predicted[0]
      result = 'NEG'
    else:
      probability = predicted[1]
      result = 'POS'
    sample.result = result
    sample.probability = probability * 100
    sample.predicted_at = timezone.now()
    sample.save()
    return redirect('samples_my-sample-details', sample_id)

class DeleteSampleView(View):
  def post(self, request, *args, **kwargs):
    if not request.user.is_authenticated:
      messages.error(request, 'برای استفاده از این بخش ابتدا به حساب کاربری خود وارد شوید.')
      return redirect('accounts_login')
    sample_id = request.POST.get('sample_id')
    sample = get_object_or_404(Sample, id=sample_id)
    if request.user != sample.account:
      messages.error(request, 'شما دسترسی لازم جهت انجام این عمل را ندارید.')
      return redirect('samples_my-sample-details', sample_id)
    IMG_DIR = os.path.join(os.getcwd(), 'media', str(sample.image).split('/')[2])
    fs = FileSystemStorage()
    fs.delete(IMG_DIR)
    sample.delete()
    return redirect('samples_my-samples')