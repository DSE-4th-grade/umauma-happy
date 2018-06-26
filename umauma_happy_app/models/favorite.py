from django.db import models
from umauma_happy_app.models.user import User

class Favorite(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  factor_id_array = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.name + ':' + self.factor_id_array

  class Meta:
    app_label = 'umauma_happy_app'