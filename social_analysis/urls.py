from django.urls import path
from social_analysis import views


app_name = 'social_analysis'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:analysis_number>', views.calculate, name='calculate'),
    path('all', views.calculate, name='calculate_all'),
    path('show_all', views.show_all_aggregate, name='show_all'),
    path('remaining', views.calculate_remaining, name='calculate_remaining'),
    path('<start>/<end>', views.calculate_by_time, name='calculate_by_time'),
]
