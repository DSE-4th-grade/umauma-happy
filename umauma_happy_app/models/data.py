from django.db import models
from umauma_happy_app.models.horse import Horse
from umauma_happy_app.models.race import Race
from umauma_happy_app.models.jockey import Jockey
from umauma_happy_app.models.stable import Stable
from umauma_happy_app.models.trainer import Trainer
from umauma_happy_app.models.distance_suitability import DistanceSuitability
from umauma_happy_app.models.leg_quality import LegQuality

class Data(models.Model):
  horse = models.ForeignKey(Horse, on_delete=models.PROTECT)
  race = models.ForeignKey(Race, on_delete=models.PROTECT)
  jockey = models.ForeignKey(Jockey, on_delete=models.PROTECT)
  sex = models.IntegerField()
  handicap = models.IntegerField()
  stable = models.ForeignKey(Stable, on_delete=models.PROTECT)
  trainer = models.ForeignKey(Trainer, on_delete=models.PROTECT)
  distance_suitability = models.ForeignKey(DistanceSuitability, on_delete=models.PROTECT)
  horse_order = models.IntegerField()
  leg_quality = models.ForeignKey(LegQuality, on_delete=models.PROTECT)
  odds = models.DecimalField(decimal_places=1, max_digits=5)
  popularity = models.IntegerField()
  rank = models.IntegerField(null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.horse.name + str(self.race.departure_time)

  class Meta:
    app_label = 'umauma_happy_app'