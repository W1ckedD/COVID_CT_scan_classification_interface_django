from django.db import models
from django.contrib.auth.models import User

class Sample(models.Model):
  account = models.ForeignKey(User, related_name='samples', on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  image = models.ImageField(upload_to='photos/%Y/%m/%d/')
  result = models.CharField(
    max_length=50,
    choices=[
      ('POS', 'مبتلا به گوید 19'),
      ('NEG', 'عدم ابتلا به کوید 19'),
      ('TBD', 'نا مشخص')
    ],
    default='TBD'
  )
  probability = models.FloatField(blank=True)
  visible_to_public = models.BooleanField(default=True)
  visible_to_users = models.BooleanField(default=True)
  issued_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f'{self.account}, {self.name}'