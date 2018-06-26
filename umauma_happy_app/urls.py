from django.urls import path

from . import views


app_name = 'umauma_happy_app'
urlpatterns = [
    path('', views.index, name='index'),
]
