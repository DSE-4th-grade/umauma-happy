from django.urls import path
from social_analysis import views


app_name = 'social_analysis'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:analysis_number>', views.calculate, name='calculate'),
    path('all', views.calculate, name='calculate'),
]
