import os
from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.db.models import Q, functions, Value
from .models import Sample
from admin_panel.models import Log

from tensorflow.keras.models import load_model
from utils.preprocess import preprocess_img
from utils.decorators import login_required, add_sample_validation


class SamplesView(View):
  def get(self, request, *args, **kwargs):
    name = request.GET.get('name')
    username = request.GET.get('username')
    owner_name = request.GET.get('owner_name')
    pos = request.GET.get('pos')
    neg = request.GET.get('neg')
    tbd = request.GET.get('tbd')
    samples = Sample.objects.annotate(
      owner_name=functions.Concat('account__first_name', Value(' '), 'account__last_name')
    )
    if name:
      samples = samples.filter(name__contains=name)
    if username:
      samples = samples.filter(account__username__icontains=username)
    if owner_name:
      samples = samples.filter(owner_name__contains=owner_name)
    pos_query = Q(result='POS') if pos else Q()
    neg_query = Q(result='NEG') if neg else Q()
    tbd_query = Q(result='TBD') if tbd else Q()
    
    samples = samples.filter(pos_query |neg_query | tbd_query)

    if request.user.is_authenticated:
      samples = samples.filter(visible_to_users=True).order_by('-issued_at')
      
      #Log
      log = Log.objects.create(
        account=request.user,
        action_type='READ',
        msg='خواندن نمونه های قابل مشاهده.'
      )
      
      return render(request, 'samples/samples.html', context={'samples': samples})
    else:
      samples = samples.filter(visible_to_public=True).order_by('-issued_at')
      return render(request, 'samples/samples.html', context={'samples': samples})

class MySamplesView(View):
  @login_required('accounts_login')
  def get(self, request, *args, **kwargs):
    samples = Sample.objects.filter(account=request.user).order_by('-issued_at')
    
    #Log
    log = Log.objects.create(
      account=request.user,
      action_type='READ',
      msg='خواندن نمونه های مربوط به خود کاربر.'
    )
    
    return render(request, 'samples/samples.html', context={'samples': samples})


class AddSampleView(View):
  @login_required('accounts_login')
  def get(self, request, *args, **kwargs):
    return render(request, 'samples/add-sample.html', context={})

  @login_required('accounts_login')
  @add_sample_validation
  def post(self, request, *args, **kwargs):
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
    #Log
    log = Log.objects.create(
      account=request.user,
      action_type='CREATE',
      msg='افزودن نمونه جدید.'
    )
    return redirect('samples_my-samples')

class SampleDetailsView(View):
  def get(self, request, *args, **kwargs):
    sample = get_object_or_404(Sample, id=kwargs.get('id'))
    log = Log.objects.create(
      account=request.user,
      action_type='READ',
      msg=f'خواندن نمونه {sample}.'
    )
    return render(request, 'samples/my-sample-details.html', context={'sample': sample})

  @login_required('accounts_login')
  def post(self, request, *args, **kwargs):
    visible_to_users = request.POST.get('visible_to_users')
    visible_to_public = request.POST.get('visible_to_public')
    sample_id = kwargs.get('id')
    sample = get_object_or_404(Sample, id=sample_id)
    if request.user != sample.account:
      log = Log.objects.create(
        account=request.user,
        action_type='UPDATE',
        msg=f'تغییر ناموفق نمونه {sample} به دلیل عدم مالکیت.',
        success=False
      )
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
    log = Log.objects.create(
      account=request.user,
      action_type='UPDATE',
      msg=f'تغییر نمونه {sample}.'
    )
    messages.success(request, 'تغییرات با موفقیت ثبت شد.')
    return redirect('samples_my-sample-details', sample_id)

class PredictSampleView(View):
  @login_required('accounts_login')
  def post(self, request, *args, **kwargs):
    MODEL_DIR = os.path.join(os.getcwd(), 'models', '002.h5')
    cnn_model = load_model(MODEL_DIR)
    sample_id = request.POST.get('sample_id')
    sample = get_object_or_404(Sample, id=sample_id)
    if request.user != sample.account:
      log = Log.objects.create(
        account=request.user,
        action_type='PREDICT',
        msg=f'محاسبه ناموفق احتمال نمونه {sample} به دلیل عدم مالکیت.',
        success=False
      )
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
    log = Log.objects.create(
      account=request.user,
      action_type='PREDICT',
      msg=f'محاسبه احتمال نمونه {sample}.'
    )
    return redirect('samples_my-sample-details', sample_id)

class EditSampleNameView(View):
  @login_required('accounts_login')
  def post(self, request, *args, **kwargs):
    sample_id = request.POST.get('sample_id')
    sample = get_object_or_404(Sample, id=sample_id)
    if request.user != sample.account:
      log = Log.objects.create(
        account=request.user,
        action_type='UPDATE',
        msg=f'تغییر ناموفق نام نمونه {sample} به دلیل عدم مالکیت.',
        success=False
      )
      messages.error(request, 'شما دسترسی لازم جهت انجام این عمل را ندارید.')
      return redirect('samples_my-sample-details', sample_id)
    name = request.POST.get('name')
    if not name:
      messages.error(request, 'لطفا نام نمونه را وارد نمایید.')
      return redirect('samples_my-sample-details', sample_id)

    sample.name = name
    sample.save()
    log = Log.objects.create(
      account=request.user,
      action_type='UPDATE',
      msg=f'تغییر نام نمونه {sample}.'
    )
    messages.success(request, 'تغییرات با موفقیت ثبت شد.')
    return redirect('samples_my-sample-details', sample_id)


class DeleteSampleView(View):
  @login_required('accounts_login')
  def post(self, request, *args, **kwargs):
    sample_id = request.POST.get('sample_id')
    sample = get_object_or_404(Sample, id=sample_id)
    if request.user != sample.account:
      log = Log.objects.create(
        account=request.user,
        action_type='DELETE',
        msg=f'حذف ناموفق نمونه {sample} به دلیل عدم مالکیت.',
        success=False
      )
      messages.error(request, 'شما دسترسی لازم جهت انجام این عمل را ندارید.')
      return redirect('samples_my-sample-details', sample_id)
    IMG_DIR = os.path.join(os.getcwd(), 'media', str(sample.image).split('/')[2])
    fs = FileSystemStorage()
    fs.delete(IMG_DIR)
    log = Log.objects.create(
      account=request.user,
      action_type='DELETE',
      msg=f'حذف نمونه {sample}.'
    )
    sample.delete()
    return redirect('samples_my-samples')