from django.db import models
from umauma_happy_app.models.history import History
from umauma_happy_app.models.factor import Factor

class Weight(models.Model):
  history = models.ForeignKey(History, on_delete=models.PROTECT)
  factor = models.ForeignKey(Factor, on_delete=models.PROTECT)
  value = models.DecimalField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.value

  class Meta:
    app_label = 'umauma_happy_app'