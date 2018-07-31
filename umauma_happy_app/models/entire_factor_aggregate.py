from django.db import models
from umauma_happy_app.models.factor import Factor
from umauma_happy_app.models.race import Race

class EntireFactorAggregate(models.Model):
  factor = models.ForeignKey(Factor, on_delete=models.PROTECT)
  use = models.IntegerField()
  hit = models.IntegerField()
  percentage = models.DecimalField(decimal_places=5, max_digits=8, null=True)
  race = models.ForeignKey(Race, on_delete=models.PROTECT, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return str(self.factor.name)

  class Meta:
    app_label = 'umauma_happy_app'