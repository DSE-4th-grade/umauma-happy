from django.db import models

class Distance(models.Model):
  value = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.value

  class Meta:
    app_label = 'umauma_happy_app'