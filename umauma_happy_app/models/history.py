from django.db import models
from umauma_happy_app.models.user import User
from umauma_happy_app.models.data import Data

class History(models.Model):
  user = models.ForeignKey(User, on_delete=models.PROTECT)
  data = models.ForeignKey(Data, on_delete=models.PROTECT)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.user.name + ':' + str(self.created_at)

  class Meta:
    app_label = 'umauma_happy_app'