from django.db import models

class Horse(models.Model):
  name = models.CharField(max_length=50)
  birth_year = models.IntegerField()
  link = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  def __str__(self):
    return self.name

  class Meta:
    app_label = 'umauma_happy_app'