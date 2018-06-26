from django.db import models
from umauma_happy_app.models.ground_condition import GroundCondition
from umauma_happy_app.models.course import Course
from umauma_happy_app.models.distance import Distance

class Race(models.Model):
  date = models.DateTimeField()
  number = models.IntegerField()
  name = models.CharField(max_length=100)
  arena = models.CharField(max_length=50)
  ground_condition = models.ForeignKey(GroundCondition, on_delete=models.PROTECT)
  course = models.ForeignKey(Course, on_delete=models.PROTECT)
  distance = models.ForeignKey(Distance, on_delete=models.PROTECT)
  departure_time = models.DateTimeField()
  head_count = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'umauma_happy_app'